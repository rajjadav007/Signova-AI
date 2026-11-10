"""
Quality and confidence validation layer for isolated sign predictions.
Rejects out-of-vocabulary, low-confidence, poorly tracked, or incomplete gestures.
"""

from dataclasses import dataclass
from typing import Dict, Optional, Tuple, Union
import numpy as np

MIN_HAND_PRESENCE_RATIO: float = 0.35
MIN_DYNAMIC_MOTION_ENERGY: float = 0.012
CONFIDENCE_RECOGNIZED_THRESHOLD: float = 0.65
CONFIDENCE_LOW_THRESHOLD: float = 0.45


@dataclass
class ValidationResult:
    status: str  # "recognized", "unknown_sign", "low_confidence", "poor_tracking", "incomplete_gesture"
    confidence: float
    is_valid: bool
    reason: Optional[str] = None


class SignQualityValidator:
    """Multi-stage validator for kinematic tracking and prediction confidence."""

    def __init__(
        self,
        min_hand_presence: float = MIN_HAND_PRESENCE_RATIO,
        min_motion_energy: float = MIN_DYNAMIC_MOTION_ENERGY,
        conf_recognized: float = CONFIDENCE_RECOGNIZED_THRESHOLD,
        conf_low: float = CONFIDENCE_LOW_THRESHOLD,
    ) -> None:
        self.min_hand_presence = min_hand_presence
        self.min_motion_energy = min_motion_energy
        self.conf_recognized = conf_recognized
        self.conf_low = conf_low

    def check_tracking_quality(self, raw_keypoints: np.ndarray) -> Tuple[bool, float]:
        """
        Calculates hand detection ratio across frames.
        raw_keypoints: shape (T, 94, 3) or (T, 94, 4) or (T, 282)
        """
        T = raw_keypoints.shape[0]
        if T == 0:
            return False, 0.0

        if raw_keypoints.ndim == 2:
            reshaped = raw_keypoints.reshape(T, 94, -1)
        else:
            reshaped = raw_keypoints

        # Left hand (6:27), Right hand (27:48)
        hands = reshaped[:, 6:48, :3]
        # Frame has hand if any coordinate in either hand is non-zero
        hand_active_frames = np.any(hands != 0.0, axis=(1, 2))
        presence_ratio = float(np.sum(hand_active_frames) / max(1, T))

        is_acceptable = presence_ratio >= self.min_hand_presence
        return is_acceptable, presence_ratio

    def check_motion_energy(self, raw_keypoints: np.ndarray) -> Tuple[bool, float]:
        """
        Measures variance of hand movement over time.
        Distinguishes active sign execution from frozen/idle hands.
        """
        T = raw_keypoints.shape[0]
        if T <= 1:
            return True, 0.0

        if raw_keypoints.ndim == 2:
            reshaped = raw_keypoints.reshape(T, 94, -1)
        else:
            reshaped = raw_keypoints

        hands = reshaped[:, 6:48, :3]  # (T, 42, 3)
        # Standard deviation along temporal axis
        temporal_std = np.std(hands, axis=0)  # (42, 3)
        energy = float(np.mean(temporal_std))

        is_dynamic = energy >= self.min_motion_energy
        return is_dynamic, energy

    def validate(
        self,
        predicted_idx: int,
        confidence: float,
        is_dynamic_sign: bool,
        raw_keypoints: Optional[np.ndarray] = None,
    ) -> ValidationResult:
        """
        Full prediction validation.
        """
        # 1. Background class check
        if predicted_idx == 0:
            return ValidationResult(
                status="unknown_sign",
                confidence=float(confidence),
                is_valid=False,
                reason="Neutral resting posture or background gesture detected.",
            )

        # 2. Tracking quality check (if raw keypoints provided)
        if raw_keypoints is not None and len(raw_keypoints) > 0:
            tracked_ok, presence = self.check_tracking_quality(raw_keypoints)
            if not tracked_ok:
                return ValidationResult(
                    status="poor_tracking",
                    confidence=float(confidence),
                    is_valid=False,
                    reason=f"Insufficient hand tracking visibility ({presence * 100:.1f}% frames).",
                )

            # 3. Dynamic motion check
            if is_dynamic_sign:
                has_motion, energy = self.check_motion_energy(raw_keypoints)
                if not has_motion:
                    return ValidationResult(
                        status="incomplete_gesture",
                        confidence=float(confidence),
                        is_valid=False,
                        reason=f"Insufficient movement for dynamic sign (motion energy {energy:.4f}).",
                    )

        # 4. Confidence thresholds
        if confidence < self.conf_low:
            return ValidationResult(
                status="unknown_sign",
                confidence=float(confidence),
                is_valid=False,
                reason=f"Prediction confidence {confidence:.2f} is below rejection threshold {self.conf_low:.2f}.",
            )
        elif confidence < self.conf_recognized:
            return ValidationResult(
                status="low_confidence",
                confidence=float(confidence),
                is_valid=False,
                reason=f"Prediction confidence {confidence:.2f} is moderate; confirmation required.",
            )

        return ValidationResult(
            status="recognized",
            confidence=float(confidence),
            is_valid=True,
            reason=None,
        )


quality_validator = SignQualityValidator()
