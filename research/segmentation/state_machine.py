"""
Configurable Finite State Machine for Continuous Sign Segmentation (Phase 4).
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class SignState(str, Enum):
    IDLE = "IDLE"
    SIGN_STARTED = "SIGN_STARTED"
    SIGN_IN_PROGRESS = "SIGN_IN_PROGRESS"
    POSSIBLE_SIGN_END = "POSSIBLE_SIGN_END"
    SIGN_COMPLETED = "SIGN_COMPLETED"


class SegmentationStateMachine:
    """
    State machine tracking temporal gesture states:
    IDLE -> SIGN_STARTED -> SIGN_IN_PROGRESS -> POSSIBLE_SIGN_END -> SIGN_COMPLETED -> IDLE
    """

    def __init__(
        self,
        start_confirmation_frames: int = 2,
        end_confirmation_frames: int = 5,
        min_segment_frames: int = 6,
        max_segment_frames: int = 150,
    ):
        self.start_confirmation_frames = start_confirmation_frames
        self.end_confirmation_frames = end_confirmation_frames
        self.min_segment_frames = min_segment_frames
        self.max_segment_frames = max_segment_frames

        self.current_state = SignState.IDLE
        self.current_segment_start: Optional[int] = None
        self.consecutive_active_frames = 0
        self.consecutive_idle_frames = 0
        self.completed_segments: List[Tuple[int, int]] = []

    def reset(self) -> None:
        """Reset state machine counters and state."""
        self.current_state = SignState.IDLE
        self.current_segment_start = None
        self.consecutive_active_frames = 0
        self.consecutive_idle_frames = 0
        self.completed_segments.clear()

    def step(
        self,
        frame_idx: int,
        is_active: bool,
        is_static_hold: bool = False,
    ) -> Tuple[SignState, Optional[Tuple[int, int]]]:
        """
        Advance state machine by one frame.

        Args:
            frame_idx: Sequential frame index (0-based)
            is_active: Whether current frame exhibits active gesture motion/presence
            is_static_hold: Whether hands are statically held in active signing space

        Returns:
            Tuple of:
                current_state: SignState after transition
                completed_segment: Optional tuple (start_frame, end_frame) if segment just finished
        """
        emitted_segment: Optional[Tuple[int, int]] = None
        effective_active = is_active or is_static_hold

        if self.current_state == SignState.IDLE:
            if effective_active:
                self.consecutive_active_frames = 1
                self.current_segment_start = frame_idx
                self.current_state = (
                    SignState.SIGN_IN_PROGRESS
                    if self.start_confirmation_frames <= 1
                    else SignState.SIGN_STARTED
                )
            else:
                self.consecutive_active_frames = 0

        elif self.current_state == SignState.SIGN_STARTED:
            if effective_active:
                self.consecutive_active_frames += 1
                if self.consecutive_active_frames >= self.start_confirmation_frames:
                    self.current_state = SignState.SIGN_IN_PROGRESS
            else:
                # Spurious noise / false start - abort back to IDLE
                self.current_state = SignState.IDLE
                self.current_segment_start = None
                self.consecutive_active_frames = 0

        elif self.current_state == SignState.SIGN_IN_PROGRESS:
            # Check maximum duration timeout
            duration = (
                frame_idx - self.current_segment_start
                if self.current_segment_start is not None
                else 0
            )
            if duration >= self.max_segment_frames:
                # Force complete segment
                emitted_segment = (self.current_segment_start, frame_idx)
                self.completed_segments.append(emitted_segment)
                self.current_state = SignState.SIGN_COMPLETED
                self.current_segment_start = None
                self.consecutive_idle_frames = 0
                return self.current_state, emitted_segment

            if effective_active:
                self.consecutive_idle_frames = 0
            else:
                self.consecutive_idle_frames = 1
                self.current_state = SignState.POSSIBLE_SIGN_END

        elif self.current_state == SignState.POSSIBLE_SIGN_END:
            if effective_active:
                # Resumed signing - false pause, recover back to IN_PROGRESS
                self.consecutive_idle_frames = 0
                self.current_state = SignState.SIGN_IN_PROGRESS
            else:
                self.consecutive_idle_frames += 1
                if self.consecutive_idle_frames >= self.end_confirmation_frames:
                    # Confirmed end of sign
                    end_frame = frame_idx - self.end_confirmation_frames + 1
                    start_frame = (
                        self.current_segment_start
                        if self.current_segment_start is not None
                        else end_frame
                    )
                    length = end_frame - start_frame + 1

                    if length >= self.min_segment_frames:
                        emitted_segment = (start_frame, end_frame)
                        self.completed_segments.append(emitted_segment)
                        self.current_state = SignState.SIGN_COMPLETED
                    else:
                        # Too short to be a valid sign
                        self.current_state = SignState.IDLE

                    self.current_segment_start = None
                    self.consecutive_idle_frames = 0

        elif self.current_state == SignState.SIGN_COMPLETED:
            # Transition out of SIGN_COMPLETED
            if effective_active:
                self.current_segment_start = frame_idx
                self.consecutive_active_frames = 1
                self.current_state = (
                    SignState.SIGN_IN_PROGRESS
                    if self.start_confirmation_frames <= 1
                    else SignState.SIGN_STARTED
                )
            else:
                self.current_state = SignState.IDLE
                self.consecutive_active_frames = 0

        return self.current_state, emitted_segment

    def finalize(self, total_frames: int) -> Optional[Tuple[int, int]]:
        """Handle open segments when video ends."""
        if self.current_state in (SignState.SIGN_IN_PROGRESS, SignState.POSSIBLE_SIGN_END):
            start = self.current_segment_start or 0
            end = total_frames - 1
            if (end - start + 1) >= self.min_segment_frames:
                seg = (start, end)
                self.completed_segments.append(seg)
                self.current_state = SignState.SIGN_COMPLETED
                return seg
        self.current_state = SignState.IDLE
        return None
