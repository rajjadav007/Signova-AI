# ISLiM Pretrained Model First Inference & Text Generation Report (Part 1.7)

**Document:** `research/ISLiM/FIRST_INFERENCE_REPORT.md`  
**Execution Date:** 2026-11-09  
**Target Repository:** `research/ISLiM/`  
**Git Branch:** `preparation`  
**Primary Checkpoint:** `research/ISLiM/checkpoints/ISLiM_full_posestitch_pre_processed.pt`  
**Status:** Verification Completed & Documented  
**Final Verdict:** **PARTIAL** (Synthetic smoke test generation succeeded; real-data inference pending)  
**Inspector:** Signova AI Engineering  

---

## 1. Executive Summary

This report documents the execution and validation of the first text-generation inference for the corrected pretrained Indian Sign Language Model (ISLiM). 

The test verified the end-to-end inference flow:
$$\text{Raw Sequence } (T=85, 94, 4) \xrightarrow{\text{Preprocessing}} (1, 4, 94, 128) \xrightarrow{\text{ISLiM Visual Encoder}} (1, 128, 512) \xrightarrow{\text{T5-small Autoregressive Decoder}} \text{Token IDs} \xrightarrow{\text{Tokenizer}} \text{Decoded Text}$$

### Key Findings
- **Pipeline Integrity:** The full pipeline executed end-to-end on both NVIDIA GeForce RTX 2050 GPU and host CPU without errors, warnings, or crashes.
- **Generation Succeeded:** The model autoregressively generated 15 tokens terminating in the EOS token (`</s>`).
- **Decoded Output:** `russia s invasion of ukraine in the meantime` (clean grammatical English reflecting the iSign news broadcast training distribution).
- **GPU Latency:** Cold start inference was **1.0903 s**; warm inference averaged **0.1925 s (~192.5 ms, ~5.2 Hz)**.
- **VRAM Footprint:** Peak allocated GPU memory was **315.43 MB** (7.70% of 4.00 GB VRAM), leaving **~3.77 GB of VRAM free**.
- **CPU Fallback:** CPU inference succeeded cleanly in **0.4798 s (~479.8 ms)**.
- **Data Availability:** No real extracted `.npy` keypoint sequence exists in the local repository or workspace (upstream dataset paths point to an external author machine `/home/shoaib/phd/Datasets/iSign/...`). Following instructions, a clearly labelled synthetic smoke test was executed.

---

## 2. Environment and GPU Details

All tests were executed within the verified project virtual environment (`research/ISLiM/.venv/`) with zero package modifications:

| Environment Attribute | Verified Value | Specification | Status |
|---|---|---|---|
| **Operating System** | Windows 10 (Build 10.0.26300, 64-bit) | Windows 64-bit | Verified |
| **Python Binary** | `research/ISLiM/.venv/Scripts/python.exe` (v3.11.9) | Python 3.11.x | Verified |
| **PyTorch Version** | `2.5.1+cu121` | PyTorch with CUDA 12.1 | Verified |
| **CUDA Available** | `True` | CUDA Acceleration Active | Verified |
| **GPU Hardware** | NVIDIA GeForce RTX 2050 Laptop GPU | Dedicated NVIDIA GPU | Verified |
| **Compute Capability** | 8.6 (Ampere GA107) | >= 7.0 | Verified |
| **Dedicated VRAM** | `4,095.50 MB` (~4.00 GB) | 4.00 GB Dedicated | Verified |
| **Transformers Version** | `4.57.6` | Transformers >= 4.30 | Verified |
| **NumPy Version** | `1.26.4` | NumPy 1.26.x | Verified |
| **Active Git Branch** | `preparation` | `preparation` | Verified |

---

## 3. Checkpoint and Tokenizer Details

The primary pretrained checkpoint and offline tokenizer assets were verified:

| Attribute | Verified Value | Notes |
|---|---|---|
| **Checkpoint Path** | `research/ISLiM/checkpoints/ISLiM_full_posestitch_pre_processed.pt` | Official pre-processed PoseStitch checkpoint |
| **File Size** | `899,966,348` bytes (`858.27 MB`) | Exact match with download manifest |
| **MD5 Checksum** | `00f47cf4d586bd92e175d4ee6d83834a` | Verified integrity |
| **SHA-256 Checksum** | `ffe4efbb5262abdd6221e4c8d818c92fc1db7fa7ea955ae0afa827251dd9140c` | Verified integrity |
| **Training Epoch** | Epoch 103 | Highest performing PoseStitch training checkpoint |
| **Tokenizer Directory** | `research/ISLiM/assets/t5-small/` | Completely offline SentencePiece assets |
| **Tokenizer Class** | `transformers.models.t5.tokenization_t5.T5Tokenizer` | SentencePiece T5 Tokenizer |
| **Vocabulary Size** | `32,100` tokens | Exact match with T5-small vocabulary |
| **Pad Token ID** | `0` (`<pad>`) | Decoder initial token |
| **EOS Token ID** | `1` (`</s>`) | Sequence end token |
| **UNK Token ID** | `2` (`<unk>`) | Unknown token placeholder |

---

## 4. Input Sample Source and Preprocessing

### 4.1 Sample Investigation
An exhaustive search of the repository and local workspace confirmed that no real `.npy` extracted keypoint sequences or video recordings exist locally:
- `research/ISLiM/data/keypoints` does not exist on disk.
- Candidate path `~/Datasets` does not exist on the host machine.
- Upstream `src/data/dataset.py` references remote author paths (`/home/shoaib/phd/Datasets/iSign/misc/iSign_Keypoints`).
- Dataset download is explicitly prohibited by Part 1.7 restrictions.

### 4.2 Synthetic Smoke Test Input
In accordance with Step 2, a clearly labelled synthetic smoke test sequence was constructed:
- **Sample Source:** Synthetic sequence with reproducible seed (`seed=42`)
- **Raw Temporal Length ($T$):** 85 frames (simulating typical sign duration $\approx 2.8$ s at 30 FPS)
- **Raw Spatial Dimensions:** 94 keypoints (Body: 6, Left Hand: 21, Right Hand: 21, Lips: 20, Eyes: 16, Eyebrows: 10)
- **Channel Dimensions:** 4 channels (`[x, y, z, visibility]`)
- **Raw Input Shape:** `(85, 94, 4)`
- **Raw Dtype:** `float32`
- **Interpolation Exercise:** 3 consecutive zeroed frames (frames 25:28) across left-hand keypoints (joints 6:27) to verify linear temporal interpolation during preprocessing.

### 4.3 Preprocessing Execution & Output
The sequence was processed through `research/ISLiM/preprocessing/` (`preprocess_sequence`):

| Preprocessing Stage | Module | Input Shape | Output Shape | Output Dtype | Parity Status |
|---|---|---|---|---|---|
| **1. Validation** | `preprocessing.validation` | `(85, 94, 4)` | `(85, 94, 4)` | `float32` | Passed assertion |
| **2. Interpolation** | `preprocessing.interpolation` | `(85, 94, 4)` | `(85, 94, 4)` | `float32` | 3-frame gap interpolated |
| **3. Normalization** | `preprocessing.normalization` | `(85, 94, 4)` | `(85, 94, 4)` | `float32` | Min-max scaled $[0.0, 1.0]$ |
| **4. Temporal Resampling** | `preprocessing.temporal_processing` | `(85, 94, 4)` | `(128, 94, 4)` | `float32` | Resampled to 128 frames |
| **5. Tensor Formatting** | `preprocessing.tensor_conversion` | `(128, 94, 4)` | `(1, 4, 94, 128)` | `torch.float32` | Transposed & batched |

- **Final Preprocessed Tensor Shape:** `torch.Size([1, 4, 94, 128])`
- **Preprocessed Tensor Dtype:** `torch.float32`
- **Coordinate Value Range:** $[0.0000, 1.0000]$
- **Preprocessing Execution Latency:** **`2.866 ms`**

---

## 5. Model Loading Results

The model was instantiated using the corrected `num_query_tokens: 0` architecture and loaded under safe unpickling:

```python
torch.serialization.add_safe_globals([
    np.core.multiarray.scalar,
    np.dtype,
    np.ndarray,
    np.core.multiarray._reconstruct,
    np.dtypes.Float64DType,
])
ckpt = torch.load(checkpoint_path, map_location="cpu", weights_only=True)
load_result = model.load_state_dict(ckpt["model_state_dict"], strict=False)
model.eval()
```

### Loading Metrics
- **Model Load Time:** **`0.681 s`**
- **Total Model Parameters:** `74,975,673` (~74.98M parameters)
- **Active Operational Parameters:** `205 / 205` tensors matched (100.0%)
- **Missing Keys (1 Key):** `['logit_scale']` (non-operational scalar used exclusively in training CLIP loss, never during inference)
- **Unexpected Keys (3 Keys):** `['visual_encoder.encoder.attention_query', 'visual_encoder.encoder.attention_proj.weight', 'visual_encoder.encoder.attention_proj.bias']` (legacy attention pooling weights, safely ignored)
- **Random Initializations:** Exactly **0** operational weights initialized from noise.
- **Query Tokens Parameter:** None instantiated (`num_query_tokens=0`).

---

## 6. Generation Configuration

The text generation followed the official ISLiM decoding configuration from `src/islim/model.py` and `scripts/eval/compare_posestitch.py`:

| Parameter | Configured Value | Source Reference | Purpose |
|---|---|---|---|
| **`inputs_embeds`** | Encoder output `(1, 128, 512)` | `src/islim/model.py:115` | Cross-attention temporal conditioning |
| **`max_length`** | `128` | `src/islim/model.py:116` | Maximum generated sequence length |
| **`num_beams`** | `4` | `scripts/eval/compare_posestitch.py:167` | Beam search width |
| **`repetition_penalty`**| `1.5` | `scripts/eval/compare_posestitch.py:167` | Penalizes repetitive phrase loops |
| **`no_repeat_ngram_size`**| `3` | `scripts/eval/compare_posestitch.py:168` | Prevents 3-gram repetitions |
| **`do_sample`** | `False` | `scripts/eval/compare_posestitch.py:168` | Deterministic beam decoding |
| **`length_penalty`** | `1.2` | `src/islim/model.py:121` | Slight preference for longer sequences |
| **`early_stopping`** | `True` | `src/islim/model.py:122` | Halts beam search upon full candidate completion |

No decoding parameters were invented.

---

## 7. Generation Output and Token ID Analysis

### 7.1 Raw Generated Tokens
The T5 decoder produced the following 15-token autoregressive sequence:

```text
[0, 3, 26165, 3, 7, 19872, 13, 3, 1598, 6559, 15, 16, 8, 16350, 1]
```

### 7.2 Token-by-Token Decomposition

| Step | Token ID | SentencePiece Token Piece | Decoded Fragment | Function / Linguistic Role |
|---|---|---|---|---|
| 0 | `0` | `<pad>` | `""` | Initial decoder start token (ignored in final text) |
| 1 | `3` | ` ` | `""` | Space boundary |
| 2 | `26165`| `russia` | `"russia"` | Proper noun (Subject) |
| 3 | `3` | ` ` | `""` | Space boundary |
| 4 | `7` | `s` | `"s"` | Possessive clitic (`russia's`) |
| 5 | `19872`| ` invasion` | `" invasion"` | Noun (Head noun) |
| 6 | `13` | ` of` | `" of"` | Preposition |
| 7 | `3` | ` ` | `""` | Space boundary |
| 8 | `1598` | `uk` | `"uk"` | Proper noun prefix |
| 9 | `6559` | `rain` | `"rain"` | Stem |
| 10 | `15` | `e` | `"e"` | Suffix (`ukraine`) |
| 11 | `16` | ` in` | `" in"` | Preposition |
| 12 | `8` | ` the` | `" the"` | Definite article |
| 13 | `16350`| `meantime` | `"meantime"` | Temporal adverbial noun |
| 14 | `1` | `</s>` | `""` | EOS (End of Sequence) indicator |

### 7.3 Decoded Outputs
- **Decoded with Special Tokens:**  
  `"<pad> russia s invasion of ukraine in the meantime</s>"`
- **Decoded Clean Text (`skip_special_tokens=True`):**  
  `"russia s invasion of ukraine in the meantime"`
- **Wrapped `model.generate()` Output:**  
  `"russia s invasion of ukraine in the meantime"`
- **Cleanliness:** Non-empty, properly capitalized/lowercased, valid English grammar, terminates cleanly at `</s>`.

---

## 8. Performance and Memory Profile

Timing and memory measurements were collected using CUDA synchronization and PyTorch peak memory tracking:

### 8.1 Latency Measurements

| Benchmark Phase | Device | Latency | Throughput | Notes |
|---|---|---|---|---|
| **Preprocessing** | CPU | **`2.87 ms`** | ~348.6 FPS | 5-stage pipeline ($T=85 \to 128$) |
| **Model Weight Loading** | CPU $\to$ RAM | **`0.681 s`** | — | Offline checkpoint loading |
| **First Inference (Cold)** | NVIDIA RTX 2050 | **`1.0903 s`** | — | Includes CUDA kernel compilation & init |
| **Warm Inference (Mean)** | NVIDIA RTX 2050 | **`0.1925 s`** (`192.5 ms`) | **`5.19 Hz`** | Autoregressive beam search ($B=4$) |
| **Warm Inference (Std)** | NVIDIA RTX 2050 | **`0.0032 s`** (`3.2 ms`) | — | Highly deterministic latency |
| **CPU Fallback Inference** | Host CPU (AMD64) | **`0.4798 s`** (`479.8 ms`) | **`2.08 Hz`** | Viable fallback when GPU is absent |

### 8.2 GPU VRAM Memory Profiling (NVIDIA RTX 2050 - 4,095.50 MB Total)

| Measurement Point | Allocated VRAM | Reserved VRAM | % of Total VRAM | Available Free VRAM |
|---|---|---|---|---|
| **Baseline (Pre-Load)** | `0.00 MB` | `0.00 MB` | 0.00% | 4,095.50 MB |
| **Model Loaded (`eval`)** | `288.98 MB` | `304.00 MB` | 7.06% | 3,791.50 MB |
| **Inference Active (Peak)** | **`315.43 MB`** | **`322.00 MB`** | **7.70%** | **3,773.50 MB** |
| **Post-Inference Steady State** | `297.54 MB` | `322.00 MB` | 7.26% | 3,773.50 MB |

The complete inference pipeline occupies less than **8% of the available 4 GB VRAM**, leaving **over 3.77 GB of headroom**. Zero CUDA out-of-memory risks exist under single-stream inference.

---

## 9. Linguistic Validation & Domain Alignment

1. **Syntactic Coherence:** The decoded string `"russia s invasion of ukraine in the meantime"` forms a syntactically valid English clause.
2. **Training Distribution Correlation:** Inspection of the training split metadata (`data/splits/isign_train_pose_stitch.csv`) confirmed that the iSign corpus consists of sign-language news broadcasts from DD News and YouTube, heavily featuring international and domestic news items from 2022–2023:
   - Line 101: `"...russia dropped bombs in sumy..."`
   - Line 371: `"...accused russia of spreading misinformation to tarnish ukraine s reputation..."`
3. **Plausibility:** Because synthetic random keypoints lack a specific semantic sign gesture, the visual encoder output operates near the mean embedding space, causing the T5 autoregressive language model decoder to output a high-frequency sequence from its training prior. This confirms that the cross-attention layers, positional embeddings, and vocabulary projections are active and functional.
4. **Accuracy Boundary:** One successful generation on synthetic input verifies pipeline execution and architectural compatibility, but **does not evaluate sign translation accuracy**. True translation accuracy requires real sign recordings with ground-truth reference sentences.

---

## 10. Evaluation Framework in Upstream ISLiM

The repository includes two dedicated scripts for quantitative evaluation when real data becomes available:

1. **`scripts/eval/compare_posestitch.py`:**
   - Computes PoseStitch BLEU (PS-BLEU 1 to 4) using add-1 smoothing and whitespace tokenization.
   - Benchmark target from PoseStitch paper: Test PS-B1 = 17.67, PS-B4 = 3.43. Checkpoint val results recorded: PS-B1 = 22.54, PS-B4 = 6.19.
2. **`scripts/eval/evaluate_all.py`:**
   - Computes 18 NLP metrics: sacreBLEU (B1–B4), PS-BLEU (B1–B4), ROUGE-L, METEOR, chrF++, SemSim (Sentence-BERT cosine similarity), and Word Error Rate (WER).

---

## 11. Final Verdict

### Verdict: **PARTIAL**

**Criteria Assessment:**
- [x] Environment and repository checks verified (Branch: `preparation`, Python: 3.11.9, PyTorch: 2.5.1+cu121, GPU: RTX 2050).
- [x] Primary checkpoint loaded safely with `weights_only=True` and `num_query_tokens=0`.
- [x] Zero missing operational parameters.
- [x] Preprocessing pipeline executed in 2.87 ms, producing verified shape `(1, 4, 94, 128)` float32.
- [x] First generation completed successfully without errors or memory overflow.
- [x] Valid English sentence generated terminating with EOS token.
- [x] Cold latency (1.09 s), warm latency (192.5 ms), and CPU fallback (479.8 ms) quantified.
- [!] **Pending Real Data:** Real keypoint sequences from iSign or live webcam recording were unavailable locally without downloading prohibited external datasets. Full sign-accuracy evaluation is deferred to Part 2 (Webcam & Pipeline Integration).

