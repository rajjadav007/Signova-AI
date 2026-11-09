#!/usr/bin/env python3
"""
Command-Line Interface for Signova AI Video-to-ISLiM Inference Pipeline (Part 2.2).

Usage Examples:
    python video_to_inference.py --video Deaf-U-SnapYT.App.mp4
    python video_to_inference.py --video International-Week-of-SnapYT.App.mp4 --decoding both
    python video_to_inference.py --video Deaf-U-SnapYT.App.mp4 --device cpu
"""

import argparse
import json
import os
from pathlib import Path
import sys

# Ensure project directories are in sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
ISLIM_DIR = PROJECT_ROOT / "research" / "ISLiM"
if str(SCRIPT_DIR.parent) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR.parent))
if str(ISLIM_DIR) not in sys.path:
    sys.path.insert(0, str(ISLIM_DIR))

# Ensure MPLCONFIGDIR is set to writable directory
os.environ["MPLCONFIGDIR"] = os.environ.get("TEMP", "C:/Temp")

try:
    from research.video_pipeline.video_inference_pipeline import (
        DEFAULT_PART2_2_RESULTS_DIR,
        VideoToISLiMPipeline,
    )
except ImportError:
    from video_pipeline.video_inference_pipeline import (
        DEFAULT_PART2_2_RESULTS_DIR,
        VideoToISLiMPipeline,
    )


def parse_args():
    parser = argparse.ArgumentParser(
        description="Signova AI Video-to-ISLiM Inference Pipeline (Part 2.2)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--video", "-v",
        required=True,
        type=str,
        help="Path to input video file (.mp4, .avi, .mov, .mkv)",
    )
    parser.add_argument(
        "--decoding", "-d",
        choices=["beam", "greedy", "both"],
        default="both",
        help="Text decoding strategy",
    )
    parser.add_argument(
        "--device",
        choices=["auto", "cuda", "cpu"],
        default="auto",
        help="Compute device",
    )
    parser.add_argument(
        "--output-dir", "-o",
        type=str,
        default=str(DEFAULT_PART2_2_RESULTS_DIR),
        help="Directory to save output .npy and report .json",
    )
    parser.add_argument(
        "--checkpoint",
        type=str,
        default=None,
        help="Custom path to model checkpoint (.pt)",
    )
    parser.add_argument(
        "--tokenizer",
        type=str,
        default=None,
        help="Custom path to tokenizer directory",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    video_path = Path(args.video).resolve()

    if not video_path.exists():
        print(f"Error: Video file not found: {video_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Initializing Video-to-ISLiM Pipeline on device: {args.device}...")
    pipeline = VideoToISLiMPipeline(
        checkpoint_path=args.checkpoint,
        tokenizer_dir=args.tokenizer,
        device=args.device,
        results_dir=args.output_dir,
    )

    print(f"Processing video: {video_path.name}...")
    if args.decoding == "both":
        result = pipeline.predict_video_both_decodings(
            video_path=video_path,
            output_dir=args.output_dir,
            save_output=True,
        )
        print("\n=== Video-to-ISLiM Translation Result ===")
        print(f"Video: {result['input_video_filename']} ({result['extracted_frame_count']} frames, {result['fps']} FPS)")
        print(f"Landmark Shape: {result['landmark_shape']} | Presence: {result['landmark_presence_percentage']}%")
        print(f"Beam Search (B=4):   \"{result['beam_search']['prediction']}\"")
        print(f"Greedy Search (B=1): \"{result['greedy_search']['prediction']}\"")
        print(f"Total Processing Time: {result['timings']['total_processing_time_seconds']}s")
        print(f"Saved Report: {result['saved_report_path']}")
    else:
        result = pipeline.predict_video(
            video_path=video_path,
            decoding=args.decoding,
            output_dir=args.output_dir,
            save_output=True,
        )
        print("\n=== Video-to-ISLiM Translation Result ===")
        print(f"Video: {result['input_video_filename']} ({result['extracted_frame_count']} frames, {result['fps']} FPS)")
        print(f"Landmark Shape: {result['landmark_shape']} | Presence: {result['landmark_presence_percentage']}%")
        print(f"Prediction ({args.decoding}): \"{result['prediction']}\"")
        print(f"Total Processing Time: {result['timings']['total_processing_time_seconds']}s")
        print(f"Saved Report: {result['saved_report_path']}")


if __name__ == "__main__":
    main()
