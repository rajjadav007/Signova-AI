"""
ISLiM Preprocessing Parity Verification Script (Part 1.6.1)

Directly compares original upstream ISLiM functions against new preprocessing pipeline:
1. Landmark extraction mapping & index verification
2. Missing landmark temporal interpolation parity
3. Spatial coordinate min-max normalization parity
4. Temporal downsampling and padding parity
5. End-to-end tensor comparison on deterministic keypoint samples
"""

import sys
import types
from pathlib import Path
from unittest.mock import MagicMock
import numpy as np
import torch

# Ensure mock mediapipe.solutions exists so scripts/preprocess/extract_keypoints.py can import
mp = types.ModuleType("mediapipe")
mp.solutions = MagicMock()


class MockPoseLandmark:
    LEFT_SHOULDER = 11
    RIGHT_SHOULDER = 12
    LEFT_ELBOW = 13
    RIGHT_ELBOW = 14
    LEFT_HIP = 23
    RIGHT_HIP = 24


mp.solutions.holistic.PoseLandmark = MockPoseLandmark
sys.modules["mediapipe"] = mp
sys.modules["mediapipe.solutions"] = mp.solutions

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

# Import Original upstream functions
from scripts.preprocess.extract_keypoints import (
    interpolate_keypoints as orig_interpolate,
    POSE_INDICES as ORIG_POSE,
    FACE_LIPS as ORIG_LIPS,
    FACE_EYES as ORIG_EYES,
    FACE_EYEBROWS as ORIG_EYEBROWS,
    FACE_INDICES as ORIG_FACE,
    NUM_KEYPOINTS as ORIG_NUM_KP,
    KEYPOINT_COORDS as ORIG_COORDS,
    MAX_MISSING_CONSECUTIVE as ORIG_MAX_MISSING,
)
from src.data.dataset import _normalize_keypoints as orig_normalize_keypoints

# Import New preprocessing modules
from preprocessing.landmark_mapping import (
    POSE_INDICES as NEW_POSE,
    FACE_LIPS as NEW_LIPS,
    FACE_EYES as NEW_EYES,
    FACE_EYEBROWS as NEW_EYEBROWS,
    FACE_INDICES as NEW_FACE,
    NUM_LANDMARKS as NEW_NUM_KP,
    NUM_CHANNELS as NEW_COORDS,
)
from preprocessing.interpolation import (
    interpolate_keypoints as new_interpolate,
    MAX_MISSING_CONSECUTIVE as NEW_MAX_MISSING,
)
from preprocessing.normalization import normalize_coordinates as new_normalize
from preprocessing.temporal_processing import resample_temporal as new_resample
from preprocessing.tensor_conversion import convert_to_tensor as new_convert
from preprocessing import preprocess_sequence


def create_deterministic_sample(T: int, seed: int = 42) -> np.ndarray:
    """Create a realistic deterministic landmark sequence with varied gaps."""
    rng = np.random.RandomState(seed)
    seq = rng.uniform(10.0, 150.0, size=(T, 94, 4)).astype(np.float32)
    # Default valid visibility
    seq[:, :, 3] = 1.0

    # 1. Short gaps <= 5 in left hand (k=10)
    if T > 15:
        seq[5:8, 10] = [0.0, 0.0, 0.0, 0.0]  # gap = 4 <= 5 (frames 5,6,7 missing)

    # 2. Long gaps > 5 in right hand (k=30)
    if T > 25:
        seq[12:19, 30] = [0.0, 0.0, 0.0, 0.0]  # gap = 8 > 5 (7 missing frames)

    # 3. Boundary missing frames in pose (k=0)
    if T > 10:
        seq[0:3, 0] = [0.0, 0.0, 0.0, 0.0]  # leading missing
        seq[-2:, 0] = [0.0, 0.0, 0.0, 0.0]  # trailing missing

    # 4. Completely missing landmark (k=50)
    seq[:, 50] = [0.0, 0.0, 0.0, 0.0]

    return seq


def verify_task_1():
    print("\n--- Task 1: Landmark Extraction & Index Parity ---")
    results = {}

    # Pose indices
    pose_match = ORIG_POSE == NEW_POSE
    results["pose_indices_match"] = pose_match
    print(f"  Pose Indices Match       : {pose_match} ({len(NEW_POSE)} landmarks)")

    # Face lips indices
    lips_match = ORIG_LIPS == NEW_LIPS
    results["lips_indices_match"] = lips_match
    print(f"  Face Lips Indices Match  : {lips_match} ({len(NEW_LIPS)} landmarks)")

    # Face eyes indices
    eyes_match = ORIG_EYES == NEW_EYES
    results["eyes_indices_match"] = eyes_match
    print(f"  Face Eyes Indices Match  : {eyes_match} ({len(NEW_EYES)} landmarks)")

    # Face eyebrows indices
    eyebrows_match = ORIG_EYEBROWS == NEW_EYEBROWS
    results["eyebrows_indices_match"] = eyebrows_match
    print(f"  Eyebrows Indices Match   : {eyebrows_match} ({len(NEW_EYEBROWS)} landmarks)")

    # Total face indices
    face_match = ORIG_FACE == NEW_FACE
    results["face_indices_match"] = face_match
    print(f"  Total Face Indices Match : {face_match} ({len(NEW_FACE)} landmarks)")

    # Dimension constants
    dims_match = (ORIG_NUM_KP == NEW_NUM_KP) and (ORIG_COORDS == NEW_COORDS)
    results["dimension_constants_match"] = dims_match
    print(f"  Total Keypoints (94)     : {ORIG_NUM_KP == NEW_NUM_KP} ({NEW_NUM_KP})")
    print(f"  Channels per Point (4)   : {ORIG_COORDS == NEW_COORDS} ({NEW_COORDS})")

    all_passed = all(results.values())
    print(f"  [Task 1 Verdict]: {'PASS' if all_passed else 'FAIL'}")
    return all_passed, results


def verify_task_2():
    print("\n--- Task 2: Interpolation Parity ---")
    results = {}

    # Check max missing threshold
    thresh_match = ORIG_MAX_MISSING == NEW_MAX_MISSING
    results["max_missing_match"] = thresh_match
    print(f"  Max Gap Threshold Match  : {thresh_match} ({ORIG_MAX_MISSING} vs {NEW_MAX_MISSING})")

    # Run side-by-side interpolation across test lengths
    diffs = []
    for T in [30, 80, 150]:
        sample = create_deterministic_sample(T, seed=T)
        orig_out = orig_interpolate(sample.copy())
        new_out = new_interpolate(sample.copy(), copy=True)

        max_d = float(np.max(np.abs(orig_out - new_out)))
        mean_d = float(np.mean(np.abs(orig_out - new_out)))
        diffs.append((T, max_d, mean_d))
        print(f"  T={T:<3}: Max Diff={max_d:.2e}, Mean Diff={mean_d:.2e}")

    max_overall_diff = max(d[1] for d in diffs)
    interp_exact = max_overall_diff == 0.0
    results["interpolation_exact_match"] = interp_exact
    print(f"  Overall Interpolation Diff: {max_overall_diff:.2e} ({'EXACT MATCH' if interp_exact else 'DIFFERENCE'})")

    all_passed = all(results.values())
    print(f"  [Task 2 Verdict]: {'PASS' if all_passed else 'FAIL'}")
    return all_passed, results


def verify_task_3():
    print("\n--- Task 3: Normalization Parity ---")
    results = {}

    diffs = []
    for T in [30, 80, 150]:
        sample = create_deterministic_sample(T, seed=T)
        interp = orig_interpolate(sample.copy())

        # Original normalization (isolated before temporal resize)
        orig_seq = interp.copy()
        x, y, z = orig_seq[:, :, 0:1], orig_seq[:, :, 1:2], orig_seq[:, :, 2:3]
        for arr in [x, y, z]:
            rng = arr.max() - arr.min()
            if rng > 1e-8:
                arr[...] = (arr - arr.min()) / rng
            else:
                arr[...] = arr - arr.min()
        orig_normed = np.concatenate([x, y, z, orig_seq[:, :, 3:4]], axis=2)

        # New normalization
        new_normed = new_normalize(interp.copy(), copy=True)

        max_d = float(np.max(np.abs(orig_normed - new_normed)))
        mean_d = float(np.mean(np.abs(orig_normed - new_normed)))
        diffs.append((T, max_d, mean_d))
        print(f"  T={T:<3}: Max Diff={max_d:.2e}, Mean Diff={mean_d:.2e}")

    max_norm_diff = max(d[1] for d in diffs)
    norm_exact = max_norm_diff == 0.0
    results["normalization_exact_match"] = norm_exact
    print(f"  Overall Normalization Diff: {max_norm_diff:.2e} ({'EXACT MATCH' if norm_exact else 'DIFFERENCE'})")

    all_passed = all(results.values())
    print(f"  [Task 3 Verdict]: {'PASS' if all_passed else 'FAIL'}")
    return all_passed, results


def verify_task_4():
    print("\n--- Task 4: Temporal Processing Parity ---")
    results = {}

    diffs = []
    # Test cases: shorter (45), exact (128), longer (200)
    for T in [45, 128, 200]:
        sample = create_deterministic_sample(T, seed=T)

        # Original temporal processing
        orig_seq = sample.copy()
        if T > 128:
            indices = torch.linspace(0, T - 1, 128).long()
            orig_temporal = orig_seq[indices.numpy()]
        elif T < 128:
            pad = np.zeros((128 - T, 94, 4), dtype=np.float32)
            orig_temporal = np.concatenate([orig_seq, pad], axis=0)
        else:
            orig_temporal = orig_seq

        # New temporal processing
        new_temporal, valid_frames = new_resample(sample.copy(), target_frames=128)

        max_d = float(np.max(np.abs(orig_temporal - new_temporal)))
        mean_d = float(np.mean(np.abs(orig_temporal - new_temporal)))
        diffs.append((T, max_d, mean_d))
        print(f"  T={T:<3}: Output Shape={new_temporal.shape}, Max Diff={max_d:.2e}, Mean Diff={mean_d:.2e}")

    max_temp_diff = max(d[1] for d in diffs)
    temp_exact = max_temp_diff == 0.0
    results["temporal_exact_match"] = temp_exact
    print(f"  Overall Temporal Diff     : {max_temp_diff:.2e} ({'EXACT MATCH' if temp_exact else 'DIFFERENCE'})")

    all_passed = all(results.values())
    print(f"  [Task 4 Verdict]: {'PASS' if all_passed else 'FAIL'}")
    return all_passed, results


def verify_task_5():
    print("\n--- Task 5: End-to-End Final Tensor Parity ---")
    results = {}

    test_lengths = [45, 128, 200]
    e2e_results = []

    for T in test_lengths:
        sample = create_deterministic_sample(T, seed=100 + T)

        # ── Pipeline A: Upstream ISLiM Reference ──
        # Step 1: extract_keypoints interpolation
        ref_interp = orig_interpolate(sample.copy())
        # Step 2: dataset normalization & temporal resize
        ref_kp, ref_n_frames = orig_normalize_keypoints(ref_interp.copy(), max_frames=128)
        # Step 3: PyTorch tensor formatting
        ref_tensor = torch.from_numpy(ref_kp).float().unsqueeze(0)  # (1, 4, 94, 128)

        # ── Pipeline B: New Signova Preprocessing ──
        new_tensor = preprocess_sequence(sample.copy(), add_batch_dim=True)

        # Comparison metrics
        max_abs_diff = float(torch.max(torch.abs(ref_tensor - new_tensor)).item())
        mean_abs_diff = float(torch.mean(torch.abs(ref_tensor - new_tensor)).item())
        shape_match = ref_tensor.shape == new_tensor.shape
        dtype_match = ref_tensor.dtype == new_tensor.dtype

        e2e_results.append({
            "T": T,
            "input_shape": sample.shape,
            "ref_shape": tuple(ref_tensor.shape),
            "new_shape": tuple(new_tensor.shape),
            "shape_match": shape_match,
            "ref_dtype": str(ref_tensor.dtype),
            "new_dtype": str(new_tensor.dtype),
            "dtype_match": dtype_match,
            "max_abs_diff": max_abs_diff,
            "mean_abs_diff": mean_abs_diff,
        })

        print(f"  Sample T={T:<3}:")
        print(f"    Input Shape           : {sample.shape}")
        print(f"    Reference Tensor Shape: {tuple(ref_tensor.shape)} ({ref_tensor.dtype})")
        print(f"    New Tensor Shape      : {tuple(new_tensor.shape)} ({new_tensor.dtype})")
        print(f"    Shape & Dtype Match   : {shape_match and dtype_match}")
        print(f"    Max Absolute Diff     : {max_abs_diff:.2e}")
        print(f"    Mean Absolute Diff    : {mean_abs_diff:.2e}")

    max_diff_overall = max(r["max_abs_diff"] for r in e2e_results)
    e2e_exact = max_diff_overall == 0.0
    results["all_shapes_match"] = all(r["shape_match"] for r in e2e_results)
    results["all_dtypes_match"] = all(r["dtype_match"] for r in e2e_results)
    results["e2e_exact_match"] = e2e_exact

    print(f"\n  Final End-to-End Maximum Absolute Difference: {max_diff_overall:.2e}")
    print(f"  Parity Status: {'EXACT BITWISE MATCH (Diff = 0.0)' if e2e_exact else 'NUMERICAL DIFFERENCE'}")
    all_passed = all(results.values())
    print(f"  [Task 5 Verdict]: {'PASS' if all_passed else 'FAIL'}")
    return all_passed, e2e_results


def main():
    print("=" * 70)
    print("  ISLiM Preprocessing Parity Verification (Part 1.6.1)")
    print("=" * 70)

    t1_pass, t1_res = verify_task_1()
    t2_pass, t2_res = verify_task_2()
    t3_pass, t3_res = verify_task_3()
    t4_pass, t4_res = verify_task_4()
    t5_pass, t5_res = verify_task_5()

    print("\n" + "=" * 70)
    print("  FINAL PARITY VERIFICATION SUMMARY")
    print("=" * 70)
    print(f"  Task 1 (Landmark Extraction) : {'PASS' if t1_pass else 'FAIL'}")
    print(f"  Task 2 (Interpolation)       : {'PASS' if t2_pass else 'FAIL'}")
    print(f"  Task 3 (Normalization)       : {'PASS' if t3_pass else 'FAIL'}")
    print(f"  Task 4 (Temporal Processing) : {'PASS' if t4_pass else 'FAIL'}")
    print(f"  Task 5 (Final Tensor Parity) : {'PASS' if t5_pass else 'FAIL'}")

    all_tasks_passed = all([t1_pass, t2_pass, t3_pass, t4_pass, t5_pass])
    verdict = "PASS" if all_tasks_passed else "FAIL"
    print(f"\n  OVERALL PREPROCESSING PARITY VERDICT: {verdict}")
    print("=" * 70)

    if not all_tasks_passed:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
