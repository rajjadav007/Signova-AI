"""
Example script demonstrating ISLiMPredictor Python API.
"""

from pathlib import Path
import sys

# Ensure research/ISLiM is on sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
ISLIM_DIR = SCRIPT_DIR.parent
if str(ISLIM_DIR) not in sys.path:
    sys.path.insert(0, str(ISLIM_DIR))

from inference.predictor import ISLiMPredictor


def run_example():
    print("=" * 65)
    print("  ISLiM Python API Inference Example")
    print("=" * 65)

    # 1. Initialize predictor once (auto selects CUDA if available)
    print("Initializing ISLiMPredictor (loads model once)...")
    predictor = ISLiMPredictor(device="auto")
    print(f"Model loaded successfully on device: {predictor.device}")

    # 2. Keypoints source: use existing real video keypoints
    keypoints_file = ISLIM_DIR / "results" / "real_video_keypoints.npy"
    if not keypoints_file.exists():
        print(f"Error: Keypoints file not found at {keypoints_file}")
        return

    # 3. Predict using official beam search
    print(f"\nRunning beam search (num_beams=4)...")
    result_beam = predictor.predict(keypoints=keypoints_file, decoding="beam")
    print(f"Beam Prediction: \"{result_beam['prediction']}\"")
    print(f"Latency: {result_beam['inference_time_ms']} ms (Total: {result_beam['total_time_ms']} ms)")

    # 4. Predict using greedy decoding
    print(f"\nRunning greedy decoding (num_beams=1)...")
    result_greedy = predictor.predict(keypoints=keypoints_file, decoding="greedy")
    print(f"Greedy Prediction: \"{result_greedy['prediction']}\"")
    print(f"Latency: {result_greedy['inference_time_ms']} ms")

    print("\n[Done] Example executed successfully.")


if __name__ == "__main__":
    run_example()
