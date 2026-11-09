# ISLiM Input Data Preprocessing and Validation Report (Part 1.6)

**Document:** `research/ISLiM/INPUT_PREPROCESSING_REPORT.md`  
**Execution Date:** 2026-11-09  
**Target Repository:** `research/ISLiM/`  
**Git Branch:** `preparation`  
**Primary Checkpoint:** `research/ISLiM/checkpoints/ISLiM_full_posestitch_pre_processed.pt`  
**Status:** Implemented, Tested, Verified & Documented  
**Inspector:** Signova AI Engineering  

---

## 1. Original Preprocessing Analysis

Inspection of the original upstream ISLiM repository (`research/ISLiM/`) revealed the exact data preprocessing lifecycle:

1. **Extraction (`scripts/preprocess/extract_keypoints.py`):**
   - MediaPipe Holistic model (`model_complexity=1, smooth_landmarks=True, refine_face_landmarks=False`).
   - Extracts 94 keypoints per frame across Body, Hands, Lips, Eyes, and Eyebrows.
   - Formats each keypoint as four channels: `[x, y, z, visibility]`.
   - Linear temporal interpolation across missing gaps ($\le 5$ consecutive frames).
   - Saved as `.npy` array with shape `(T, 94, 4)` (`float16` or `float32`).

2. **Dataset Loading & Preprocessing (`src/data/dataset.py` -> `_normalize_keypoints`):**
   - Reads `.npy` file.
   - Spatial Min-Max Normalization: Independent scaling per axis for $x, y, z$ to $[0, 1]$ if range $> 1e-8$. Visibility channel 3 is untouched.
   - Temporal Resampling to 128 Frames:
     - If $T > 128$: Uniform downsampling via `torch.linspace(0, T - 1, 128).long()`.
     - If $T < 128$: Temporal zero-padding at the sequence end `(128 - T, 94, 4)`.
   - Transpose: Permutes from `(T, 94, 4)` to `(4, 94, 128)` (`(C, K, T)`).
   - Batching: `collate_fn` stacks samples into `(B, 4, 94, 128)`.

3. **Encoder Ingestion (`src/islim/encoder.py` -> `ISLiMEncoder._normalize_frames`):**
   - Detects if `keypoints.shape[1] == 4` and permutes to `(B, 128, 94, 4)`.
   - Idempotently verifies temporal length $T=128$.
   - Flattens spatial-coordinate dimensions $94 \times 4 = 376$ and projects into the visual transformer.

---

## 2. Landmark Index Mapping

ISLiM strictly enforces 94 keypoints structured across six anatomical groups:

| Group Name | Keypoint Count | Local Indices | MediaPipe Source | Coordinate Channels | Visibility Rule |
|---|---|---|---|---|---|
| **Pose / Body** | 6 | 0–5 | PoseLandmark (11, 12, 13, 14, 23, 24) | `[x, y, z, vis]` | From MediaPipe Pose `lm.visibility` |
| **Left Hand** | 21 | 6–26 | LeftHandLandmark (0–20) | `[x, y, z, 1.0]` | Explicitly 1.0 when detected |
| **Right Hand** | 21 | 27–47 | RightHandLandmark (0–20) | `[x, y, z, 1.0]` | Explicitly 1.0 when detected |
| **Lips** | 20 | 48–67 | FaceMesh Lips (20 specific indices) | `[x, y, z, vis]` | `1.0 if lm.z > -0.5 else 0.5` |
| **Eyes** | 16 | 68–83 | FaceMesh Eyes (16 specific indices) | `[x, y, z, vis]` | `1.0 if lm.z > -0.5 else 0.5` |
| **Eyebrows** | 10 | 84–93 | FaceMesh Eyebrows (10 specific indices) | `[x, y, z, vis]` | `1.0 if lm.z > -0.5 else 0.5` |
| **Total** | **94** | **0–93** | **MediaPipe Holistic** | **4 values / point** | **Total input dimension: 376** |

### Face Mesh Index Specifics
- **Lips (20):** `[61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 409, 270, 95, 88, 178, 87, 14, 78, 308]`
- **Eyes (16):** `[33, 133, 160, 158, 153, 144, 145, 246, 362, 263, 387, 385, 380, 373, 374, 249]`
- **Eyebrows (10):** `[107, 66, 105, 63, 70, 336, 296, 334, 293, 300]`

Implemented in: `research/ISLiM/preprocessing/landmark_mapping.py`. Includes helper `extract_holistic_frame(results)` for MediaPipe Holistic integration.

---

## 3. Input Data Contract

The preprocessing pipeline specifies the following interface contract:

- **Raw Input:** Sequence of landmark frames:
  - Format: NumPy array of shape `(T, 94, 4)` or batched `(B, T, 94, 4)`.
  - Temporal length $T$: Variable ($T \ge 1$).
  - Coordinate range: Unnormalized pixel/normalized camera coordinates.
  - Channels: `0: x`, `1: y`, `2: z`, `3: visibility`.
- **Preprocessed Output:**
  - Format: `torch.FloatTensor` of shape `(B, 4, 94, 128)` (or `(4, 94, 128)` if `add_batch_dim=False`).
  - Data Type: `torch.float32`.
  - Coordinate range: Spatial coordinates $(x, y, z) \in [0.0, 1.0]$.
  - Visibility range: $[0.0, 1.0]$.
  - Temporal dimension: Exactly 128 frames.
  - Channel ordering: Channel-first `(B, C, K, T)`.

---

## 4. Landmark Validation

Implemented in: `research/ISLiM/preprocessing/validation.py`.

- **Checks:**
  1. Non-empty array (`size > 0`, $T \ge 1$).
  2. Dimensionality: 3D sequence `(T, 94, 4)` or 4D batch `(B, T, 94, 4)`.
  3. Landmark count: Exactly 94 at axis -2.
  4. Channel count: Exactly 4 at axis -1.
  5. Numeric validity: Strict finite check (zero NaNs, zero Infs).
  6. Visibility bounds: Values within $[0.0, 1.05]$.
- **Error Handling:**
  - Non-throwing check: `validate_sequence(arr) -> (bool, Optional[str])`.
  - Throwing check: `assert_valid_sequence(arr) -> np.ndarray` raises `PreprocessingValidationError(ValueError)` with informative diagnostic messages.

---

## 5. Missing Landmark Handling

Implemented in: `research/ISLiM/preprocessing/interpolation.py`.

Faithfully reproduces upstream `scripts/preprocess/extract_keypoints.py`:
- Valid frames identified where $\text{visibility} > 0.5$.
- **Interior Gaps ($1 < \text{gap} \le 5$):** Linearly interpolated across time:
  $$\alpha = \frac{j}{\text{gap}}, \quad \mathbf{k}_{a+j} = (1 - \alpha)\mathbf{k}_a + \alpha\mathbf{k}_b$$
- **Large Gaps ($\text{gap} > 5$):** Not interpolated; remain set to `0.0`.
- **Sequence Boundaries:** Frames before first valid frame clamp to first valid frame; frames after last valid frame clamp to last valid frame.
- **Missing Across Sequence:** If a landmark is never detected across all frames, it remains all `0.0`.
- **Copy Semantics:** Returns a clean copy (`copy=True` by default) to prevent caller side-effects.

---

## 6. Coordinate Normalization

Implemented in: `research/ISLiM/preprocessing/normalization.py`.

Faithfully reproduces upstream `src/data/dataset.py`:
- Independent per-sequence, per-channel min-max normalization for $x, y, z$:
  $$\hat{c} = \frac{c - c_{\min}}{c_{\max} - c_{\min}}$$
- **Constant Coordinate Handling:** If $c_{\max} - c_{\min} \le 10^{-8}$ (e.g. constant channel or all zeros), sets channel to $c - c_{\min} = 0.0$ to prevent division by zero.
- **Visibility Channel:** Preserved unchanged without scaling.

---

## 7. Temporal Processing

Implemented in: `research/ISLiM/preprocessing/temporal_processing.py`.

Faithfully reproduces upstream `src/data/dataset.py`:
- Target sequence length: `128` frames.
- **Shorter sequences ($T < 128$):** Zero-padded at the end:
  $$\text{padding} = \text{zeros}((128 - T, 94, 4))$$
- **Longer sequences ($T > 128$):** Uniformly downsampled across time using PyTorch's deterministic linspace indexing:
  $$\text{indices} = \text{torch.linspace}(0, T - 1, 128).\text{long}()$$
- **Exact sequences ($T = 128$):** Passed through unchanged.
- Supports both NumPy arrays and PyTorch tensors.

---

## 8. Tensor Conversion

Implemented in: `research/ISLiM/preprocessing/tensor_conversion.py`.

Converts normalized array `(128, 94, 4)` into the official model tensor:
- Permutes axes from $(T=128, K=94, C=4)$ to $(C=4, K=94, T=128)$.
- Prepend batch dimension: `(1, 4, 94, 128)`.
- Enforces `torch.float32`.
- Direct GPU placement support (`device="cuda"`).

Unified pipeline facade:
`research/ISLiM/preprocessing/__init__.py` -> `preprocess_sequence(raw_sequence, add_batch_dim=True, device=None)`.

---

## 9. Final Model Input Shape & Encoder Verification

The preprocessed tensor was integrated and verified against the official `ISLiMModel` loaded with checkpoint `ISLiM_full_posestitch_pre_processed.pt` (`num_query_tokens: 0`):

| Test Case | Input Raw Shape | Preprocessed Tensor Shape | Visual Encoder Output Shape | Temporal Preservation | Status |
|---|---|---|---|---|---|
| **Short Sequence** ($T=45 < 128$) | `(45, 94, 4)` | `(1, 4, 94, 128)` | `(1, 128, 512)` | 128 / 128 (100%) | **Passed** |
| **Exact Sequence** ($T=128$) | `(128, 94, 4)` | `(1, 4, 94, 128)` | `(1, 128, 512)` | 128 / 128 (100%) | **Passed** |
| **Long Sequence** ($T=210 > 128$) | `(210, 94, 4)` | `(1, 4, 94, 128)` | `(1, 128, 512)` | 128 / 128 (100%) | **Passed** |
| **Batched Sequences** ($B=2, T=75$) | `(2, 75, 94, 4)` | `(2, 4, 94, 128)` | `(2, 128, 512)` | 128 / 128 (100%) | **Passed** |
| **GPU Execution** (CUDA 0) | `(90, 94, 4)` | `(1, 4, 94, 128)` | `(1, 128, 512)` | 128 / 128 (100%) | **Passed** |

All 128 temporal tokens are preserved without query token slicing and directly condition T5-small's cross-attention decoder ($d_{\text{model}} = 512$).

---

## 10. Automated Test Results

Automated unit tests were executed using standard Python `unittest`:

```text
Ran 38 tests in 0.035s
STATUS: OK (38 passed, 0 failed, 0 errors)
```

### Test Suite Breakdown
1. `test_landmark_mapping.py` (5 tests): Group counts (94 total), landmark group lookup, face landmark ranges, mock MediaPipe Holistic extraction, None-safe fallback.
2. `test_validation.py` (9 tests): Valid 3D/4D inputs, empty sequence rejection, invalid dimensions, wrong landmark counts (75 vs 94), missing channels, NaN rejection, Inf rejection, visibility range bounds.
3. `test_interpolation.py` (7 tests): Single missing frame interpolation, 5-frame gap boundary, $>5$ frame gap rejection (zeroed), boundary extrapolation, completely missing landmarks, copy semantics, batched sequences.
4. `test_normalization.py` (5 tests): Independent channel min-max scaling to $[0, 1]$, constant coordinate handling, epsilon threshold ($10^{-8}$), untouched visibility, batched sample independence.
5. `test_temporal_processing.py` (5 tests): Padding shorter sequences with end zeros, exact length pass-through, linspace downsampling longer sequences, PyTorch tensor support, batched temporal resizing.
6. `test_tensor_conversion.py` (7 tests): Channel permute to `(1, 4, 94, 128)`, unbatched `(4, 94, 128)`, batched `(B, 4, 94, 128)`, end-to-end short/long/batched pipeline execution, invalid sequence rejection.

---

## 11. Differences from Original Implementation

| Component | Upstream ISLiM | Signova Preprocessing Pipeline | Reason |
|---|---|---|---|
| **Pipeline Modularity** | Scattered across `scripts/preprocess/extract_keypoints.py` and `src/data/dataset.py` | Unified modular package under `research/ISLiM/preprocessing/` | High reusability for FastAPI backend and live webcam inference |
| **Memory Mutation** | Upstream mutated arrays in-place (`kp_seq[...] = ...`) | Functions return explicit copies (`copy=True`) | Thread-safe, side-effect free inference in concurrent environments |
| **Input Validation** | None; silent crashes on NaN or wrong shapes | Comprehensive contract validation with informative exceptions | Safety barrier against malformed video frames and corrupted data |
| **Batching Support** | Single sample per `__getitem__`, batched via DataLoader `collate_fn` | Native 3D `(T, 94, 4)` and 4D `(B, T, 94, 4)` support | Allows both single-stream web inference and batched evaluation |

---

## 12. Pending Issues

None. The preprocessing pipeline is fully verified, passes all automated tests, and seamlessly feeds into the loaded `ISLiMModel` producing the exact expected `(B, 128, 512)` representations.

---

## 13. Conclusion

Part 1.6 is complete. The preprocessing pipeline accurately transforms arbitrary raw landmark sequences into the exact format required by the official ISLiM architecture without altering the upstream codebase or introducing incompatible assumptions. The codebase is prepared for model inference testing in Part 1.7.

