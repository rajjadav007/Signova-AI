"""
Temporal sliding window and gesture boundary segmentation for live webcam streams.
Maintains a rolling 30-frame landmark buffer, detects kinematic motion boundaries,
and triggers isolated recognition upon gesture completion with debounce protection.
"""

from collections import deque
import logging
from typing import Deque, Optional
import numpy as np

logger = logging.getLogger("signova.ml.segmentation")

DEFAULT_WINDOW_SIZE: int = 30
MOTION_START_THRESHOLD: float = 0.025
MOTION_SETTLE_THRESHOLD: float = 0.012
DEFAULT_COOLDOWN_FRAMES: int = 45  # 1.5s at 30 FPS


class SignSegmentationBuffer:
    """Manages rolling temporal buffer and motion-based sign trigger."""

    def __init__(
        self,
        window_size: int = DEFAULT_WINDOW_SIZE,
        start_threshold: float = MOTION_START_THRESHOLD,
        settle_threshold: float = MOTION_SETTLE_THRESHOLD,
        cooldown_frames: int = DEFAULT_COOLDOWN_FRAMES,
    ) -> None:
        self.window_size = window_size
        self.start_threshold = start_threshold
        self.settle_threshold = settle_threshold
        self.cooldown_frames = cooldown_frames

        self.buffer: Deque[np.ndarray] = deque(maxlen=window_size)
        self.prev_hands: Optional[np.ndarray] = None
        self.is_signing: bool = False
        self.cooldown_counter: int = 0
        self.active_frame_count: int = 0

    def reset(self) -> None:
        """Clears buffer and state."""
        self.buffer.clear()
        self.prev_hands = None
        self.is_signing = False
        self.cooldown_counter = 0
        self.active_frame_count = 0

    def add_frame(self, frame_landmarks: np.ndarray) -> Optional[np.ndarray]:
        """
        Ingests a single frame's landmarks (shape (94, 3) or (94, 4)).
        
        Returns:
            completed_sequence: np.ndarray of shape (window_size, 94, C) if boundary detected,
                                otherwise None.
        """
        self.buffer.append(frame_landmarks)

        if self.cooldown_counter > 0:
            self.cooldown_counter -= 1

        # Extract hands: indices 6:48
        if frame_landmarks.ndim == 2:
            hands = frame_landmarks[6:48, :3]
        else:
            hands = frame_landmarks.reshape(94, -1)[6:48, :3]

        # Calculate kinematic velocity if previous frame exists
        if self.prev_hands is not None:
            # Velocity = average displacement of active hand points
            active_mask = np.any(hands != 0.0, axis=-1) & np.any(self.prev_hands != 0.0, axis=-1)
            if np.any(active_mask):
                displacement = np.linalg.norm(hands[active_mask] - self.prev_hands[active_mask], axis=-1)
                velocity = float(np.mean(displacement))
            else:
                velocity = 0.0
        else:
            velocity = 0.0

        self.prev_hands = hands.copy()

        # State transition logic
        if not self.is_signing:
            if velocity >= self.start_threshold and self.cooldown_counter == 0:
                self.is_signing = True
                self.active_frame_count = 1
        else:
            self.active_frame_count += 1
            # Check for gesture settling or minimum window filled
            has_settled = (velocity < self.settle_threshold and self.active_frame_count >= 15)
            buffer_full = (self.active_frame_count >= self.window_size)

            if (has_settled or buffer_full) and len(self.buffer) == self.window_size:
                # Gesture boundary triggered!
                completed_seq = np.array(self.buffer, dtype=np.float32)
                self.is_signing = False
                self.active_frame_count = 0
                self.cooldown_counter = self.cooldown_frames
                return completed_seq

        return None
