"""
CLI runner for continuous sign segmentation on a single video or keypoints file (Phase 4).
"""

import argparse
import json
from pathlib import Path
import sys
import time
from typing import Any, Dict, Optional
import numpy as np

# Ensure research paths in sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
ISLIM_DIR = PROJECT_ROOT / "research" / "ISLiM"
RESEARCH_DIR = PROJECT_ROOT / "research"

for p in [str(PROJECT_ROOT), str(RESEARCH_DIR), str(ISLIM_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from research.segmentation.boundary_detector import ContinuousSignSegmenter
from research.segmentation.classifier_bridge import SegmentClassifierBridge
from research.segmentation.config import SegmentationConfig
from research.segmentation.segment_extractor import SegmentExtractor
from research.segmentation.visualizer import SegmentationVisualizer
from research.video_pipeline.video_processor import VideoProcessor


def process_single_video(
    video_path: Optional[Path] = None,
    keypoints_path: Optional[Path] = None,
    approach: str = "combined",
    decoding: str = "beam",
    output_dir: Optional[Path] = None,
    render_video: bool = True,
) -> Dict[str, Any]:
    """Process single continuous sign video through segmentation and recognition."""
    out_dir = Path(output_dir or SCRIPT_DIR / "results").resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    # 1. Obtain Keypoints and metadata
    if keypoints_path and Path(keypoints_path).exists():
        kp_file = Path(keypoints_path).resolve()
        keypoints = np.load(str(kp_file))
        fps = 30.0
        base_name = kp_file.stem.replace("_keypoints", "")
        v_path = Path(video_path) if video_path else None
    elif video_path and Path(video_path).exists():
        v_path = Path(video_path).resolve()
        base_name = v_path.stem
        print(f"Extracting 94 Holistic landmarks from {v_path.name}...")
        processor = VideoProcessor()
        keypoints, report = processor.process_video(v_path, output_dir=out_dir, save_output=False)
        fps = float(report.get("fps", 30.0))
    else:
        raise ValueError("Must provide either a valid --video or --keypoints path.")

    total_frames = len(keypoints)
    duration_s = total_frames / fps
    print(f"Loaded {total_frames} frames ({duration_s:.2f}s) at {fps:.2f} fps.")

    # 2. Segment
    cfg = SegmentationConfig(approach=approach, results_dir=out_dir)
    segmenter = ContinuousSignSegmenter(cfg)
    extractor = SegmentExtractor(cfg)

    t0 = time.perf_counter()
    seg_res = segmenter.segment(keypoints, fps=fps, approach=approach)
    raw_boundaries = seg_res["raw_segments"]
    features = seg_res["features"]
    frame_states = seg_res["frame_states"]

    extracted = extractor.extract_segments(
        keypoints,
        raw_boundaries,
        fps=fps,
        features=features,
    )

    # 3. Classify Segments
    print("Loading ISLiM classifier...")
    bridge = SegmentClassifierBridge()
    classified_segments = []
    recognized_sequence = []

    for item in extracted:
        meta = item["metadata"]
        landmarks = item["landmarks"]
        pred = bridge.classify_segment(landmarks, is_valid=meta.is_valid, decoding=decoding)
        classified_segments.append({
            "metadata": meta.to_dict(),
            "prediction": pred,
        })
        if meta.is_valid and not pred["is_rejected"]:
            recognized_sequence.append(pred["prediction"])

    total_time_s = time.perf_counter() - t0

    # 4. Baseline Full-Video ISLiM
    print("Running baseline Full-Video ISLiM translation...")
    full_islim_res = bridge.classify_full_video(keypoints, decoding=decoding)

    # 5. Visualizations
    chart_path = out_dir / f"timeline_{base_name}_{approach}.png"
    SegmentationVisualizer.generate_timeline_chart(
        keypoints=keypoints,
        fps=fps,
        features=features,
        detected_segments=classified_segments,
        ground_truth_segments=None,
        output_path=chart_path,
        video_title=f"{base_name} [{approach.upper()}]",
        velocity_threshold=cfg.velocity_start_threshold,
    )

    annotated_video_path = None
    if render_video and v_path and v_path.exists():
        video_out_name = f"segmented_{base_name}.mp4"
        annotated_video_path = out_dir / video_out_name
        print(f"Rendering annotated video: {annotated_video_path.name}...")
        SegmentationVisualizer.generate_annotated_video(
            video_path=v_path,
            fps=fps,
            frame_states=frame_states,
            detected_segments=classified_segments,
            output_path=annotated_video_path,
        )

    output_record = {
        "source": base_name,
        "approach": approach,
        "fps": fps,
        "total_frames": total_frames,
        "duration_seconds": round(duration_s, 3),
        "landmark_shape": list(keypoints.shape),
        "total_processing_time_seconds": round(total_time_s, 4),
        "num_detected_segments": len(classified_segments),
        "recognized_sign_sequence": recognized_sequence,
        "segments": classified_segments,
        "full_video_islim": full_islim_res,
        "timeline_chart": str(chart_path),
        "annotated_video": str(annotated_video_path) if annotated_video_path else None,
    }

    result_json_path = out_dir / f"segmentation_{base_name}_{approach}.json"
    with open(result_json_path, "w", encoding="utf-8") as f:
        json.dump(output_record, f, indent=2)

    print(f"\n--- Results for {base_name} ---")
    print(f"Detected Segments: {len(classified_segments)}")
    print(f"Recognized Signs: {' '.join(recognized_sequence) if recognized_sequence else '[None]'}")
    print(f"Full-Video ISLiM: \"{full_islim_res['prediction']}\"")
    print(f"Timeline Chart: {chart_path}")
    if annotated_video_path:
        print(f"Annotated Video: {annotated_video_path}")
    print(f"Report JSON: {result_json_path}")

    return output_record


def main():
    parser = argparse.ArgumentParser(description="Signova AI Continuous Sign Segmentation Runner")
    parser.add_argument("--video", type=str, default=None, help="Path to input video file")
    parser.add_argument("--keypoints", type=str, default=None, help="Path to pre-extracted .npy keypoints")
    parser.add_argument("--approach", choices=["combined", "motion", "landmark"], default="combined")
    parser.add_argument("--decoding", choices=["beam", "greedy"], default="beam")
    parser.add_argument("--output-dir", type=str, default=None)
    parser.add_argument("--no-render-video", action="store_true")

    args = parser.parse_args()
    process_single_video(
        video_path=Path(args.video) if args.video else None,
        keypoints_path=Path(args.keypoints) if args.keypoints else None,
        approach=args.approach,
        decoding=args.decoding,
        output_dir=Path(args.output_dir) if args.output_dir else None,
        render_video=not args.no_render_video,
    )


if __name__ == "__main__":
    main()
