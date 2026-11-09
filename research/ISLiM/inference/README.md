# ISLiM Standalone Inference Application

The ISLiM Standalone Inference Application provides modular Python components and a command-line interface to translate Indian Sign Language (ISL) landmark sequences (`.npy`) into fluent English sentences using the pretrained ISLiM model.

## 1. Overview & Pipeline

The pipeline operates entirely on 94-landmark holistic sequences extracted from ISL video:

$$\text{Input .npy Keypoints } (T, 94, 4) \xrightarrow{\text{Validation}} \text{Interpolate / Normalize} \xrightarrow{\text{Resample}} (1, 4, 94, 128) \xrightarrow{\text{Visual Encoder}} \text{T5-Small Generation} \xrightarrow{\text{Decoded Text}}$$

- **Visual Encoder:** Spatial Conv1D + Transformer Encoder ($d_{\text{model}} = 512, N_{\text{layers}} = 4, N_{\text{heads}} = 8$) operating in full-frame mode (`num_query_tokens=0`).
- **Language Decoder:** Pretrained T5-small autoregressive cross-attention decoder.

## 2. Environment Requirements

- **Python:** 3.11+
- **PyTorch:** 2.5.1+cu121
- **Hardware:** NVIDIA GeForce RTX 2050 (or any CUDA-enabled GPU / CPU fallback)
- **Virtual Environment:** `research/ISLiM/.venv`

Activate the environment:
```powershell
.\research\ISLiM\.venv\Scripts\Activate.ps1
```

## 3. Checkpoint and Asset Locations

- **Model Checkpoint:** `research/ISLiM/checkpoints/ISLiM_full_posestitch_pre_processed.pt`
- **Tokenizer Directory:** `research/ISLiM/assets/t5-small/`

## 4. Command-Line Interface (CLI)

Run `standalone_inference.py` from the `research/ISLiM` directory:

### Basic Inference (Default: Beam Search on GPU/Auto)
```bash
python standalone_inference.py --input results/real_video_keypoints.npy
```

### Greedy Decoding ($B=1$)
```bash
python standalone_inference.py --input results/real_video_keypoints.npy --decoding greedy
```

### Beam Search with Custom Beams
```bash
python standalone_inference.py --input results/real_video_keypoints.npy --decoding beam --num_beams 4
```

### Force CPU Execution
```bash
python standalone_inference.py --input results/real_video_keypoints.npy --device cpu
```

### Save Output to JSON File
```bash
python standalone_inference.py --input results/real_video_keypoints.npy --output results/my_prediction.json
```

## 5. Python API Usage

The application is fully reusable from other Python modules or backend services. The model is loaded once upon predictor initialization and reused across all subsequent predictions.

```python
from pathlib import Path
from inference.predictor import ISLiMPredictor

# 1. Initialize predictor once
predictor = ISLiMPredictor(device="auto")

# 2. Predict from file or numpy array
result = predictor.predict(
    keypoints="results/real_video_keypoints.npy",
    decoding="beam",  # or 'greedy'
)

# 3. Access results
print("Prediction:", result["prediction"])
print("Latency:", result["inference_time_ms"], "ms")
print("Total Time:", result["total_time_ms"], "ms")
```

### Batch Inference
```python
import numpy as np

# Batched array shape: (B, T, 94, 4)
batch_kps = np.random.rand(2, 60, 94, 4).astype(np.float32)
batch_result = predictor.predict(batch_kps, decoding="beam")

print("Predictions:", batch_result["prediction"])  # List of strings
```

## 6. Greedy vs Beam Decoding

| Feature | Greedy Decoding (`--decoding greedy`) | Beam Search (`--decoding beam`) |
|---|---|---|
| **Beams ($B$)** | $B = 1$ | $B = 4$ (default) |
| **Generation Latency** | $\sim 250 - 310\text{ ms}$ | $\sim 420 - 1260\text{ ms}$ |
| **Repetition Penalty** | None | $1.5$ |
| **No-Repeat N-Gram** | None | $3$ |
| **Length Penalty** | None | $1.2$ |
| **Behavior** | Fast, greedy token selection; may produce `<unk>` | Fluent, globally optimized sequences |

## 7. Input File Format

The application accepts NumPy `.npy` files or NumPy ndarrays adhering to the ISLiM landmark layout:
- **Single Sequence:** `(T, 94, 4)` where $T \ge 1$ frames.
- **Batch Sequences:** `(B, T, 94, 4)` where $B \ge 1$ sequences.
- **Landmark Channels:** $4$ values per landmark: $[x, y, z, \text{visibility}]$.
- **Landmark Ordering:**
  - Indices 0–5: Upper body pose (6 landmarks)
  - Indices 6–26: Left hand (21 landmarks)
  - Indices 27–47: Right hand (21 landmarks)
  - Indices 48–93: Face mesh (46 landmarks)

*Note: Raw video files (.mp4, .avi) are not accepted directly. Video files must be pre-extracted to landmarks using MediaPipe Holistic.*

## 8. Output Format

Inference produces a structured JSON dictionary:

```json
{
  "success": true,
  "prediction": "but i cannot wait to stop and let me go",
  "token_ids": [0, 68, 3, 23, 1178, 1749, 12, 1190, 11, 752, 140, 281, 1],
  "device": "cuda:0",
  "decoding_strategy": "beam",
  "preprocessing_time_ms": 15.45,
  "inference_time_ms": 1262.76,
  "total_time_ms": 1278.21,
  "input_shape": [125, 94, 4],
  "model_input_shape": [1, 4, 94, 128],
  "model": "ISLiM",
  "accuracy_verified": false,
  "note": "Translation accuracy is unverified without ground-truth subtitles/labels."
}
```

## 9. Known Limitations

1. **Fixed Temporal Window ($T=128$):** Input sequences are resampled or padded to 128 frames.
2. **Missing Ground Truth:** In the absence of aligned subtitle reference labels, translation accuracy cannot be verified automatically.
3. **Landmark Quality Dependency:** Missing hand landmarks exceeding 5 frames degrade visual encoder representations.

## 10. Troubleshooting

- **`InvalidInputError: expected 94 landmarks`:** The input file has the wrong landmark layout (e.g. MediaPipe full 543 landmarks or pose 33 landmarks). Map the indices to the 94 ISLiM indices.
- **`ModelLoadingError: Checkpoint file does not exist`:** Check that `research/ISLiM/checkpoints/ISLiM_full_posestitch_pre_processed.pt` is present.
- **`CUDA out of memory`:** The application requires ~315 MB VRAM. If another process is exhausting VRAM, run with `--device cpu`.
