"""
Comparative testing and evaluation of continuous sign segmentation approaches (Phase 4).
Compares:
  1. Motion-based segmentation
  2. Landmark-based segmentation
  3. Combined motion and landmark segmentation (Dual-condition gate)
Against Ground Truth and compares with Full-Video ISLiM translation baseline.
"""

import json
from pathlib import Path
import sys
import time
from typing import Any, Dict, List, Optional
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
from research.segmentation.evaluator import SegmentationEvaluator
from research.segmentation.segment_extractor import SegmentExtractor
from research.segmentation.visualizer import SegmentationVisualizer


def run_comparative_experiment(
    ground_truth_path: Optional[Path] = None,
    results_dir: Optional[Path] = None,
    render_video: bool = True,
) -> Dict[str, Any]:
    """
    Run full comparative segmentation benchmark across test videos.
    """
    gt_file = Path(ground_truth_path or SCRIPT_DIR / "ground_truth.json").resolve()
    out_dir = Path(results_dir or SCRIPT_DIR / "results").resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(gt_file, "r", encoding="utf-8") as f:
        ground_truth_data = json.load(f)

    # Instantiate shared components
    print("Initializing ISLiM Segment Classifier Bridge...")
    classifier_bridge = SegmentClassifierBridge()
    evaluator = SegmentationEvaluator(time_tolerance_seconds=0.30, iou_threshold=0.35)
    approaches = ["motion", "landmark", "combined"]

    test_video_specs = [
        {
            "filename": "vidssavecom-president-prime-minister-chief-minister-indian-sign-language-i_KWDwb1ih.mp4",
            "video_path": PROJECT_ROOT / "vidssavecom-president-prime-minister-chief-minister-indian-sign-language-i_KWDwb1ih.mp4",
            "keypoints_path": RESEARCH_DIR / "video_pipeline" / "results_part2_2" / "vidssavecom-president-prime-minister-chief-minister-indian-sign-language-i_KWDwb1ih_keypoints.npy",
            "title": "Video 1: President / Prime Minister (Short 2.23s sequence)",
        },
        {
            "filename": "Learn-Indian-Sign-SnapYT.App (1) (online-video-cutter.com).mp4",
            "video_path": PROJECT_ROOT / "Learn-Indian-Sign-SnapYT.App (1) (online-video-cutter.com).mp4",
            "keypoints_path": RESEARCH_DIR / "video_pipeline" / "results_part2_2" / "Learn-Indian-Sign-SnapYT.App (1) (online-video-cutter.com)_keypoints.npy",
            "title": "Video 2: Instructional ISL Phrases (5.94s with static hold)",
        },
    ]

    all_results: Dict[str, Any] = {
        "benchmark_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "videos_evaluated": [],
    }

    for spec in test_video_specs:
        v_name = spec["filename"]
        v_path = spec["video_path"]
        kp_path = spec["keypoints_path"]
        v_title = spec["title"]
        gt_entry = ground_truth_data.get(v_name, {})
        gt_segments = gt_entry.get("segments", [])

        print(f"\n=======================================================")
        print(f"Processing: {v_name}")
        print(f"=======================================================")

        if not kp_path.exists():
            raise FileNotFoundError(f"Keypoints file not found: {kp_path}")

        keypoints = np.load(str(kp_path))
        fps = float(gt_entry.get("fps", 30.0))
        total_frames = len(keypoints)
        duration_s = total_frames / fps

        print(f"Loaded keypoints shape: {keypoints.shape}, FPS: {fps:.2f}, Duration: {duration_s:.2f}s")

        # 1. Independent Full-Video ISLiM Baseline
        print("\n[Baseline] Running Full-Video ISLiM translation...")
        full_video_res = classifier_bridge.classify_full_video(keypoints, decoding="beam")
        print(f"Full-Video ISLiM Prediction: \"{full_video_res['prediction']}\" (latency: {full_video_res['inference_time_ms']} ms)")

        video_record: Dict[str, Any] = {
            "video_filename": v_name,
            "fps": fps,
            "total_frames": total_frames,
            "duration_seconds": round(duration_s, 3),
            "landmark_shape": list(keypoints.shape),
            "full_video_islim": full_video_res,
            "ground_truth_segments": gt_segments,
            "approaches": {},
        }

        # 2. Evaluate Each Segmentation Approach
        for approach in approaches:
            print(f"\n--- Testing Approach: {approach.upper()} ---")
            cfg = SegmentationConfig(approach=approach, results_dir=out_dir)
            segmenter = ContinuousSignSegmenter(cfg)
            extractor = SegmentExtractor(cfg)

            t0 = time.perf_counter()
            seg_res = segmenter.segment(keypoints, fps=fps, approach=approach)
            raw_boundaries = seg_res["raw_segments"]
            features = seg_res["features"]
            frame_states = seg_res["frame_states"]

            # Extract validated segments
            extracted = extractor.extract_segments(
                keypoints,
                raw_boundaries,
                fps=fps,
                features=features,
            )

            # Classify valid segments
            classified_segments = []
            recognized_sequence = []
            for item in extracted:
                meta = item["metadata"]
                landmarks = item["landmarks"]
                pred = classifier_bridge.classify_segment(
                    landmarks,
                    is_valid=meta.is_valid,
                    decoding="beam",
                )
                classified_segments.append({
                    "metadata": meta.to_dict(),
                    "prediction": pred,
                })
                if meta.is_valid and not pred["is_rejected"]:
                    recognized_sequence.append(pred["prediction"])

            proc_time_s = time.perf_counter() - t0

            # Quantitative evaluation against Ground Truth
            eval_metrics = evaluator.evaluate(
                predicted_segments=[s["metadata"] for s in classified_segments],
                ground_truth_segments=gt_segments,
                total_duration_seconds=duration_s,
                processing_time_seconds=proc_time_s,
            )

            # Visualizations
            chart_filename = f"timeline_{Path(v_name).stem}_{approach}.png"
            chart_path = out_dir / chart_filename
            SegmentationVisualizer.generate_timeline_chart(
                keypoints=keypoints,
                fps=fps,
                features=features,
                detected_segments=classified_segments,
                ground_truth_segments=gt_segments,
                output_path=chart_path,
                video_title=f"{v_title} [{approach.upper()}]",
                velocity_threshold=cfg.velocity_start_threshold,
            )

            annotated_video_path = None
            if render_video and approach == "combined" and v_path.exists():
                video_out_name = f"segmented_{Path(v_name).stem}.mp4"
                annotated_video_path = out_dir / video_out_name
                print(f"Generating annotated MP4 video: {annotated_video_path.name}...")
                SegmentationVisualizer.generate_annotated_video(
                    video_path=v_path,
                    fps=fps,
                    frame_states=frame_states,
                    detected_segments=classified_segments,
                    output_path=annotated_video_path,
                )

            # Print summary for approach
            b_metrics = eval_metrics["boundary_metrics"]
            s_metrics = eval_metrics["segment_metrics"]
            print(f"Detected: {len(classified_segments)} segments | Recognized: {recognized_sequence}")
            print(f"Boundary F1: {b_metrics['f1_score']:.4f} (P={b_metrics['precision']:.2f}, R={b_metrics['recall']:.2f})")
            print(f"Segment F1:  {s_metrics['f1_score']:.4f} (P={s_metrics['precision']:.2f}, R={s_metrics['recall']:.2f})")
            print(f"Over-seg: {eval_metrics['rates']['over_segmentation_rate']:.2f}, Under-seg: {eval_metrics['rates']['under_segmentation_rate']:.2f}")

            video_record["approaches"][approach] = {
                "detected_segments_count": len(classified_segments),
                "recognized_sequence": recognized_sequence,
                "segments": classified_segments,
                "evaluation": eval_metrics,
                "timeline_chart": str(chart_path),
                "annotated_video": str(annotated_video_path) if annotated_video_path else None,
            }

        all_results["videos_evaluated"].append(video_record)

    # Save detailed JSON report
    report_file = out_dir / "comparative_segmentation_report.json"
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)

    print(f"\n=======================================================")
    print(f"Benchmark Complete! Report saved to: {report_file}")
    print(f"=======================================================")
    return all_results


if __name__ == "__main__":
    run_comparative_experiment()
