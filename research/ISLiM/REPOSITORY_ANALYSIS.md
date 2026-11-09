# ISLiM Repository Analysis Report

**Analysis Date:** 2026-11-09  
**Target Repository:** [ahmedshoaib/ISLiM](https://github.com/ahmedshoaib/ISLiM)  
**Cloned Location:** `research/ISLiM/`  
**Git Commit:** `ec50943b928c9db32b0a9bd30d74b7eb43d81a5d`  
**Inspector:** Signova AI Engineering  

---

## 1. Executive Summary

ISLiM (**I**ndian **S**ign **L**anguage **i**n **M**otion / Keypoint-based Sign Language Translation) is a compact, gloss-free deep learning system designed to translate continuous Indian Sign Language (ISL) keypoint sequences directly into English sentences.

Unlike traditional two-stage translation pipelines that rely on intermediate symbolic glosses, ISLiM maps raw skeletal keypoint streams to text end-to-end. It features a ~14.5M parameter temporal visual encoder combined with a pretrained Hugging Face `t5-small` text decoder (~60M parameters), yielding a total model size of approximately **75M parameters**.

---

## 2. Verified Repository Structure

The repository was cloned and verified directly on disk. The clean directory tree is as follows:

```text
research/ISLiM/
├── checkpoints/
│   └── .gitkeep                     # Placeholder; checkpoints are hosted externally
├── configs/
│   ├── isign_4loss.yaml             # Primary 4-loss training config on iSign
│   ├── phoenix_crosslingual.yaml    # Transfer learning config for German Phoenix-2014-T
│   └── spamof_4loss.yaml            # Config for SpaMo-OF 10K subset
├── data/
│   └── splits/
│       ├── .gitkeep
│       ├── generate_pose_stitch_split.py # Split generation script
│       ├── isign_all_pose_stitch.csv     # Full metadata table
│       ├── isign_train_pose_stitch.csv   # Training split (113,800 samples)
│       ├── isign_val_pose_stitch.csv     # Validation split (6,322 samples)
│       ├── isign_test_pose_stitch.csv    # Test split (6,323 samples)
│       └── summary.json                  # Dataset split statistics
├── scripts/
│   ├── eval/
│   │   ├── compare_phoenix.py       # Cross-dataset benchmark vs Phoenix
│   │   ├── compare_posestitch.py    # Benchmark vs PoseStitch baseline
│   │   ├── evaluate_all.py          # Primary evaluation script (BLEU, ROUGE, chrF, etc.)
│   │   ├── length_analysis.py       # Sequence length evaluation
│   │   └── loss_ablation.py         # Multi-loss ablation evaluator
│   ├── mobile/
│   │   ├── export_torchscript.py    # Tracing & script export to TorchScript / Lite
│   │   ├── prepare_data.py          # Android asset exporter
│   │   └── verify.py                # Cosine similarity & parity validator
│   ├── preprocess/
│   │   └── extract_keypoints.py     # Video to 94 MediaPipe Holistic landmarks
│   ├── viz/
│   │   ├── darken_for_print.py      # Plot adjustments
│   │   └── keypoint_comparison.py   # Visual inspection of skeletal frames
│   ├── run.sh                       # Wrapper shell script for training
│   └── train.py                     # Main PyTorch training routine
├── src/
│   ├── data/
│   │   ├── __init__.py
│   │   ├── augmentation.py          # Temporal & spatial augmentations (jitter, scaling)
│   │   ├── dataset.py               # PoseStitchDataset & SpaMoOFDataset PyTorch loaders
│   │   └── preprocessing.py         # Text cleaning and contraction expansion
│   ├── islim/
│   │   ├── __init__.py
│   │   ├── encoder.py               # VisualEncoder & ISLiMEncoder architecture
│   │   └── model.py                 # ISLiMModel wrapper integrating encoder + T5
│   ├── losses/
│   │   ├── __init__.py
│   │   ├── contrastive.py           # CLIP-style vision-text contrastive loss
│   │   ├── entropy.py               # Logit entropy regularization
│   │   └── semantic.py              # Sentence transformer semantic embedding loss
│   └── metrics.py                   # BLEU-1..4, ROUGE-L, METEOR, chrF++, WER
├── config.py                        # Central path & environment configuration
├── LICENSE                          # Apache-2.0 License
├── README.md                        # Project documentation & instructions
└── requirements.txt                 # Python dependencies
```

---

## 3. Important Source Files and Their Roles

| File Path | Component | Responsibility |
|---|---|---|
| `src/islim/model.py` | Model Root | Defines `ISLiMModel`, coordinating visual encoder forward pass, Hugging Face T5 decoder, target tokenization, multi-loss forward paths (`forward`, `forward_with_hidden`, `forward_with_clip`), and autoregressive `generate()` beam search. |
| `src/islim/encoder.py` | Visual Encoder | Implements `TemporalConv1D`, `VisualEncoder`, and `ISLiMEncoder`. Handles input projection (376 to 376), temporal convolutions (376 to 256 to 256), positional embeddings, query-token prepend (16 tokens), and 4-layer Transformer Encoder. |
| `scripts/preprocess/extract_keypoints.py` | Landmark Extraction | Extracts 94 MediaPipe Holistic landmarks per video frame, handles 5-frame interpolation over missing values, and saves `.npy` sequences of shape `(T, 94, 4)`. |
| `src/data/dataset.py` | Preprocessing & Loading | Reads keypoint files, applies spatial min-max scaling to `[0, 1]`, normalizes temporal length to 128 frames (resampling via `torch.linspace` or zero-padding), and batches tensors. |
| `src/data/preprocessing.py` | Text Processing | Implements PoseStitch-style text normalization (contractions expansion, number splitting, punctuation removal). |
| `scripts/eval/evaluate_all.py` | Batch Evaluation | Loads checkpoint `best_model.pt`, runs beam search on test set, calculates corpus sacreBLEU, PS-BLEU, ROUGE-L, chrF++, and METEOR. |
| `scripts/mobile/export_torchscript.py` | Deployment Utility | Traces `visual_encoder` and decomposes T5 decoder for TorchScript mobile execution with KV cache. |
| `config.py` | Configuration | Resolves dataset paths, checkpoint directories, and environment variables. |

---

## 4. Model Architecture Details

The ISLiM architecture is partitioned into two major stages:

```text
Keypoint Sequence (B, 4, 94, 128)
               │
               ▼
   [Permute to (B, 128, 94, 4)]
               │
   [Flatten Keypoints: 94 * 4 = 376 channels]
               │
   [Linear Projection: 376 → 376]
               │
   [2x Temporal Conv1D (kernel=5): 376 → 256 → 256]
               │
   [Linear Projection: 256 → 512]
               │
   [Add Learnable Positional Embedding (128, 512)]
               │
   [Prepend 16 Learnable Query Tokens (B, 16+128=144, 512)]
               │
   [4-Layer Transformer Encoder (d=512, heads=8, ffn=2048, GELU, norm_first)]
               │
   [Slice Prepended Query Tokens: x[:, :16, :]]
               │
   [LayerNorm + Linear Projection: 512 → 512]
               │
               ▼
Encoder Output / Visual Embeddings (B, 16, 512)
               │
               ▼
Pretrained T5-Small Decoder (Cross-Attention over 16 tokens)
               │
               ▼
Autoregressive Text Output (English Sentence)
```

### Key Architectural Parameters
- **Input Channels per Landmark:** 4 (`x`, `y`, `z`, `visibility`)
- **Number of Keypoints:** 94
- **Input Flat Dimension:** $94 \times 4 = 376$
- **Temporal Target Frames:** 128 frames
- **Temporal Convolutions:** 2 layers (channels: 376 $\to$ 256 $\to$ 256, kernel size: 5, padding: 2)
- **Transformer Encoder:** 4 layers, hidden size $d=512$, 8 attention heads, FFN dimension 2048, GELU activation, pre-layer normalization (`norm_first=True`)
- **Temporal Compression:** 16 learnable query tokens attend to all 128 temporal positions and are sliced off, producing a compressed $16 \times 512$ sequence ($8\times$ compression)
- **Decoder:** Hugging Face `T5ForConditionalGeneration` (`t5-small`, $d_{\text{model}}=512$, 6 decoder layers)
- **Generation Settings:** Beam search with `num_beams=4`, `repetition_penalty=1.5`, `no_repeat_ngram_size=3`, `length_penalty=1.2`, `max_length=128`

---

## 5. Input Format and Landmark Specification

ISLiM explicitly operates on **94 selected landmarks** extracted via MediaPipe Holistic:

| Index Range | Subsystem | Count | Specific Landmarks / Indices |
|---|---|---|---|
| **0 – 5** | Body (Pose) | 6 | Left Shoulder (11), Right Shoulder (12), Left Elbow (13), Right Elbow (14), Left Hip (23), Right Hip (24) |
| **6 – 26** | Left Hand | 21 | Wrist (0) and 20 finger joints (1–20) |
| **27 – 47** | Right Hand | 21 | Wrist (0) and 20 finger joints (1–20) |
| **48 – 67** | Lips (Face) | 20 | Mesh IDs: `[61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 409, 270, 95, 88, 178, 87, 14, 78, 308]` |
| **68 – 83** | Eyes (Face) | 16 | Mesh IDs: `[33, 133, 160, 158, 153, 144, 145, 246, 362, 263, 387, 385, 380, 373, 374, 249]` |
| **84 – 93** | Eyebrows (Face) | 10 | Mesh IDs: `[107, 66, 105, 63, 70, 336, 296, 334, 293, 300]` |
| **Total** | | **94** | |

### Channel Representation
Each landmark contains 4 values:
1. `x`: normalized horizontal coordinate
2. `y`: normalized vertical coordinate
3. `z`: depth coordinate
4. `visibility` (confidence):
   - Pose: direct MediaPipe confidence score.
   - Hands: set to `1.0` when detected.
   - Face: set to `1.0` if `z > -0.5`, otherwise `0.5`.

### Preprocessing and Normalization
1. **Gap Filling:** Linear interpolation across missing landmark gaps $\le 5$ consecutive frames. Unseen landmarks remain zero.
2. **Spatial Scaling:** Each sample's `x`, `y`, `z` coordinates are min-max scaled independently across all frames:
   $$\hat{x} = \frac{x - x_{\min}}{x_{\max} - x_{\min}}$$
3. **Temporal Normalization:**
   - If $T > 128$: uniformly sampled across time via `torch.linspace(0, T - 1, 128).long()`.
   - If $T < 128$: zero-padded along the temporal axis to reach 128 frames.
4. **Final Tensor Shape:** `(1, 4, 94, 128)` (or `(1, 128, 94, 4)`).

---

## 6. Pretrained Checkpoint Requirements

- **Local Repository Status:** No model checkpoints are bundled in the git tree (`checkpoints/` contains only `.gitkeep`).
- **External Checkpoint URL:** The repository `README.md` links to a Google Drive folder:  
  `https://drive.google.com/drive/folders/100H39_Pcpd6WeXmXG0-bEvif-HDHihzC?usp=sharing`
- **Required Model Files:**
  - `best_model.pt`: Contains the dictionary:
    ```python
    {
        "epoch": int,
        "model_state_dict": dict,
        "optimizer_state_dict": dict,
        "best_bleu4": float,
        "val_results": dict
    }
    ```
  - `t5-small` Hugging Face weights and tokenizer (downloaded automatically or cached via Hugging Face Hub).

---

## 7. Inference Pipeline Status & Gaps

### What is Available in the Repository
- **Batch Evaluation:** `scripts/eval/evaluate_all.py` can evaluate a dataset split against pre-extracted `.npy` files.
- **TorchScript Exporters:** `scripts/mobile/export_torchscript.py` decomposes the model into mobile-compatible traces.
- **Keypoint Extractor:** `scripts/preprocess/extract_keypoints.py` processes raw video files into `.npy` files.

### What is Missing or Unverified
1. **No Standalone Single-Sample Inference Script:** There is no `infer.py` or `predict.py` that accepts an input video, video stream, or live camera feed, extracts landmarks, runs inference, and returns predicted text.
2. **No Sample `.npy` Files:** Although the `README.md` claims the repository ships with 15 sample keypoint files, `research/ISLiM/data/` contains only CSV split tables and split generator scripts; no `.npy` files are included in the repository commits.
3. **External Checkpoint Verification:** The model weights in the external Google Drive have not yet been downloaded or verified for structural compatibility with `src/islim/model.py`.
4. **Streaming / Real-Time Buffering:** The model expects an entire sequence normalized to 128 frames. For live web camera usage, a sliding window buffer of frames (e.g., 60–128 frames at 25–30 FPS) or activity-detection trigger is required.

---

## 8. Integration Considerations for Signova AI (FastAPI + React)

1. **Inference Location (Frontend vs Backend):**
   - **Option A (Full Server Processing):** Frontend streams video frames over WebSocket or HTTP upload; FastAPI runs MediaPipe Holistic + PyTorch ISLiM.  
     *Drawback:* High network bandwidth, server CPU/GPU load running MediaPipe on every frame.
   - **Option B (Edge Landmark Extraction - Recommended):** Frontend runs MediaPipe Holistic in browser (using `@mediapipe/tasks-vision` or `@mediapipe/holistic`), extracts the 94 landmarks, and sends raw `(T, 94, 4)` numeric arrays to FastAPI via WebSocket or REST.  
     *Advantage:* Bandwidth drops by ~98% (sending small float arrays instead of high-res video), backend only performs fast tensor normalization and neural forward pass (~30–60 ms on GPU / ~150 ms on CPU).
2. **Resource Footprint:**
   - 75M parameters require only ~300 MB of RAM/VRAM in FP32 (and ~150 MB in FP16).
   - Easily deployable on consumer GPUs or lightweight cloud servers (e.g., Render, AWS, GCP).
3. **Signova AI Backend ML Service Plan:**
   - Create an isolated service in `backend/app/ml/` that implements:
     - Landmark indexing matching the 94 ISLiM points.
     - Min-max spatial normalization and 128-frame interpolation.
     - Checkpoint loader and cached `ISLiMModel` instance.
     - Fast greedy or beam search text generation.

---

*Report prepared by Signova AI Senior Engineering Team.*

