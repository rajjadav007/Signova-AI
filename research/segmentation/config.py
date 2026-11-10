"""
Configuration dataclasses for continuous sign segmentation (Phase 4).
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Union


@dataclass
class SegmentationConfig:
    """Configurable hyperparameters for continuous sign boundary detection."""

    # Segmentation approach: 'motion', 'landmark', or 'combined'
    approach: str = "combined"

    # Kinematic thresholds (normalized coordinate space)
    velocity_start_threshold: float = 0.018
    velocity_idle_threshold: float = 0.010
    velocity_valley_threshold: float = 0.016
    acceleration_spike_threshold: float = 0.025
    kinetic_energy_weight: float = 0.7

    # Spatial / Signing space thresholds (y in [0, 1], 0=top, 1=bottom)
    # Hands elevated above rest position (relative to hips or lower torso)
    rest_y_margin: float = 0.08  # Fraction below hip level considered resting
    static_hold_velocity_ceiling: float = 0.012  # Below this, movement is low

    # State machine confirmation windows (in frames)
    start_confirmation_frames: int = 2
    end_confirmation_frames: int = 3
    min_segment_frames: int = 6       # ~0.20s at 30 fps
    max_segment_frames: int = 150     # ~5.00s at 30 fps

    # Temporal smoothing
    smoothing_window: int = 3

    # Segment validation criteria
    min_hand_presence_ratio: float = 0.25
    min_tracking_quality: float = 0.20

    # Paths
    results_dir: Path = field(
        default_factory=lambda: Path(__file__).resolve().parent / "results"
    )
