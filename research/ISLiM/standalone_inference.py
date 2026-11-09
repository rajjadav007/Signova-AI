#!/usr/bin/env python3
"""
ISLiM Standalone Command-Line Inference Application.

Translates an Indian Sign Language (ISL) keypoint sequence (.npy) into English text.

Usage Examples:
    python standalone_inference.py --input results/real_video_keypoints.npy
    python standalone_inference.py --input results/real_video_keypoints.npy --decoding greedy
    python standalone_inference.py --input results/real_video_keypoints.npy --device cpu
    python standalone_inference.py --input results/real_video_keypoints.npy --output results/prediction.json
"""

import os
import sys
import argparse
from pathlib import Path

# Ensure research/ISLiM is on sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

# Ensure MPLCONFIGDIR is set to writable temp
os.environ["MPLCONFIGDIR"] = os.environ.get("TEMP", "C:/Temp")

from inference.predictor import ISLiMPredictor
from inference.output_handler import save_result_to_json
from inference.exceptions import ISLiMInferenceError


def parse_args():
    parser = argparse.ArgumentParser(
        description="ISLiM Standalone Inference: Indian Sign Language Keypoints to English Translation",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        type=str,
        help="Path to input .npy keypoint file (shape: [T, 94, 4] or [B, T, 94, 4])",
    )
    parser.add_argument(
        "--decoding", "-d",
        choices=["beam", "greedy"],
        default="beam",
        help="Text decoding strategy (beam search or greedy decoding)",
    )
    parser.add_argument(
        "--device",
        choices=["auto", "cuda", "cpu"],
        default="auto",
        help="Execution device ('cuda', 'cpu', or 'auto')",
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="Optional path to save structured output JSON file",
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
        help="Custom path to local T5-small tokenizer directory",
    )
    parser.add_argument(
        "--num_beams",
        type=int,
        default=4,
        help="Number of beams for beam search",
    )
    parser.add_argument(
        "--repetition_penalty",
        type=float,
        default=1.5,
        help="Repetition penalty for generation",
    )
    parser.add_argument(
        "--no_repeat_ngram_size",
        type=int,
        default=3,
        help="No-repeat n-gram size for generation",
    )
    parser.add_argument(
        "--length_penalty",
        type=float,
        default=1.2,
        help="Length penalty for beam search",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    input_path = Path(args.input)

    # 1. Validate input path existence early
    if not input_path.exists():
        print(f"Error: Input file does not exist: {input_path}", file=sys.stderr)
        sys.exit(1)

    try:
        # 2. Initialize Predictor (loads model once)
        print(f"Loading ISLiM model on device '{args.device}'...")
        predictor = ISLiMPredictor(
            checkpoint_path=args.checkpoint,
            tokenizer_dir=args.tokenizer,
            device=args.device,
        )

        # 3. Execute Prediction
        print(f"Translating keypoints from '{input_path.name}' using {args.decoding} decoding...")
        result = predictor.predict(
            keypoints=input_path,
            decoding=args.decoding,
            num_beams=args.num_beams,
            repetition_penalty=args.repetition_penalty,
            no_repeat_ngram_size=args.no_repeat_ngram_size,
            length_penalty=args.length_penalty,
        )

        # 4. Display Results
        print("\n" + "=" * 65)
        print(f"  Translation Result (ISLiM Pretrained Model)")
        print("=" * 65)
        print(f"  Prediction       : \"{result['prediction']}\"")
        print(f"  Device           : {result['device']}")
        print(f"  Decoding Strategy: {result['decoding_strategy']}")
        print(f"  Input Shape      : {result['input_shape']}")
        print(f"  Model Tensor     : {result['model_input_shape']}")
        print(f"  Preprocessing    : {result['preprocessing_time_ms']} ms")
        print(f"  Inference Latency: {result['inference_time_ms']} ms")
        print(f"  Total Time       : {result['total_time_ms']} ms")
        print(f"  Accuracy Status  : {'VERIFIED' if result['accuracy_verified'] else 'UNVERIFIED (No ground truth)'}")
        print("=" * 65)

        # 5. Save output if requested
        if args.output:
            out_file = save_result_to_json(result, args.output)
            print(f"Saved structured result to: {out_file}")

    except ISLiMInferenceError as e:
        print(f"\nInference Error: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"\nUnexpected Failure: {e}", file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    main()
