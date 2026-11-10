"""
Kinematic feature extraction and boundary detection approaches for continuous sign language (Phase 4).
"""

from typing import Any, Dict, List, Optional, Tuple
import numpy as np

from .config import SegmentationConfig
from .state_machine import SegmentationStateMachine, SignState


class KinematicFeatureExtractor:
    """
    Extracts frame-by-frame kinematic and spatial signals from (T, 94, 4) landmark sequences.
    Preserves exact 94-landmark ordering from ISLiM/MediaPipe Holistic.
    """

    # Indices matching research/ISLiM/preprocessing/landmark_mapping.py
    IDX_LEFT_SHOULDER = 0
    IDX_RIGHT_SHOULDER = 1
    IDX_LEFT_HIP = 4
    IDX_RIGHT_HIP = 5
    IDX_LEFT_WRIST = 6
    IDX_RIGHT_WRIST = 27
    RANGE_LEFT_HAND = slice(6, 27)
    RANGE_RIGHT_HAND = slice(27, 48)

    @classmethod
    def extract_features(
        cls,
        keypoints: np.ndarray,
        fps: float = 30.0,
        smoothing_window: int = 3,
    ) -> Dict[str, np.ndarray]:
        """
        Compute kinematic time series from keypoint sequence.

        Args:
            keypoints: (T, 94, 4) float32 array [x, y, z, visibility]
            fps: Video frames per second
            smoothing_window: Window size for moving average temporal filter

        Returns:
            Dictionary containing 1D time series arrays of length T.
        """
        T = len(keypoints)
        if T == 0:
            raise ValueError("Keypoints sequence cannot be empty.")

        # 1. Hand Presence
        lh_joints = keypoints[:, cls.RANGE_LEFT_HAND, :3]
        rh_joints = keypoints[:, cls.RANGE_RIGHT_HAND, :3]
        lh_present = np.any(lh_joints != 0, axis=(1, 2))
        rh_present = np.any(rh_joints != 0, axis=(1, 2))
        hands_present = lh_present | rh_present

        # 2. Wrist Coordinates
        lw_coords = keypoints[:, cls.IDX_LEFT_WRIST, :3]
        rw_coords = keypoints[:, cls.IDX_RIGHT_WRIST, :3]

        # 3. Wrist Velocities (Euclidean delta)
        lw_vel = np.zeros(T, dtype=np.float32)
        rw_vel = np.zeros(T, dtype=np.float32)

        for t in range(1, T):
            if lh_present[t] and lh_present[t - 1]:
                lw_vel[t] = float(np.linalg.norm(lw_coords[t] - lw_coords[t - 1]))
            if rh_present[t] and rh_present[t - 1]:
                rw_vel[t] = float(np.linalg.norm(rw_coords[t] - rw_coords[t - 1]))

        max_wrist_vel = np.maximum(lw_vel, rw_vel)

        # 4. Hand Kinetic Energy (average velocity across all active hand joints)
        hand_energy = np.zeros(T, dtype=np.float32)
        for t in range(1, T):
            diffs = []
            if lh_present[t] and lh_present[t - 1]:
                d_lh = np.linalg.norm(lh_joints[t] - lh_joints[t - 1], axis=1)
                diffs.extend(d_lh)
            if rh_present[t] and rh_present[t - 1]:
                d_rh = np.linalg.norm(rh_joints[t] - rh_joints[t - 1], axis=1)
                diffs.extend(d_rh)
            if diffs:
                hand_energy[t] = float(np.mean(diffs))

        # 5. Hand Acceleration
        wrist_acc = np.zeros(T, dtype=np.float32)
        wrist_acc[1:] = np.abs(np.diff(max_wrist_vel))

        # 6. Torso and Signing Space Elevation
        # MediaPipe coordinates: y in [0, 1], 0 is top of image, 1 is bottom
        shoulders_y = (keypoints[:, cls.IDX_LEFT_SHOULDER, 1] + keypoints[:, cls.IDX_RIGHT_SHOULDER, 1]) / 2.0
        hips_y = (keypoints[:, cls.IDX_LEFT_HIP, 1] + keypoints[:, cls.IDX_RIGHT_HIP, 1]) / 2.0
        torso_height = np.maximum(np.abs(hips_y - shoulders_y), 0.1)

        # Baseline resting y-level is lower torso / navel (0.80 of torso height below shoulders)
        rest_y_baseline = shoulders_y + 0.80 * torso_height

        in_signing_space = np.zeros(T, dtype=bool)
        for t in range(T):
            if not hands_present[t]:
                in_signing_space[t] = False
                continue
            # If at least one active hand is above resting level (y increases downwards)
            lh_elevated = lh_present[t] and (lw_coords[t, 1] > 0) and (lw_coords[t, 1] < rest_y_baseline[t])
            rh_elevated = rh_present[t] and (rw_coords[t, 1] > 0) and (rw_coords[t, 1] < rest_y_baseline[t])
            in_signing_space[t] = lh_elevated or rh_elevated

        # 7. Temporal Smoothing on velocity and energy
        if smoothing_window > 1:
            kernel = np.ones(smoothing_window, dtype=np.float32) / smoothing_window
            smooth_vel = np.convolve(max_wrist_vel, kernel, mode="same")
            smooth_energy = np.convolve(hand_energy, kernel, mode="same")
        else:
            smooth_vel = max_wrist_vel
            smooth_energy = hand_energy

        # 8. Tracking Quality (fraction of expected landmarks visible)
        vis_scores = keypoints[:, :, 3]  # channel 3 is visibility
        tracking_quality = np.mean(vis_scores, axis=1)

        return {
            "hands_present": hands_present,
            "lh_present": lh_present,
            "rh_present": rh_present,
            "wrist_velocity": max_wrist_vel,
            "smooth_velocity": smooth_vel,
            "hand_energy": smooth_energy,
            "wrist_acceleration": wrist_acc,
            "in_signing_space": in_signing_space,
            "tracking_quality": tracking_quality,
            "torso_height": torso_height,
        }


class ContinuousSignSegmenter:
    """
    Performs sign boundary detection using configurable approaches:
      - 'motion': Motion-based (velocity & acceleration only)
      - 'landmark': Landmark/spatial-based (hand presence & elevation in signing space)
      - 'combined': Multi-signal fusion with dual-condition static hold gate
    """

    def __init__(self, config: Optional[SegmentationConfig] = None):
        self.config = config or SegmentationConfig()

    def segment(
        self,
        keypoints: np.ndarray,
        fps: float = 30.0,
        approach: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Segment a continuous landmark sequence into individual gesture boundaries.

        Returns:
            Dictionary containing:
                approach: Name of approach used
                raw_segments: List of (start_frame, end_frame)
                frame_states: Array of SignState string for each frame
                features: Kinematic feature dictionary
        """
        approach = approach or self.config.approach
        features = KinematicFeatureExtractor.extract_features(
            keypoints,
            fps=fps,
            smoothing_window=self.config.smoothing_window,
        )

        T = len(keypoints)
        state_machine = SegmentationStateMachine(
            start_confirmation_frames=self.config.start_confirmation_frames,
            end_confirmation_frames=self.config.end_confirmation_frames,
            min_segment_frames=self.config.min_segment_frames,
            max_segment_frames=self.config.max_segment_frames,
        )

        frame_states: List[str] = []
        is_active_flags = np.zeros(T, dtype=bool)
        is_static_hold_flags = np.zeros(T, dtype=bool)

        vel = features["smooth_velocity"]
        energy = features["hand_energy"]
        in_space = features["in_signing_space"]
        hands_present = features["hands_present"]

        # Compute activation flags based on selected approach
        for t in range(T):
            if approach == "motion":
                # Approach A: Motion only
                # Active if velocity or energy exceeds threshold
                is_active = (vel[t] > self.config.velocity_start_threshold) or (
                    energy[t] > self.config.velocity_start_threshold
                )
                is_static_hold = False

            elif approach == "landmark":
                # Approach B: Landmark/Spatial only
                # Active if hand present and in active signing volume
                is_active = bool(in_space[t] and hands_present[t])
                is_static_hold = False

            elif approach == "combined":
                # Approach C: Multi-signal combined with dual-condition static hold
                is_elevated = bool(in_space[t] and hands_present[t])
                has_motion = bool(
                    (vel[t] > self.config.velocity_start_threshold)
                    or (energy[t] > self.config.velocity_start_threshold)
                )
                static_hold = bool(
                    is_elevated
                    and (vel[t] <= self.config.static_hold_velocity_ceiling)
                )

                is_active = bool(is_elevated and (has_motion or static_hold))
                is_static_hold = bool(is_elevated and static_hold)
            else:
                raise ValueError(f"Unknown segmentation approach: {approach}")

            is_active_flags[t] = is_active
            is_static_hold_flags[t] = is_static_hold

            state, _ = state_machine.step(
                frame_idx=t,
                is_active=is_active,
                is_static_hold=is_static_hold,
            )
            frame_states.append(state.value)

        # Handle any trailing open segment
        final_seg = state_machine.finalize(total_frames=T)
        if final_seg and final_seg not in state_machine.completed_segments:
            state_machine.completed_segments.append(final_seg)

        return {
            "approach": approach,
            "raw_segments": list(state_machine.completed_segments),
            "frame_states": frame_states,
            "is_active_flags": is_active_flags,
            "is_static_hold_flags": is_static_hold_flags,
            "features": features,
            "total_frames": T,
            "fps": fps,
        }
