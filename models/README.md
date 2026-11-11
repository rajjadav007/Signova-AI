# Signova AI - Model Weights & Checkpoints Directory

This directory stores locally downloaded pretrained checkpoints, configs, and label maps for Indian Sign Language recognition.

> **Note:** Binary model weights (`*.pt`, `*.ckpt`, `*.joblib`, `*.safetensors`, `*.task`) are excluded from Git version control via `.gitignore`.

## Directory Structure

```text
models/
├── checkpoints/       # Pretrained neural net checkpoints (.pt, .joblib)
├── assets/            # MediaPipe tasks (holistic_landmarker.task)
├── configs/           # Architecture and evaluation configs
├── labels/            # Class mappings (isolated_labels.json)
├── tokenizer/         # Tokenizer configs and vocab files
└── README.md
```

## Supported Models

1. **Isolated Sign Classifier (BiLSTM / Temporal CNN):**
   - Checkpoint: `models/checkpoints/isolated_model_best.pt`
   - Labels: `models/labels/isolated_labels.json`
   - Input: Resampled MediaPipe landmarks `(30, 282)`

2. **VSRS ISL Recognizer (Scikit-Learn MLP):**
   - Model artifact: `models/checkpoints/vsrs/model.joblib`
   - Input: Flattened landmark vector
