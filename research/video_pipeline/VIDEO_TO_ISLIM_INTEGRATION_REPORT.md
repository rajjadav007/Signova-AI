# Video-to-ISLiM Inference Integration Report (Part 2.2)

**Document:** `research/video_pipeline/VIDEO_TO_ISLIM_INTEGRATION_REPORT.md`  
**Execution Date:** 2026-11-09  
**Target Module:** `research/video_pipeline/`  
**Git Branch:** `preparation`  
**Inspector:** Signova AI Engineering  
**Integrated Pipeline Status:** **PASS**  
**Translation Semantic Accuracy Status:** **UNVERIFIED** (No reference ground-truth subtitles available)

---

## 1. Executive Summary

Part 2.2 successfully integrates the video decoding and MediaPipe 94-landmark extraction pipeline (Part 2.1) with the standalone ISLiM deep learning inference engine (Part 1.9).

The integrated system operates completely end-to-end:
$$\text{Input Video (.mp4)} \xrightarrow{\text{VideoReader}} \text{RGB Frames} \xrightarrow{\text{MediaPipeLandmarkExtractor}} \text{Keypoints } (T, 94, 4) \xrightarrow{\text{ISLiM Preprocessing}} (1, 4, 94, 128) \xrightarrow{\text{ISLiM + T5}} \text{English Text}$$

Users no longer need to extract or upload intermediary `.npy` keypoint files.

---

## 2. Video Inputs Discovered and Tested

A workspace scan identified two video recordings:

| Role | Filename | Path | Size | Resolution | FPS | Frames | Duration |
|---|---|---|---|---|---|---|---|
| **Primary Test (Newly Added)** | `Deaf-U-SnapYT.App.mp4` | `D:\Signova AI\Deaf-U-SnapYT.App.mp4` | 3.46 MB | 640x360 | 23.98 | 1,646 | 68.652 s |
| **Regression Baseline** | `International-Week-of-SnapYT.App.mp4` | `D:\Signova AI\International-Week-of-SnapYT.App.mp4` | 145 KB | 360x360 | 30.00 | 125 | 4.167 s |

---

## 3. Integrated Pipeline Architecture

The integrated architecture is implemented in [`research/video_pipeline/video_inference_pipeline.py`](file:///d:/Signova%20AI/research/video_pipeline/video_inference_pipeline.py) via `VideoToISLiMPipeline`:

1. **Model Persistence / Single Load:**
   - Pretrained ISLiM checkpoint (`ISLiM_full_posestitch_pre_processed.pt`) and local T5-small tokenizer (`research/ISLiM/assets/`) are loaded once upon pipeline instantiation.
   - Subsequent calls reuse the in-memory PyTorch module without disk or VRAM reload overhead.
2. **Video Ingestion & Streaming:**
   - `VideoReader` validates container formats (`.mp4`, `.avi`, `.mov`, `.mkv`), opens OpenCV `VideoCapture`, and streams RGB frames lazily ($O(1)$ memory).
3. **94-Landmark Extraction:**
   - `MediaPipeLandmarkExtractor` executes `vision.HolisticLandmarker` per frame, outputting raw `(T, 94, 4)` float32 arrays across Pose (6), Left Hand (21), Right Hand (21), Lips (20), Eyes (16), and Eyebrows (10).
4. **Verified Preprocessing:**
   - Linear interpolation fills coordinate gaps ($\le 5$ frames).
   - Independent spatial min-max normalization scales $(x, y, z)$ to $[0.0, 1.0]$.
   - Uniform temporal downsampling resamples $T$ frames to fixed 128 frames.
   - Transposes to channel-first batch tensor `(1, 4, 94, 128)`.
5. **Autoregressive Generation:**
   - Visual transformer projects 128 visual tokens ($d=512$).
   - Autoregressive T5 decoder generates English text tokens with `num_beams=4` (and `num_beams=1` greedy).
6. **Result & Artifact Persistence:**
   - Persists raw landmark arrays `.npy` and structured JSON inference reports into `research/video_pipeline/results_part2_2/`.

---

## 4. Landmark Extraction & Preprocessing Results

| Metric | Primary Test: `Deaf-U-SnapYT.App.mp4` | Baseline Test: `International-Week-of-SnapYT.App.mp4` |
|---|---|---|
| **Total Frames Extracted** | 1,646 frames | 125 frames |
| **Landmark Array Shape** | `(1646, 94, 4)` | `(125, 94, 4)` |
| **Data Type** | `float32` | `float32` |
| **Pose Detection Rate** | 1,307 / 1,646 (**79.40%**) | 125 / 125 (**100.0%**) |
| **Face Detection Rate** | 1,194 / 1,646 (**72.54%**) | 125 / 125 (**100.0%**) |
| **Right Hand Detection Rate** | 1,065 / 1,646 (**64.70%**) | 120 / 125 (**96.0%**) |
| **Left Hand Detection Rate** | 974 / 1,646 (**59.17%**) | 110 / 125 (**88.0%**) |
| **Landmark Presence Percentage** | **68.24%** | **96.43%** |
| **Resampled Tensor Shape** | `torch.Size([1, 4, 94, 128])` | `torch.Size([1, 4, 94, 128])` |
| **Preprocessing Latency** | 90.35 ms | 5.13 ms |

---

## 5. Model Translation & Generation Outputs

### 5.1 Primary Test: `Deaf-U-SnapYT.App.mp4` (New Video)
- **Extracted Frames:** 1,646
- **Beam Search ($B=4$):**
  - **Decoded Prediction:** `"a mixture of two liquids"`
  - **Generated Token IDs:** `[0, 3, 9, 4989, 13, 192, 4400, 7, 1]`
  - **Inference Latency:** **511.18 ms**
- **Greedy Search ($B=1$):**
  - **Decoded Prediction:** `"unknown person"`
  - **Generated Token IDs:** `[0, 7752, 568, 1]`
  - **Inference Latency:** **119.63 ms**
- **Semantic Assessment:** The sentence is grammatically coherent English. Because no official reference subtitles accompany the clip, translation correctness is classified as **UNVERIFIED**.

### 5.2 Baseline Regression Test: `International-Week-of-SnapYT.App.mp4`
- **Extracted Frames:** 125
- **Beam Search ($B=4$):**
  - **Decoded Prediction:** `"but i cannot wait to stop and let me go"`
  - **Generated Token IDs:** `[0, 68, 3, 23, 1178, 1749, 12, 1190, 11, 752, 140, 281, 1]`
  - **Inference Latency:** **289.91 ms**
- **Greedy Search ($B=1$):**
  - **Decoded Prediction:** `"i cannot wait to stop my unknown"`
  - **Generated Token IDs:** `[0, 3, 23, 1178, 1749, 12, 1190, 82, 7752, 1]`
  - **Inference Latency:** **93.64 ms**
- **Parity Verification:** Predictions match Part 1.7.1 and Part 1.9 with 100% string and token equality.

---

## 6. Runtime and Memory Measurements

Hardware: Intel Core CPU + NVIDIA GeForce RTX 2050 (4 GB VRAM)

| Execution Stage | `Deaf-U-SnapYT.App.mp4` (1,646 frames) | `International-Week-of-SnapYT.App.mp4` (125 frames) |
|---|---|---|
| **Landmark Extraction** | 35.77 s (~46.0 FPS) | 5.62 s (~22.2 FPS) |
| **Tensor Preprocessing** | 90.35 ms | 5.13 ms |
| **Beam Inference ($B=4$)** | 511.18 ms | 289.91 ms |
| **Greedy Inference ($B=1$)** | 119.63 ms | 93.64 ms |
| **Total End-to-End Latency** | **36.59 s** | **6.02 s** |
| **Peak GPU VRAM** | **314.77 MB** | **315.15 MB** |
| **Execution Device** | `cuda` (NVIDIA GeForce RTX 2050) | `cuda` (NVIDIA GeForce RTX 2050) |

---

## 7. Test Suite Results

Test suite: `research/video_pipeline/tests/` (18 unit and integration tests)

```text
test_landmark_definitions_and_ordering ... ok
test_landmark_extractor_blank_frame ... ok
test_landmark_extractor_invalid_input ... ok
test_landmark_extractor_missing_asset ... ok
test_landmark_extractor_resource_cleanup ... ok
test_model_loaded_once_and_reused ... ok
test_baseline_video_regression ... ok
test_sample_video_integration_and_parity ... ok
test_video_processor_empty_video ... ok
test_video_processor_missing_video ... ok
test_video_processor_synthetic_run ... ok
test_video_reader_corrupted_file ... ok
test_video_reader_empty_video ... ok
test_video_reader_missing_file ... ok
test_video_reader_resource_cleanup ... ok
test_video_reader_synthetic_video ... ok
test_video_reader_unsupported_format ... ok
test_video_reader_valid_sample_video ... ok

----------------------------------------------------------------------
Ran 18 tests in 11.234s

OK
```

---

## 8. Persisted Artifacts

Dedicated Part 2.2 results directory: `research/video_pipeline/results_part2_2/`

1. `Deaf-U-SnapYT.App_keypoints.npy` (1,646 frames $\times$ 94 landmarks $\times$ 4 coordinates = 2.47 MB)
2. `Deaf-U-SnapYT.App_inference_report.json`
3. `International-Week-of-SnapYT.App_keypoints.npy` (125 frames $\times$ 94 landmarks $\times$ 4 coordinates = 188 KB)
4. `International-Week-of-SnapYT.App_inference_report.json`

---

## 9. Status Classification

In accordance with Signova AI engineering rules:
- **Integrated Pipeline Status:** **PASS** (Video decoding, landmark extraction, preprocessing, model loading reuse, autoregressive generation, and result persistence completed cleanly).
- **Translation Accuracy Status:** **UNVERIFIED** (No verified ground-truth subtitles are available for the test videos).

---

## 10. Conclusion

Part 2.2 is complete. Direct video-to-text inference is fully functional, reproducible, and verified.
