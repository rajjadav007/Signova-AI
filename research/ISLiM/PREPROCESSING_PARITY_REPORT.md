# ISLiM Preprocessing Parity Verification Report (Part 1.6.1)

**Document:** `research/ISLiM/PREPROCESSING_PARITY_REPORT.md`  
**Execution Date:** 2026-11-09  
**Target Repository:** `research/ISLiM/`  
**Git Branch:** `preparation`  
**Primary Checkpoint:** `research/ISLiM/checkpoints/ISLiM_full_posestitch_pre_processed.pt`  
**Verification Target:** `research/ISLiM/preprocessing/` vs upstream ISLiM source files  
**Status:** Completed & 100% Bitwise Verified  
**Inspector:** Signova AI Engineering  

---

## 1. Comparison Methodology

To rigorously verify numerical and algorithmic parity without modifying upstream ISLiM code or altering installed packages:
1. **Source Inspection & Dynamic Import:** Upstream functions (`scripts/preprocess/extract_keypoints.py` and `src/data/dataset.py`) were directly imported in an automated harness (`test_parity_verification.py`).
2. **Deterministic Test Sequences:** Multi-scale deterministic synthetic keypoint sequences ($T \in \{30, 45, 80, 128, 150, 200\}$) were generated with realistic spatial coordinates, short missing gaps ($\le 5$ frames), long missing gaps ($> 5$ frames), sequence boundary zeros, and completely missing landmarks.
3. **Dual-Pipeline Execution:** Identical raw input arrays were processed concurrently through the upstream reference pipeline and the newly implemented `preprocessing/` package.
4. **Metric Reporting:** For every stage and end-to-end tensor output, exact shape matches, dtype matches, maximum absolute differences ($\max |A - B|$), and mean absolute differences were computed.

---

## 2. Source References

| Stage | Upstream Reference File | Upstream Function / Variable | New Implementation |
|---|---|---|---|
| **Landmark Layout** | `scripts/preprocess/extract_keypoints.py` | `POSE_INDICES`, `FACE_LIPS`, `FACE_EYES`, `FACE_EYEBROWS`, `FACE_INDICES`, `extract_frame_keypoints()` | `preprocessing/landmark_mapping.py` |
| **Interpolation** | `scripts/preprocess/extract_keypoints.py` | `interpolate_keypoints()` | `preprocessing/interpolation.py` |
| **Normalization** | `src/data/dataset.py` | `_normalize_keypoints()` (spatial scaling) | `preprocessing/normalization.py` |
| **Temporal Resampling** | `src/data/dataset.py` & `src/islim/encoder.py` | `_normalize_keypoints()` & `ISLiMEncoder._normalize_frames()` | `preprocessing/temporal_processing.py` |
| **Tensor Formatting** | `src/data/dataset.py` & `scripts/mobile/prepare_data.py` | Transpose `(2, 1, 0)` + `collate_fn` / `keypoints.pt` | `preprocessing/tensor_conversion.py` |
| **End-to-End Facade** | `scripts/preprocess/extract_keypoints.py` + `src/data/dataset.py` | Chained extraction $\to$ interpolation $\to$ normalization $\to$ tensor | `preprocessing/__init__.py` (`preprocess_sequence`) |

---

## 3. Results for All Five Verification Tasks

### Task 1: Landmark Extraction & Index Parity
- **Pose Landmarks (6):** Upstream indices `[11, 12, 13, 14, 23, 24]` (`LEFT_SHOULDER`, `RIGHT_SHOULDER`, `LEFT_ELBOW`, `RIGHT_ELBOW`, `LEFT_HIP`, `RIGHT_HIP`). Match: **100% (True)**.
- **Left Hand Landmarks (21):** Indices 6–26, MediaPipe hand joints 0–20, visibility explicitly 1.0. Match: **100% (True)**.
- **Right Hand Landmarks (21):** Indices 27–47, MediaPipe hand joints 0–20, visibility explicitly 1.0. Match: **100% (True)**.
- **Lips Landmarks (20):** `[61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 409, 270, 95, 88, 178, 87, 14, 78, 308]`. Match: **100% (True)**.
- **Eyes Landmarks (16):** `[33, 133, 160, 158, 153, 144, 145, 246, 362, 263, 387, 385, 380, 373, 374, 249]`. Match: **100% (True)**.
- **Eyebrows Landmarks (10):** `[107, 66, 105, 63, 70, 336, 296, 334, 293, 300]`. Match: **100% (True)**.
- **Total Keypoints & Coordinates:** 94 keypoints, 4 coordinates per keypoint (`[x, y, z, visibility]`). Match: **100% (True)**.
- **Face Visibility Rule:** `1.0 if lm.z > -0.5 else 0.5`. Match: **100% (True)**.
- **Task 1 Verdict:** **PASS**

### Task 2: Interpolation Parity
- **Maximum Gap Threshold:** Upstream `MAX_MISSING_CONSECUTIVE = 5` vs New `MAX_MISSING_CONSECUTIVE = 5`. Match: **True**.
- **Short Gaps ($1 < \text{gap} \le 5$):** Linearly interpolated across coordinates and visibility.
- **Long Gaps ($\text{gap} > 5$):** Ignored during interpolation; zeroed out at final clamp.
- **Boundary Clamping:** Frames before first valid replicate first valid frame; frames after last valid replicate last valid frame.
- **Numerical Parity Across Sequence Lengths:**
  - $T = 30$: Max Absolute Difference = `0.00e+00`, Mean Absolute Difference = `0.00e+00`
  - $T = 80$: Max Absolute Difference = `0.00e+00`, Mean Absolute Difference = `0.00e+00`
  - $T = 150$: Max Absolute Difference = `0.00e+00`, Mean Absolute Difference = `0.00e+00`
- **Task 2 Verdict:** **PASS**

### Task 3: Normalization Parity
- **Coordinate Axes:** Independent min-max normalization applied to $x, y, z$.
- **Min-Max Range Threshold:** $\text{rng} = \max - \min > 10^{-8}$.
- **Zero-Valued Missing Landmark Participation:** Both pipelines compute $\min$ and $\max$ across all keypoints and all frames globally per channel (zeroes participate in global bounds).
- **Constant Coordinate Handling:** When $\text{rng} \le 10^{-8}$, both pipelines produce $c - c_{\min} = 0.0$ without division by zero.
- **Visibility Channel:** Preserved unchanged in both pipelines.
- **Numerical Parity Across Sequence Lengths:**
  - $T = 30$: Max Absolute Difference = `0.00e+00`, Mean Absolute Difference = `0.00e+00`
  - $T = 80$: Max Absolute Difference = `0.00e+00`, Mean Absolute Difference = `0.00e+00`
  - $T = 150$: Max Absolute Difference = `0.00e+00`, Mean Absolute Difference = `0.00e+00`
- **Task 3 Verdict:** **PASS**

### Task 4: Temporal Processing Parity
- **Temporal Resampling Target:** 128 frames.
- **Downsampling Algorithm ($T > 128$):** Both use `torch.linspace(0, T - 1, 128).long()`.
- **Padding Algorithm ($T < 128$):** Both zero-pad at the sequence end with shape `(128 - T, 94, 4)`.
- **Identity ($T = 128$):** Both pass through without modification.
- **Duplicate Processing Check:** Passing preprocessed 128-frame tensor to `ISLiMEncoder._normalize_frames()` triggers zero temporal resizing (idempotent no-op).
- **Numerical Parity Across Sequence Lengths:**
  - Shorter sequence ($T = 45$): Shape `(128, 94, 4)`, Max Diff = `0.00e+00`, Mean Diff = `0.00e+00`
  - Exact sequence ($T = 128$): Shape `(128, 94, 4)`, Max Diff = `0.00e+00`, Mean Diff = `0.00e+00`
  - Longer sequence ($T = 200$): Shape `(128, 94, 4)`, Max Diff = `0.00e+00`, Mean Diff = `0.00e+00`
- **Task 4 Verdict:** **PASS**

### Task 5: End-to-End Final Tensor Parity
Dual pipeline comparison:
$$\text{Sample} \to \text{Upstream [extract\_keypoints + dataset]} \to \text{Tensor A}$$
$$\text{Sample} \to \text{Signova [preprocess\_sequence]} \to \text{Tensor B}$$

| Sample Length ($T$) | Input Shape | Reference Shape | New Shape | Dtype | Max Absolute Difference | Mean Absolute Difference | Parity Status |
|---|---|---|---|---|---|---|---|
| **$T = 45$ (Short)** | `(45, 94, 4)` | `(1, 4, 94, 128)` | `(1, 4, 94, 128)` | `torch.float32` | **`0.00e+00`** | **`0.00e+00`** | Exact Bitwise Match |
| **$T = 128$ (Exact)** | `(128, 94, 4)` | `(1, 4, 94, 128)` | `(1, 4, 94, 128)` | `torch.float32` | **`0.00e+00`** | **`0.00e+00`** | Exact Bitwise Match |
| **$T = 200$ (Long)** | `(200, 94, 4)` | `(1, 4, 94, 128)` | `(1, 4, 94, 128)` | `torch.float32` | **`0.00e+00`** | **`0.00e+00`** | Exact Bitwise Match |

- **Task 5 Verdict:** **PASS**

---

## 4. Differences Found

| Aspect | Upstream ISLiM Pipeline | New Preprocessing Pipeline | Nature of Difference |
|---|---|---|---|
| **Memory Mutation** | Mutates numpy arrays in-place (`kp_seq[...] = ...`) | Default `copy=True` (returns new array) | Architectural refinement (thread safety) |
| **Input Validation** | None; unhandled crashes on NaNs, Infs, or wrong shapes | Strict validation raising `PreprocessingValidationError` | Safety & robustness feature |
| **Batching Support** | Single sample per item, batched in DataLoader | Native support for both 3D `(T, 94, 4)` and 4D `(B, T, 94, 4)` | Convenience for inference & batching |
| **Numerical Logic** | Exact equations for interpolation, normalization, and temporal linspace | Exact equations for interpolation, normalization, and temporal linspace | **Zero difference (100% bitwise parity)** |

---

## 5. Acceptability of Differences

Every identified difference represents an operational and robustness enhancement rather than a numerical divergence:
1. **Array Immutability (`copy=True`):** Acceptable and essential. In concurrent web environments (FastAPI/WebSockets), mutating caller buffers causes race conditions and data corruption.
2. **Input Contract Validation:** Acceptable and essential. Prevents corrupt camera frames or NaN vectors from causing silent gradient errors or unhandled crashes in PyTorch layers.
3. **Flexible Batching Dimension:** Acceptable. Allows single-sample webcam stream inference without requiring a PyTorch DataLoader wrapper.
4. **Numerical Parity:** Absolute difference is strictly **`0.00e+00`** across all tests. Zero mathematical drift was introduced.

---

## 6. Final Verdict

**FINAL VERDICT: PASS**

The new preprocessing pipeline achieves **100% bitwise parity ($\text{Max Diff} = 0.00\text{e}+00$)** with the original upstream ISLiM training and dataset pipeline while providing thread safety, contract validation, and single-stream inference support.

