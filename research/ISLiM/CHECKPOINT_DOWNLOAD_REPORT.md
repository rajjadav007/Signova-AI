# ISLiM Pretrained Checkpoint Download Report (Part 1.3)

**Date:** 2026-11-09  
**Model:** ISLiM (Indian Sign Language in Motion / Keypoint-based Sign Language Translation)  
**Task:** Phase 1 | Part 1.3 Pretrained Checkpoint Download & Organization  
**Status:** Completed & Verified  

---

## 1. Official Checkpoint Source

- **Official Repository:** [ahmedshoaib/ISLiM](https://github.com/ahmedshoaib/ISLiM)
- **Official Checkpoint Hosting:** Google Drive Folder documented in official `README.md`:
  `https://drive.google.com/drive/folders/100H39_Pcpd6WeXmXG0-bEvif-HDHihzC?usp=sharing`
- **Hosting Folder Contents Verified:**
  - `ISLiM_full_posestitch_pre_processed.pt` (Google Drive File ID: `1mZtXateoZn_3T1T4Lc3yowMvB0jWm9EX`)
  - `ISLiM_4Loss_best_for_10kSpamoOF.pt` (Google Drive File ID: `1DW7pyxnqUQwLxvJTSTzmOzmmCn5k14mP`)
  - `mobile/` subfolder (Android deployment & C++/Kotlin verification assets)

---

## 2. Downloaded Files & Verification Results

Both official pretrained checkpoint files were downloaded directly into `research/ISLiM/checkpoints/` using official filenames and verified with non-executing byte checks:

| Attribute | Primary iSign Checkpoint | SpaMo-OF Subset Checkpoint |
|---|---|---|
| **Filename** | `ISLiM_full_posestitch_pre_processed.pt` | `ISLiM_4Loss_best_for_10kSpamoOF.pt` |
| **Description** | Full iSign dataset (PoseStitch splits, 90/5/5, 4-loss) | SpaMo-OF 10k subset (80/10/10, 4-loss) |
| **Exact Size (Bytes)** | `899,966,348` bytes | `899,970,408` bytes |
| **Size (MB)** | `858.27 MB` | `858.28 MB` |
| **Magic Bytes** | `504b0304` (`PK\x03\x04` - PyTorch zip archive) | `504b0304` (`PK\x03\x04` - PyTorch zip archive) |
| **Archive Member** | `best_ps/data.pkl` | `best_model/data.pkl` |
| **MD5 Checksum** | `00f47cf4d586bd92e175d4ee6d83834a` | `06dfd255e606b4daf0f3f2bd11722179` |
| **SHA-256 Checksum** | `ffe4efbb5262abdd6221e4c8d818c92fc1db7fa7ea955ae0afa827251dd9140c` | `cf97d0ac9abcdfced0e128e98eede967ddf2479b2590eb0d1b891f96f176fc54` |
| **Integrity Status** | Complete, uncorrupted, non-HTML stream | Complete, uncorrupted, non-HTML stream |

---

## 3. Checkpoint Directory Structure

```text
research/ISLiM/checkpoints/
├── .gitkeep                                  # Git placeholder tracking directory
├── ISLiM_full_posestitch_pre_processed.pt    # 858.27 MB (Primary full iSign checkpoint)
└── ISLiM_4Loss_best_for_10kSpamoOF.pt        # 858.28 MB (SpaMo-OF 10k subset checkpoint)
```

---

## 4. Storage Space Status

- **Host Drive:** `D:\`
- **Initial Free Space:** `20.40 GB`
- **Space Used by Checkpoints:** `1.68 GB` (1,799,936,756 bytes)
- **Remaining Free Space:** `18.73 GB`
- **Assessment:** Sufficient disk space remaining for subsequent evaluation and inference tasks.

---

## 5. Security & Git Protection

- Root `.gitignore` contains rule `*.pt` and `!**/checkpoints/.gitkeep`.
- Checkpoints are verified excluded from Git tracking (`git status` shows clean checkpoint state).
- No model weights committed or staged.
- Checkpoints downloaded via verified official link without third-party mirrors or unsafe executables.
- Magic bytes confirm PyTorch ZIP archive structure without loading weights or executing pickle payloads.

---

## 6. Missing or Inaccessible Files

- **None.** All official pretrained model files documented in the upstream repository have been acquired and verified.

---

## 7. Modified & Created Files

- **Created:**
  - `research/ISLiM/download_checkpoints.py` — Deterministic streaming download and checksum verification tool.
  - `research/ISLiM/checkpoints/ISLiM_full_posestitch_pre_processed.pt` — Downloaded binary checkpoint.
  - `research/ISLiM/checkpoints/ISLiM_4Loss_best_for_10kSpamoOF.pt` — Downloaded binary checkpoint.
  - `research/ISLiM/CHECKPOINT_DOWNLOAD_REPORT.md` — This verification report.
- **Untouched:**
  - All original ISLiM source files in `src/`, `scripts/`, `configs/` remain completely untouched.

---

## 8. Part 1.3 Completion Status

- [x] Official checkpoint sources verified.
- [x] Required files identified.
- [x] Storage capacity checked.
- [x] Checkpoint directory created.
- [x] Official pretrained files downloaded.
- [x] File integrity checked.
- [x] Checkpoint organisation documented.
- [x] Large files excluded from Git.
- [x] Original ISLiM source files untouched.

**Verdict:** Part 1.3 is complete. Ready for Part 1.4 (Model architecture inspection and checkpoint loading) pending user approval.

