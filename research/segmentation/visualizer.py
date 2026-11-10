"""
Visualization generator for continuous sign segmentation (Phase 4).
Generates timeline charts (PNG) and annotated video clips (MP4).
"""

from pathlib import Path
from typing import Any, Dict, List, Optional
import cv2
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np


class SegmentationVisualizer:
    """
    Renders timeline plots and annotated MP4 video playback with boundary overlays.
    """

    STATE_COLORS = {
        "IDLE": (120, 120, 120),          # Gray
        "SIGN_STARTED": (0, 200, 255),     # Yellow / Gold (BGR)
        "SIGN_IN_PROGRESS": (0, 220, 0),   # Green (BGR)
        "POSSIBLE_SIGN_END": (0, 140, 255),# Orange (BGR)
        "SIGN_COMPLETED": (255, 180, 0),  # Cyan / Light blue (BGR)
    }

    @staticmethod
    def generate_timeline_chart(
        keypoints: np.ndarray,
        fps: float,
        features: Dict[str, np.ndarray],
        detected_segments: List[Dict[str, Any]],
        ground_truth_segments: Optional[List[Dict[str, Any]]],
        output_path: Path,
        video_title: str = "Signova AI - Sign Segmentation",
        velocity_threshold: float = 0.015,
    ) -> Path:
        """
        Produce a publication-quality Matplotlib timeline visualization PNG.
        """
        output_path = Path(output_path).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)

        T = len(keypoints)
        time_axis = np.arange(T) / fps
        duration = T / fps

        fig, (ax_sig, ax_seg, ax_track) = plt.subplots(
            nrows=3,
            ncols=1,
            figsize=(14, 8),
            sharex=True,
            gridspec_kw={"height_ratios": [3, 2.5, 1.2]},
        )
        fig.suptitle(f"{video_title} (Duration: {duration:.2f}s, {T} frames)", fontsize=14, weight="bold")

        # 1. Kinematic Signal Plot
        vel = features.get("smooth_velocity", np.zeros(T))
        energy = features.get("hand_energy", np.zeros(T))

        ax_sig.plot(time_axis, vel, label="Wrist Velocity (smoothed)", color="#1f77b4", linewidth=1.8)
        ax_sig.plot(time_axis, energy, label="Hand Kinetic Energy", color="#ff7f0e", linestyle="--", alpha=0.7)
        ax_sig.axhline(
            y=velocity_threshold,
            color="#d62728",
            linestyle=":",
            linewidth=1.5,
            label=f"Active Threshold ({velocity_threshold})",
        )
        ax_sig.set_ylabel("Kinematic Magnitude", fontsize=10)
        ax_sig.set_title("Kinematic Signals & Activation Thresholds", fontsize=11, loc="left")
        ax_sig.grid(True, linestyle="--", alpha=0.4)
        ax_sig.legend(loc="upper right", framealpha=0.9)

        # 2. Segment Comparison Timeline (Ground Truth vs Detected)
        ax_seg.set_ylim(-0.5, 2.5)
        ax_seg.set_yticks([0.5, 1.5])
        ax_seg.set_yticklabels(["Detected Segments", "Ground Truth"], fontsize=10, weight="bold")
        ax_seg.set_title("Sign Segment Boundaries & Recognized Labels", fontsize=11, loc="left")
        ax_seg.grid(True, axis="x", linestyle="--", alpha=0.4)

        # Draw Ground Truth Spans
        if ground_truth_segments:
            for gt in ground_truth_segments:
                g_start = float(gt["start_time"])
                g_end = float(gt["end_time"])
                g_dur = g_end - g_start
                g_label = gt.get("label", "SIGN")

                rect = patches.Rectangle(
                    (g_start, 1.1),
                    g_dur,
                    0.7,
                    linewidth=1.5,
                    edgecolor="#2ca02c",
                    facecolor="#98df8a",
                    alpha=0.8,
                )
                ax_seg.add_patch(rect)
                ax_seg.text(
                    g_start + g_dur / 2.0,
                    1.45,
                    g_label,
                    ha="center",
                    va="center",
                    fontsize=9,
                    weight="bold",
                    color="#004d00",
                )

        # Draw Detected Spans
        for seg in detected_segments:
            meta = seg.get("metadata")
            if hasattr(meta, "to_dict"):
                meta_dict = meta.to_dict()
            else:
                meta_dict = meta or {}

            d_start = float(meta_dict.get("start_timestamp", 0))
            d_end = float(meta_dict.get("end_timestamp", 0))
            d_dur = d_end - d_start
            is_valid = meta_dict.get("is_valid", True)
            pred_text = seg.get("prediction", {}).get("prediction", "") or meta_dict.get("segment_id", "seg")

            box_color = "#1f77b4" if is_valid else "#d62728"
            fill_color = "#aec7e8" if is_valid else "#ff9896"

            rect = patches.Rectangle(
                (d_start, 0.1),
                d_dur,
                0.7,
                linewidth=1.5,
                edgecolor=box_color,
                facecolor=fill_color,
                alpha=0.85,
            )
            ax_seg.add_patch(rect)

            label_str = f"[{meta_dict.get('segment_id', '')}]\n{pred_text}"
            ax_seg.text(
                d_start + d_dur / 2.0,
                0.45,
                label_str,
                ha="center",
                va="center",
                fontsize=8,
                weight="bold",
                color="#08306b" if is_valid else "#67000d",
            )

            # Vertical boundary markers
            ax_sig.axvline(x=d_start, color=box_color, linestyle="--", alpha=0.5)
            ax_sig.axvline(x=d_end, color=box_color, linestyle=":", alpha=0.5)

        # 3. Tracking Quality & Hand Presence
        trk = features.get("tracking_quality", np.ones(T))
        ax_track.fill_between(time_axis, trk, 0, color="#2ca02c", alpha=0.3, label="Tracking Quality")
        ax_track.plot(time_axis, trk, color="#2ca02c", linewidth=1.2)
        ax_track.set_ylim(0, 1.1)
        ax_track.set_ylabel("Quality", fontsize=9)
        ax_track.set_xlabel("Time (seconds)", fontsize=10, weight="bold")
        ax_track.grid(True, linestyle="--", alpha=0.4)

        plt.tight_layout()
        plt.savefig(output_path, dpi=180)
        plt.close(fig)
        return output_path

    @classmethod
    def generate_annotated_video(
        cls,
        video_path: Path,
        fps: float,
        frame_states: List[str],
        detected_segments: List[Dict[str, Any]],
        output_path: Path,
    ) -> Path:
        """
        Generate an annotated MP4 video showing frame state badges and segment info.
        """
        video_path = Path(video_path).resolve()
        output_path = Path(output_path).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)

        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise FileNotFoundError(f"Cannot open video file: {video_path}")

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))

        # Index segments by frame for O(1) lookup
        frame_to_seg: Dict[int, Dict[str, Any]] = {}
        for seg in detected_segments:
            meta = seg.get("metadata")
            m = meta.to_dict() if hasattr(meta, "to_dict") else (meta or {})
            sf = m.get("start_frame", 0)
            ef = m.get("end_frame", 0)
            pred = seg.get("prediction", {}).get("prediction", "")
            for f in range(sf, ef + 1):
                frame_to_seg[f] = {
                    "id": m.get("segment_id", ""),
                    "pred": pred,
                    "valid": m.get("is_valid", True),
                }

        frame_idx = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret or frame is None:
                break

            current_time = frame_idx / fps
            state_str = frame_states[frame_idx] if frame_idx < len(frame_states) else "IDLE"
            state_color = cls.STATE_COLORS.get(state_str, (200, 200, 200))

            # Header Banner
            cv2.rectangle(frame, (0, 0), (width, 85), (20, 20, 20), -1)

            # State Pill / Badge
            cv2.rectangle(frame, (15, 15), (240, 65), state_color, -1)
            cv2.putText(
                frame,
                state_str,
                (25, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.75,
                (0, 0, 0) if state_str in ("SIGN_STARTED", "POSSIBLE_SIGN_END", "SIGN_COMPLETED") else (255, 255, 255),
                2,
                cv2.LINE_AA,
            )

            # Time and Frame metadata
            time_str = f"Time: {current_time:.2f}s | Frame: {frame_idx}/{total_frames}"
            cv2.putText(
                frame,
                time_str,
                (260, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (240, 240, 240),
                2,
                cv2.LINE_AA,
            )

            # Segment Information Overlay if inside active segment
            active_info = frame_to_seg.get(frame_idx)
            if active_info:
                seg_label = f"Segment {active_info['id']}: \"{active_info['pred']}\""
                cv2.putText(
                    frame,
                    seg_label,
                    (260, 70),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.65,
                    (100, 255, 100) if active_info["valid"] else (100, 100, 255),
                    2,
                    cv2.LINE_AA,
                )

            out.write(frame)
            frame_idx += 1

        cap.release()
        out.release()
        return output_path
