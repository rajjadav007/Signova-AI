# Signova AI Video Input and Landmark Extraction Pipeline Report (Part 2.1)

**Document:** `research/video_pipeline/VIDEO_PIPELINE_REPORT.md`  
**Execution Date:** 2026-11-09  
**Target Module:** `research/video_pipeline/`  
**Git Branch:** `preparation`  
**Test Video:** `International-Week-of-SnapYT.App.mp4`  
**Inspector:** Signova AI Engineering  
**Final Verdict:** **PASS**

---

## 1. Implementation Summary

Part 2.1 implements the standalone, modular video input and landmark extraction pipeline for Signova AI.

The pipeline decodes video containers (`.mp4`, `.avi`, `.mov`, `.mkv`), streams RGB frames via a lazy generator for $O(1)$ memory usage, extracts 94 MediaPipe Holistic landmarks per frame strictly conforming to the ISLiM landmark layout, and persists the raw landmark sequence as a standard NumPy `.npy` array with accompanying metadata JSON report.

### Pipeline Workflow
$$\text{Video File (.mp4, .avi, .mov, .mkv)} \xrightarrow{\text{VideoReader (OpenCV streaming)}} \text{RGB Frames} \xrightarrow{\text{MediaPipeLandmarkExtractor}} \text{Landmarks } (T, 94, 4) \xrightarrow{\text{OutputHandler}} \text{.npy } + \text{ .json report}$$

---

## 2. Files Created or Modified

### Files Created
- `research/video_pipeline/__init__.py`: Package entry point exposing configuration, exceptions, classes, and utilities.
- `research/video_pipeline/config.py`: Centralized configuration, MediaPipe asset path resolution, supported formats, and 94-landmark index/slice definitions.
- `research/video_pipeline/exceptions.py`: Custom typed exception hierarchy (`VideoPipelineError`, `VideoNotFoundError`, `UnsupportedVideoFormatError`, `CorruptedVideoError`, `EmptyVideoError`, `LandmarkExtractionError`, `ModelAssetNotFoundError`).
- `research/video_pipeline/video_reader.py`: Robust OpenCV video reader with input validation, metadata extraction, error detection, streaming generator, and safe resource cleanup.
- `research/video_pipeline/landmark_extractor.py`: MediaPipe HolisticLandmarker wrapper extracting exact 94 landmarks `(x, y, z, visibility)` per frame with proper fallback and cleanup.
- `research/video_pipeline/output_handler.py`: Validated serialization and deserialization for `.npy` (`allow_pickle=False`) and structured JSON extraction reports.
- `research/video_pipeline/video_processor.py`: End-to-end coordinator running decoding, landmark extraction, timing, statistics calculation, and disk persistence.
- `research/video_pipeline/tests/__init__.py`: Test suite package definition.
- `research/video_pipeline/tests/test_video_reader.py`: Unit tests for video format validation, missing files, 0-byte empty files, corrupted streams, and resource cleanup.
- `research/video_pipeline/tests/test_landmark_extractor.py`: Unit tests for landmark indices, group slice ranges, blank frame extraction, invalid input shapes, and cleanup.
- `research/video_pipeline/tests/test_video_processor.py`: Unit tests for synthetic video processing, output persistence, metrics calculation, and exception propagation.
- `research/video_pipeline/tests/test_video_integration.py`: End-to-end integration test verifying extraction on `International-Week-of-SnapYT.App.mp4` and exact numerical parity against Phase 1.7.1 baseline.
- `research/video_pipeline/results/.gitkeep`: Results directory placeholder.
- `research/video_pipeline/results/International-Week-of-SnapYT.App_keypoints.npy`: Persisted keypoint sequence `(125, 94, 4)` float32.
- `research/video_pipeline/results/International-Week-of-SnapYT.App_extraction_report.json`: Persisted extraction report.
- `research/video_pipeline/VIDEO_PIPELINE_REPORT.md`: This comprehensive verification report.

### Files Modified
- `docs/PROGRESS_TRACKER.md`: Updated Part 2.1 status to Completed with verification details.

---

## 3. Video Input Validation Results

The `VideoReader` was subjected to strict boundary and edge case verification:

| Scenario / Test Case | Input Condition | Expected Behavior | Actual Behavior | Result |
|---|---|---|---|---|
| **Valid MP4** | `International-Week-of-SnapYT.App.mp4` | Parse width=360, height=360, fps=30.0, frame_count=125 | Exact metadata parsed; 125 RGB frames streamed | **PASS** |
| **Missing File** | `non_existent.mp4` | Raise `VideoNotFoundError` | Raised `VideoNotFoundError` with descriptive message | **PASS** |
| **Unsupported Extension** | `sample.txt` | Raise `UnsupportedVideoFormatError` | Raised `UnsupportedVideoFormatError` with allowed formats list | **PASS** |
| **0-Byte Empty File** | `empty.mp4` (0 bytes) | Raise `EmptyVideoError` | Raised `EmptyVideoError` | **PASS** |
| **Corrupted Video Stream** | Non-video bytes in `.mp4` file | Raise `CorruptedVideoError` or `EmptyVideoError` | OpenCV cannot open; raised `CorruptedVideoError` | **PASS** |
| **Resource Cleanup** | Context manager or explicit `release()` | Release OpenCV `VideoCapture` object | `_cap` set to `None`, handle released | **PASS** |

---

## 4. MediaPipe Extraction Details

- **Model Asset Used:** `research/ISLiM/assets/holistic_landmarker.task` (10.3 MB binary bundle).
- **MediaPipe Tasks Vision API:** `vision.HolisticLandmarker` running under `RunningMode.IMAGE`.
- **Confidence Thresholds:**
  - `min_face_detection_confidence: 0.5`
  - `min_pose_detection_confidence: 0.5`
  - `min_hand_landmarks_confidence: 0.5`
- **Output Channel Encoding:**
  - Channel 0: $x$ coordinate (normalized horizontal coordinate $[0.0, 1.0]$)
  - Channel 1: $y$ coordinate (normalized vertical coordinate $[0.0, 1.0]$)
  - Channel 2: $z$ coordinate (relative landmark depth)
  - Channel 3: Visibility score $[0.0, 1.0]$
- **Missing Landmark Convention:**
  - If a anatomical subsystem (e.g., left hand) is not detected in a frame, all corresponding keypoints remain preallocated zeros `[0.0, 0.0, 0.0, 0.0]` (visibility = 0.0).

---

## 5. Landmark Ordering Verification

The landmark indices and slice layout strictly replicate the verified Phase 1 ISLiM mapping:

| Landmark Subsystem | Landmark Count | Array Slice Range | MediaPipe Source Indices | Coordinate Channels | Visibility Rule |
|---|---:|---|---|---|---|
| **Pose / Upper Body** | 6 | `[0:6]` | MediaPipe Pose: `[11, 12, 13, 14, 23, 24]` | `[x, y, z, vis]` | From MediaPipe `lm.visibility` |
| **Left Hand** | 21 | `[6:27]` | MediaPipe Left Hand joints: `0–20` | `[x, y, z, 1.0]` | Explicitly 1.0 when detected |
| **Right Hand** | 21 | `[27:48]` | MediaPipe Right Hand joints: `0–20` | `[x, y, z, 1.0]` | Explicitly 1.0 when detected |
| **Face Lips** | 20 | `[48:68]` | Face Mesh 20 specific lip points | `[x, y, z, vis]` | `1.0 if lm.z > -0.5 else 0.5` |
| **Face Eyes** | 16 | `[68:84]` | Face Mesh 16 specific eye points | `[x, y, z, vis]` | `1.0 if lm.z > -0.5 else 0.5` |
| **Face Eyebrows** | 10 | `[84:94]` | Face Mesh 10 specific eyebrow points | `[x, y, z, vis]` | `1.0 if lm.z > -0.5 else 0.5` |
| **Total Keypoints** | **94** | `[0:94]` | Full Holistic Landmarker | **4 values / point** | **Frame shape: (94, 4)** |

---

## 6. Output Shape and Data Type

The pipeline enforces strict data contracts:
- **Array Shape:** Exactly `(T, 94, 4)` where $T = 125$ for the sample video.
- **Array Data Type:** `numpy.float32`.
- **Serialization:** Saved via `np.save(path, keypoints, allow_pickle=False)`.
- **Integrity Check:** Successfully reloaded via `np.load(path, allow_pickle=False)` without loss of precision or modification of shape/dtype.

---

## 7. Sample Video Test Results

Processed video: `International-Week-of-SnapYT.App.mp4`

| Property | Value | Notes |
|---|---|---|
| **Container / Resolution** | MP4 (`360x360`) | Square aspect ratio, standard mobile framing |
| **Total Frames** | 125 | Matches physical video duration (4.167 s @ 30 FPS) |
| **Processed Frames** | 125 | Zero frames dropped or skipped |
| **Extracted Sequence Shape** | `(125, 94, 4)` | Verified float32 |
| **Pose Detection** | 125 / 125 (**100.0%**) | Upper torso tracked across every frame |
| **Face Detection** | 125 / 125 (**100.0%**) | Face mesh tracked across every frame |
| **Right Hand Detection** | 120 / 125 (**96.0%**) | Active signing hand |
| **Left Hand Detection** | 110 / 125 (**88.0%**) | Secondary hand dropped only during rest |
| **Total Landmark Instances** | 11,750 ($125 \times 94$) | Complete coordinate matrix |
| **Present Landmarks** | 11,330 (**96.43%**) | Landmarks with visibility > 0.0 |
| **Missing Landmarks** | 420 (**3.57%**) | Left/Right hand occlusion gaps |
| **Saved Keypoints Artifact** | `research/video_pipeline/results/International-Week-of-SnapYT.App_keypoints.npy` | 188,128 bytes |
| **Saved Report Artifact** | `research/video_pipeline/results/International-Week-of-SnapYT.App_extraction_report.json` | Formatted JSON |

### Numerical Parity with Phase 1.7.1 Baseline
Extracted keypoints were compared against `research/ISLiM/results/real_video_keypoints.npy`:
- **Max Absolute Difference:** `0.0`
- **Mean Absolute Difference:** `0.0`
- **Exact Boolean Equality (`np.array_equal`):** `True`
- **Verdict:** Exact numerical parity confirmed.

---

## 8. Performance Measurements

Measurements captured on host hardware (Intel Core CPU + NVIDIA GeForce RTX 2050):

| Metric | Measurement |
|---|---|
| **Total Processing Duration** | 10.44 s |
| **Landmark Extraction Duration** | 10.18 s |
| **Average Time per Frame** | 81.43 ms |
| **Processing Throughput (FPS)** | 12.28 FPS |
| **Peak Host Memory Footprint** | Minimal (Generator streams single frame at a time, avoiding uncompressed frame buffer in RAM) |

---

## 9. Test Suite Execution Results

All 16 unit and integration tests executed using Python's standard `unittest` framework:

```text
test_landmark_definitions_and_ordering ... ok
test_landmark_extractor_blank_frame ... ok
test_landmark_extractor_invalid_input ... ok
test_landmark_extractor_missing_asset ... ok
test_landmark_extractor_resource_cleanup ... ok
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
Ran 16 tests in 6.625s

OK
```

---

## 10. Known Limitations

1. **Static Video Files Only:** This module processes offline video files (`.mp4`, `.avi`, `.mov`, `.mkv`). Real-time webcam streaming and WebRTC/WebSocket ingestion will be added in Phase 3.
2. **Preprocessing & Model Decoupling:** In strict accordance with Part 2.1 specifications, temporal interpolation, min-max spatial normalization to $[0, 1]$, and temporal resampling to 128 frames are not applied in this stage; they remain part of the downstream ISLiM preprocessing pipeline.
3. **Hardware Acceleration:** MediaPipe Tasks currently operates on CPU/XNNPACK backend for landmark detection on Windows.

---

## 11. Final Verdict

**Verdict:** **PASS**

All Part 2.1 completion criteria have been met:
- Local video files can be opened and decoded frame-by-frame.
- 94 MediaPipe Holistic landmarks extracted with exact Phase 1 ordering and visibility rules.
- Output array has shape `(T, 94, 4)` and `float32` dtype.
- Saved `.npy` (`allow_pickle=False`) and `.json` artifacts reload cleanly.
- Sample video `International-Week-of-SnapYT.App.mp4` processed with 100% numerical parity to Phase 1.7.1 baseline.
- All 16 unit and integration tests pass cleanly.
