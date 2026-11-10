"""
Segment extraction, validation, and structured metadata formatting (Phase 4).
"""

from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Tuple
import numpy as np

from .config import SegmentationConfig


@dataclass
class SegmentMetadata:
    """Structured representation of an extracted sign gesture segment."""

    segment_id: str
    start_frame: int
    end_frame: int
    start_timestamp: float
    end_timestamp: float
    duration_seconds: float
    frame_count: int
    tracking_quality: float
    hand_presence_ratio: float
    mean_wrist_velocity: float
    max_wrist_velocity: float
    is_valid: bool
    validation_status: str
    rejection_reasons: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SegmentExtractor:
    """
    Extracts individual gesture segments from continuous keypoint sequences,
    validates criteria, and preserves original (T_seg, 94, 4) landmark format.
    """

    def __init__(self, config: Optional[SegmentationConfig] = None):
        self.config = config or SegmentationConfig()

    def extract_segments(
        self,
        keypoints: np.ndarray,
        raw_boundaries: List[Tuple[int, int]],
        fps: float = 30.0,
        features: Optional[Dict[str, np.ndarray]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Process raw boundary intervals into validated segment records with sliced landmarks.

        Args:
            keypoints: Full continuous sequence (T, 94, 4) float32
            raw_boundaries: List of (start_frame, end_frame)
            fps: Frames per second of source video
            features: Optional precomputed kinematic features

        Returns:
            List of dictionaries, each containing 'metadata' (SegmentMetadata) and 'landmarks' (np.ndarray).
        """
        extracted = []

        for idx, (start_f, end_f) in enumerate(raw_boundaries):
            seg_id = f"seg_{idx + 1:03d}"
            start_f = max(0, int(start_f))
            end_f = min(len(keypoints) - 1, int(end_f))
            frame_cnt = end_f - start_f + 1

            if frame_cnt <= 0:
                continue

            seg_landmarks = keypoints[start_f : end_f + 1].copy()  # (frame_cnt, 94, 4)
            start_t = round(start_f / fps, 3)
            end_t = round(end_f / fps, 3)
            duration_s = round(end_t - start_t, 3)

            # Tracking quality & hand presence
            vis_slice = seg_landmarks[:, :, 3]
            avg_vis = float(np.mean(vis_slice))

            # Hand presence across slice
            lh_active = np.any(seg_landmarks[:, 6:27, :3] != 0, axis=(1, 2))
            rh_active = np.any(seg_landmarks[:, 27:48, :3] != 0, axis=(1, 2))
            hand_active = lh_active | rh_active
            hand_presence_ratio = float(np.mean(hand_active))

            # Velocity metrics within segment
            if features is not None and "wrist_velocity" in features:
                vel_slice = features["wrist_velocity"][start_f : end_f + 1]
                mean_vel = float(np.mean(vel_slice))
                max_vel = float(np.max(vel_slice))
            else:
                mean_vel = 0.0
                max_vel = 0.0

            # Validation criteria
            rejection_reasons = []
            if frame_cnt < self.config.min_segment_frames:
                rejection_reasons.append(
                    f"Frame count {frame_cnt} below minimum {self.config.min_segment_frames}"
                )
            if hand_presence_ratio < self.config.min_hand_presence_ratio:
                rejection_reasons.append(
                    f"Hand presence ratio {hand_presence_ratio:.2f} below threshold {self.config.min_hand_presence_ratio}"
                )
            if avg_vis < self.config.min_tracking_quality:
                rejection_reasons.append(
                    f"Tracking quality {avg_vis:.2f} below threshold {self.config.min_tracking_quality}"
                )
            if np.isnan(seg_landmarks).any():
                rejection_reasons.append("Segment landmarks contain NaN values")

            is_valid = len(rejection_reasons) == 0
            val_status = "VALID" if is_valid else f"REJECTED: {'; '.join(rejection_reasons)}"

            meta = SegmentMetadata(
                segment_id=seg_id,
                start_frame=start_f,
                end_frame=end_f,
                start_timestamp=start_t,
                end_timestamp=end_t,
                duration_seconds=duration_s,
                frame_count=frame_cnt,
                tracking_quality=round(avg_vis, 4),
                hand_presence_ratio=round(hand_presence_ratio, 4),
                mean_wrist_velocity=round(mean_vel, 4),
                max_wrist_velocity=round(max_vel, 4),
                is_valid=is_valid,
                validation_status=val_status,
                rejection_reasons=rejection_reasons,
            )

            extracted.append({
                "metadata": meta,
                "landmarks": seg_landmarks,
            })

        return extracted
