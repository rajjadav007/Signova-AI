# ISLiM Pretrained Model Comprehensive Evaluation Report (Part 1.8)

**Document:** `research/ISLiM/MODEL_EVALUATION_REPORT.md`  
**Execution Date:** 2026-11-09  
**Target Repository:** `research/ISLiM/`  
**Git Branch:** `preparation`  
**Primary Checkpoint:** `research/ISLiM/checkpoints/ISLiM_full_posestitch_pre_processed.pt`  
**Tokenizer Asset:** `research/ISLiM/assets/t5-small/`  
**Inspector:** Signova AI Engineering  
**Final Verdict:** **PARTIAL** (Engineering pipeline, preprocessing, latency, memory, and decoding benchmarks: **PASS**; Translation semantic accuracy: **UNVERIFIED / N/A** due to 0 verified ground-truth reference samples in workspace)

---

## 1. Executive Summary

This report delivers the comprehensive evaluation of the pretrained Indian Sign Language Model (ISLiM) under Part 1.8.

In accordance with strict evaluation protocols:
1. No synthetic ground-truth data or imaginary translations were invented.
2. The workspace was thoroughly inventoried for videos, keypoint arrays, and annotations.
3. The official ISLiM decoding parameters ($B=4, \text{repetition\_penalty}=1.5, \text{no\_repeat\_ngram\_size}=3, \text{length\_penalty}=1.2$) and corrected architecture configuration (`num_query_tokens=0`, full-frame mode) were evaluated.
4. Latency (cold/warm), peak GPU memory (VRAM), CPU versus GPU performance, and preprocessing throughput were benchmarked using CUDA synchronization.
5. Error analysis was performed across word-level alignments, repetition patterns, tracking stability, and domain discrepancies.

```
                              EVALUATION WORKFLOW
 ┌────────────────────────┐      ┌─────────────────────────┐      ┌─────────────────────────┐
 │   Data Inspection      │ ───> │  Preprocessing (4.6ms)  │ ───> │   Inference Benchmark   │
 │ 1 Video / 0 References │      │   Tensor (1, 4, 94, 128)│      │  Cold: 1.42s | Warm: 0.42s│
 └────────────────────────┘      └─────────────────────────┘      └─────────────────────────┘
                                                                               │
 ┌────────────────────────┐      ┌─────────────────────────┐                   │
 │ Final Verdict: PARTIAL │ <─── │     Error Analysis      │ <─────────────────┘
 │  Engineering: PASS     │      │   Substitutions: N/A    │
 │  Accuracy: UNVERIFIED  │      │   Domain Gap: DIVERGENT │
 └────────────────────────┘      └─────────────────────────┘
```

---

## 2. Evaluation Dataset Details

### 2.1 Workspace Data Inventory

An exhaustive search was conducted across the workspace for video files, `.npy` keypoint archives, and dataset splits.

| Data Category | Target Location | Found Count | Details / Status |
|---|---|---|---|
| **ISL Video Recordings** | Workspace root (`D:\Signova AI\`) | **1 file** | `International-Week-of-SnapYT.App.mp4` (145,070 bytes, 125 frames, 30.0 FPS, 360x360) |
| **iSign Test Split Metadata** | `research/ISLiM/data/splits/isign_test_pose_stitch.csv` | **6,304 rows** | Contains text transcripts (`text`, `text_original`) and pointers to `.npy` keypoint filenames (`kp_file`). |
| **iSign Val Split Metadata** | `research/ISLiM/data/splits/isign_val_pose_stitch.csv` | **6,322 rows** | Validation split metadata. |
| **iSign Train Split Metadata** | `research/ISLiM/data/splits/isign_train_pose_stitch.csv` | **113,800 rows** | Training split metadata. |
| **Physical Split Keypoint Files** | `research/ISLiM/data/keypoints/` | **0 files** | The physical `.npy` landmark files corresponding to the iSign splits are **not stored** in this repository. |
| **Extracted Real Video Keypoints** | `research/ISLiM/results/real_video_keypoints.npy` | **1 file** | `(125, 94, 4)` float32 array extracted via MediaPipe Holistic in Part 1.7.1. |

### 2.2 Usable Sample Accounting

In strict compliance with evaluation rules:
- **Total Usable Physical Samples:** **1** (`International-Week-of-SnapYT.App.mp4`)
- **Samples with Verified Ground-Truth References:** **0**
- **Samples without References (Unlabelled):** **1**
- **Metadata-Only Entries (Missing Keypoints):** **6,304**

> **Official Reporting Notice:**  
> The 6,304 rows in `isign_test_pose_stitch.csv` contain ground-truth reference sentences, but their corresponding `.npy` landmark files are absent from disk (`data/keypoints/` is empty). Conversely, the single physical video in the workspace (`International-Week-of-SnapYT.App.mp4`) does not have an official reference subtitle. Therefore, zero samples possess both physical input landmarks and verified reference text. Per instructions, translation accuracy metrics (BLEU, WER) are declared **UNVERIFIED / N/A**.

---

## 3. Evaluation Configuration

All tests were executed on the local runtime environment using the verified, non-fine-tuned assets:

| Parameter | Configured Value | Specification Source |
|---|---|---|
| **Model Checkpoint** | `ISLiM_full_posestitch_pre_processed.pt` | Epoch 103, 74,975,673 parameters |
| **Architecture Mode** | Full-frame visual encoder (`num_query_tokens = 0`) | `research/ISLiM/FINAL_MODEL_COMPATIBILITY_REPORT.md` |
| **Visual Encoder Embedding** | $d_{\text{model}} = 512, N_{\text{layers}} = 4, N_{\text{heads}} = 8$ | `src/islim/encoder.py` |
| **Language Decoder** | T5-small autoregressive cross-attention | Local weights in `research/ISLiM/assets/t5-small/` |
| **Tokenizer** | Local T5Tokenizer | `research/ISLiM/assets/t5-small/` |
| **Beam Search Configuration** | `num_beams = 4, repetition_penalty = 1.5, no_repeat_ngram_size = 3, length_penalty = 1.2, early_stopping = True, do_sample = False` | `scripts/eval/compare_posestitch.py` |
| **Greedy Search Configuration**| `num_beams = 1, do_sample = False` | Baseline contrastive decoding |
| **Input Shape** | `(1, 4, 94, 128)` float32 | `research/ISLiM/PREPROCESSING_PARITY_REPORT.md` |
| **Primary Compute Device** | NVIDIA GeForce RTX 2050 (4 GB VRAM) | CUDA 12.1, PyTorch 2.5.1 |
| **Secondary Compute Device** | AMD Ryzen CPU | Single-socket multicore host |

---

## 4. Translation Metrics

Translation metrics were evaluated through `research/ISLiM/evaluation/metrics.py`.

| Metric | Measured Value | Implementation / Tokenization | Validity Status |
|---|---|---|---|
| **Word Error Rate (WER)** | **N/A** | Levenshtein DP token alignment | **UNVERIFIED_NO_GROUND_TRUTH** |
| **PoseStitch BLEU-1 (B1)** | **N/A** | Add-1 smoothing, `str.split()` | **UNVERIFIED_NO_GROUND_TRUTH** |
| **PoseStitch BLEU-2 (B2)** | **N/A** | Add-1 smoothing, `str.split()` | **UNVERIFIED_NO_GROUND_TRUTH** |
| **PoseStitch BLEU-3 (B3)** | **N/A** | Add-1 smoothing, `str.split()` | **UNVERIFIED_NO_GROUND_TRUTH** |
| **PoseStitch BLEU-4 (B4)** | **N/A** | Add-1 smoothing, `str.split()` | **UNVERIFIED_NO_GROUND_TRUTH** |
| **Corpus-Level BLEU** | **N/A** | SacreBLEU / NLTK corpus BLEU | **UNVERIFIED_NO_GROUND_TRUTH** |
| **Exact Match Rate (EM)** | **N/A** | Normalized whitespace exact string match | **UNVERIFIED_NO_GROUND_TRUTH** |

### 4.1 Metric Safeguard Verification
`metrics.py` incorporates an automated guard against false validation. When executed against samples without verified reference translations, it returns:
```json
{
  "status": "UNVERIFIED_NO_GROUND_TRUTH",
  "message": "No verified ground truth reference translations available. Accuracy metrics cannot be calculated.",
  "metrics_available": false,
  "wer": null,
  "ps_bleu": {"b1": null, "b2": null, "b3": null, "b4": null},
  "exact_match": null,
  "evaluated_sample_count": 0
}
```
A unit self-test embedded within `metrics.py` verified that on identical ground-truth pairs, the implementation computes $\text{WER} = 0.0\%$ and $\text{BLEU-1} > 90.0\%$, ensuring algorithmic correctness whenever ground-truth data becomes available.

---

## 5. Example Predictions versus References

### 5.1 Real Video Sample: `International-Week-of-SnapYT.App.mp4`

| Field | Content | Notes |
|---|---|---|
| **Sample Identifier** | `International-Week-of-SnapYT.App.mp4` | Project root MP4 video |
| **Verified Reference Translation**| `None (Unlabelled clip)` | No official subtitle transcript provided |
| **Decoded Beam Search ($B=4$)** | `"but i cannot wait to stop and let me go"` | `[0, 68, 3, 23, 1178, 1749, 12, 1190, 11, 752, 140, 281, 1]` |
| **Decoded Greedy Search ($B=1$)** | `"i cannot wait to stop my unknown"` | `[0, 3, 23, 1178, 1749, 12, 1190, 82, 7752, 1]` |
| **CPU Decoded Output ($B=4$)** | `"but i cannot wait to stop and let me go"` | Bitwise identical token IDs to GPU execution |

### 5.2 Decoded Semantic Observations
1. **Linguistic Fluency:** Both beam and greedy search outputs form grammatically valid English phrases.
2. **Vocabulary Signature:** Greedy decoding produces the token `"unknown"` (`token_id: 7752`), directly reflecting the iSign training vocabulary convention where low-frequency sign words are mapped to `<unk> / unknown`.
3. **Semantic Divergence:** The video title suggests advocacy for the Deaf community ("International Week of the Deaf"), whereas the model generated conversational idioms ("cannot wait to stop and let me go"). Without reference annotations, this is categorized as **UNVERIFIED / POTENTIAL OUT-OF-DOMAIN HALLUCINATION**.

---

## 6. Runtime and Memory Benchmarks

All GPU measurements utilized `torch.cuda.synchronize()` before and after execution intervals to prevent asynchronous CUDA dispatch skew. Peak VRAM was monitored using PyTorch native memory tracking APIs (`reset_peak_memory_stats`, `max_memory_allocated`).

### 6.1 Benchmark Results Summary

| Benchmark Category | Metric | Measured Value | Operational Notes |
|---|---|---|---|
| **Preprocessing Throughput** | Mean Latency (10 runs) | **`13.84 ms`** | Linear interpolation + Min-Max normalization + Linspace resampling |
| | Minimum Latency | **`7.81 ms`** | Cache-warm execution |
| | Maximum Latency | **`19.73 ms`** | Cache-cold execution |
| | Latency Std. Dev. | **`3.00 ms`** | Highly deterministic pipeline |
| **Model Ingestion** | Checkpoint Load Time | **`1.818 s`** | 74.98M parameters mapped from local disk |
| **GPU Inference (Beam $B=4$)** | Cold Inference Latency | **`1.422 s`** | First pass (CUDA kernel compilation & initial memory allocation) |
| | Warm Inference Latency | **`0.422 s`** ($421.5\text{ ms}$) | Mean of 5 warm passes ($\sigma = 15.5\text{ ms}$, $\text{min} = 398.7\text{ ms}$) |
| **GPU Inference (Greedy $B=1$)**| Warm Inference Latency | **`0.257 s`** ($256.8\text{ ms}$) | Single-beam greedy decoding |
| **CPU Inference (Beam $B=4$)** | Single-pass Latency | **`0.821 s`** ($820.7\text{ ms}$) | AMD Ryzen host CPU execution |
| **Acceleration Factor** | GPU Speedup vs CPU | **`1.95x`** | Warm GPU ($0.422\text{ s}$) vs CPU ($0.821\text{ s}$) |
| **GPU Memory (VRAM)** | Baseline Model Allocated | **`289.16 MB`** | Weights in FP32 on RTX 2050 |
| | Peak VRAM During Generation | **`315.15 MB`** | **$7.69\%$ of 4,096 MB total GPU VRAM** |
| | VRAM Delta During Decoding | **`25.99 MB`** | Temporary KV-cache and beam search states |
| | Post-Generation Allocated | **`297.54 MB`** | Stable baseline state |
| **Reliability Count** | Success / Failure Count | **`1 / 0`** ($100\%$ success) | Zero kernel crashes, zero OOM errors |

---

## 7. Error Analysis

Error analysis was conducted using `research/ISLiM/evaluation/error_analysis.py`.

### 7.1 Word-Level Error Alignment
- **Substitutions:** Uncomputable (Ground truth reference absent).
- **Deletions / Omissions:** Uncomputable.
- **Insertions:** Uncomputable.

### 7.2 Repetition and Degeneracy Check
- **Consecutive Word Repeats:** `False` (0 detected).
- **Repeated Bigrams:** `False` (0 detected).
- **Degenerate Loops:** Neither beam search nor greedy search entered autoregressive repetition loops. `no_repeat_ngram_size=3` and `repetition_penalty=1.5` effectively eliminated cyclic degeneracies.

### 7.3 Malformed Output Detection
- **Is Malformed:** `False`.
- **Special Token Leakage:** None (`<pad>`, `</s>` properly stripped by tokenizer).
- **Token Count:** 13 tokens generated, well within the 128 max length constraint.

### 7.4 Landmark Extraction and Tracking Stability
Analysis of the 125-frame raw keypoint sequence:
- **Pose Detection Rate:** **`100.0%`** (125/125 frames)
- **Face Mesh Detection Rate:** **`100.0%`** (125/125 frames)
- **Right Hand Detection Rate:** **`96.0%`** (120/125 frames, max gap: 4 frames)
- **Left Hand Detection Rate:** **`88.0%`** (110/125 frames, max gap: 7 frames)
- **Overall Landmark Presence Rate:** **`96.43%`** (11,330 / 11,750 keypoint instances)
- **Tracking Risk Assessment:** **`MODERATE`**. While the right hand gaps ($\le 4$) were fully reconstructed by linear interpolation, the left hand had a 7-frame gap during resting posture that exceeded the standard 5-frame interpolation window.

### 7.5 Domain Discrepancy Analysis

| Evaluation Dimension | ISLiM Training Domain (iSign) | Evaluation Video Sample | Discrepancy Assessment |
|---|---|---|---|
| **Recording Origin** | Doordarshan & ISLRTC broadcast news | YouTube social media campaign | **DIVERGENT:** Formal sign language news vs informal social video |
| **Signer Presentation** | Studio broadcast framing, high contrast | Square mobile web video ($360\times 360$) | **ACCEPTABLE:** Upper body and hands visible |
| **Target Vocabulary** | News, government policy, formal education | Advocacy / campaign message | **DIVERGENT:** Tokenizer contains sign news vocabulary |
| **Temporal Span** | 128 frames ($~4.26\text{s}$) | 125 frames ($4.17\text{s}$) | **COMPLIANT:** Matches optimal ISLiM temporal window |

---

## 8. Limitations

1. **Absence of Ground-Truth Labels:** The repository lacks physical keypoint files for the 6,304 test split items and lacks subtitles for the sole real video. Translation accuracy (BLEU/WER) cannot be scientifically stated without verified reference labels.
2. **Fixed Temporal Window ($T=128$):** The visual encoder enforces a fixed 128-frame architecture. Shorter or longer continuous signing videos must be linearly resampled or chunked, which may compress or stretch dynamic hand motions.
3. **Left Hand Tracking Fragility:** When signers rest their non-dominant hand below camera view, MediaPipe hand tracking drops to 0.0, necessitating synthetic linear interpolation.
4. **Broadcast Vocabulary Bias:** Pretrained exclusively on iSign (formal Doordarshan news), the model may struggle with colloquial, conversational, or regional sign variations.

---

## 9. Deliverables Inventory

The following evaluation artifacts were created and validated in `research/ISLiM/`:

| File Path | Description | Lines / Size |
|---|---|---|
| `research/ISLiM/evaluation/metrics.py` | Standalone metric suite (WER, PoseStitch PS-BLEU B1-B4, SacreBLEU, EM) with safeguards and self-test suite | 240 lines |
| `research/ISLiM/evaluation/error_analysis.py` | Diagnostic tools for repetitions, tracking stability, malformed predictions, and domain gaps | 225 lines |
| `research/ISLiM/evaluation/evaluate_islim.py` | Complete end-to-end evaluation runner profiling preprocessing, cold/warm GPU, CPU, and decoding | 380 lines |
| `research/ISLiM/evaluation/results/evaluation_summary.json` | Comprehensive machine-readable evaluation report and performance metrics | 194 lines |
| `research/ISLiM/evaluation/results/evaluation_samples.csv` | Tabular sample-level breakdown of predictions, latencies, and tracking metrics | 2 rows |
| `research/ISLiM/MODEL_EVALUATION_REPORT.md` | This formal evaluation report | — |

---

## 10. Final Verdict

### Overall Verdict: **PARTIAL**

- **Engineering Pipeline & Ingestion:** **PASS**  
  The full pipeline ($\text{Video} \to \text{MediaPipe} \to \text{Preprocessing} \to \text{Visual Encoder} \to \text{T5-Small}$) executes deterministically without errors.
- **Runtime Performance & Memory:** **PASS**  
  Warm GPU latency of **`0.422 s`** ($421.5\text{ ms}$) and peak VRAM of **`315.15 MB`** easily meet edge and desktop real-time constraints.
- **Translation Semantic Accuracy:** **UNVERIFIED / N/A**  
  Zero physical samples with verified ground-truth reference translations exist in the workspace. In adherence to core rules, translation accuracy is not claimed.
