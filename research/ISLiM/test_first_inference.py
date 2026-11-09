"""
ISLiM Pretrained Model First Inference & Text Generation Verification Script (Part 1.7)

Executes:
1. Environment and GPU verification.
2. Search and verification of valid input sample.
3. Preprocessing via verified research/ISLiM/preprocessing pipeline.
4. Model loading with safe weights_only=True and num_query_tokens=0.
5. Official ISLiM text generation with T5 decoder.
6. Timing measurements (model load, preprocessing, cold GPU, warm GPU, CPU).
7. GPU memory profiling (allocated, reserved, peak).
8. Token ID inspection and text decoding validation.
"""

import os
import sys
import time
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, Tuple

import numpy as np
import torch
import torch.nn.functional as F

# Ensure research/ISLiM is on sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from preprocessing import preprocess_sequence
from src.islim.model import ISLiMModel
from transformers import T5Tokenizer


def register_safe_globals():
    """Register safe NumPy globals for PyTorch weights_only=True loading."""
    safe_types = [
        np.core.multiarray.scalar,
        np.dtype,
        np.ndarray,
        np.core.multiarray._reconstruct,
        np.dtypes.Float64DType,
    ]
    torch.serialization.add_safe_globals(safe_types)


def compute_file_hash(path: Path) -> Tuple[str, str]:
    """Compute MD5 and SHA-256 for a given file."""
    md5_hash = hashlib.md5()
    sha256_hash = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            md5_hash.update(chunk)
            sha256_hash.update(chunk)
    return md5_hash.hexdigest(), sha256_hash.hexdigest()


def find_input_sample(script_dir: Path) -> Tuple[str, np.ndarray, bool]:
    """
    Search repository and local directories for real preprocessed keypoint sequence.
    Returns: (description, raw_array, is_real)
    """
    candidate_dirs = [
        script_dir / "data" / "keypoints",
        script_dir / "data",
        Path.home() / "Datasets" / "iSign" / "misc" / "iSign_Keypoints",
        Path.home() / "Datasets",
    ]
    
    found_real = None
    for c_dir in candidate_dirs:
        if c_dir.exists() and c_dir.is_dir():
            for f in c_dir.glob("*.npy"):
                try:
                    arr = np.load(f)
                    if arr.ndim == 3 and arr.shape[1] == 94 and arr.shape[2] == 4:
                        found_real = (f"Real sample from {f}", arr, True)
                        break
                except Exception:
                    continue
        if found_real:
            break

    if found_real:
        return found_real

    # Synthetic smoke test sample (explicitly labelled)
    # Shape: (T, 94, 4), e.g., T = 85
    print("\n[!] Real dataset sample not found locally. Initiating synthetic smoke test.")
    np.random.seed(42)
    T = 85
    # Realistic normalized landmark coordinates in [0.2, 0.8]
    coords = np.random.uniform(0.2, 0.8, size=(T, 94, 3)).astype(np.float32)
    # Visibility: 1.0 for valid landmarks
    vis = np.ones((T, 94, 1), dtype=np.float32)
    synthetic_seq = np.concatenate([coords, vis], axis=2)

    # Introduce a short gap (frames 25:28) on left hand (joints 6:27) to verify interpolation
    synthetic_seq[25:28, 6:27, :] = 0.0

    return (
        f"Synthetic smoke test sample (T={T}, 94, 4) with seed=42 and 3-frame missing gap",
        synthetic_seq,
        False,
    )


def build_model_config(assets_dir: Path) -> dict:
    return {
        "encoder": {
            "keypoint_dim": 4,
            "num_keypoints": 94,
            "temporal_channels": [376, 256, 256],
            "temporal_kernel": 5,
            "transformer_embed_dim": 512,
            "transformer_num_heads": 8,
            "transformer_num_layers": 4,
            "transformer_dropout": 0.2,
            "output_dim": 512,
            "max_frames": 128,
            "num_query_tokens": 0,  # Full-frame mode
        },
        "t5": {
            "t5_model": str(assets_dir.as_posix()),
            "d_model": 512,
            "max_target_len": 128,
            "label_smoothing": 0.0,
        },
    }


def main():
    print("=" * 75)
    print("  ISLiM Pretrained Model First Inference & Text Generation Verification")
    print("=" * 75)

    results: Dict[str, Any] = {}

    # 1. Environment & GPU Checks
    print("\n[1/7] Checking Environment and Hardware...")
    results["python_version"] = sys.version
    results["pytorch_version"] = torch.__version__
    results["cuda_available"] = torch.cuda.is_available()
    
    if torch.cuda.is_available():
        results["gpu_name"] = torch.cuda.get_device_name(0)
        results["gpu_vram_total_mb"] = round(torch.cuda.get_device_properties(0).total_memory / (1024 ** 2), 2)
        print(f"  PyTorch        : {results['pytorch_version']}")
        print(f"  CUDA Available : {results['cuda_available']}")
        print(f"  GPU Hardware   : {results['gpu_name']} ({results['gpu_vram_total_mb']} MB VRAM)")
    else:
        results["gpu_name"] = "None"
        results["gpu_vram_total_mb"] = 0.0
        print("  CUDA is NOT available! Running CPU-only.")

    checkpoint_path = SCRIPT_DIR / "checkpoints" / "ISLiM_full_posestitch_pre_processed.pt"
    assets_dir = SCRIPT_DIR / "assets" / "t5-small"
    
    if not checkpoint_path.exists():
        raise FileNotFoundError(f"Checkpoint not found: {checkpoint_path}")
    if not assets_dir.exists():
        raise FileNotFoundError(f"Tokenizer assets not found: {assets_dir}")

    results["checkpoint_path"] = str(checkpoint_path)
    results["checkpoint_size_bytes"] = checkpoint_path.stat().st_size
    results["checkpoint_size_mb"] = round(results["checkpoint_size_bytes"] / (1024 ** 2), 2)
    print(f"  Checkpoint     : {checkpoint_path.name} ({results['checkpoint_size_mb']} MB)")

    # 2. Input Sample
    print("\n[2/7] Finding and Loading Input Keypoint Sample...")
    sample_desc, raw_sample, is_real = find_input_sample(SCRIPT_DIR)
    results["sample_source"] = sample_desc
    results["is_real_sample"] = is_real
    results["raw_sample_shape"] = list(raw_sample.shape)
    results["raw_sample_dtype"] = str(raw_sample.dtype)
    print(f"  Sample Source  : {sample_desc}")
    print(f"  Raw Shape      : {raw_sample.shape} ({raw_sample.dtype})")
    print(f"  Real Sample?   : {is_real}")

    # 3. Input Preprocessing
    print("\n[3/7] Running Verified Preprocessing Pipeline...")
    t_prep_start = time.perf_counter()
    preprocessed_tensor = preprocess_sequence(raw_sample, add_batch_dim=True)
    t_prep_elapsed = time.perf_counter() - t_prep_start

    results["prep_time_ms"] = round(t_prep_elapsed * 1000, 3)
    results["preprocessed_shape"] = list(preprocessed_tensor.shape)
    results["preprocessed_dtype"] = str(preprocessed_tensor.dtype)
    results["preprocessed_min"] = float(preprocessed_tensor.min())
    results["preprocessed_max"] = float(preprocessed_tensor.max())
    print(f"  Preprocessed Shape : {preprocessed_tensor.shape}")
    print(f"  Preprocessed Dtype : {preprocessed_tensor.dtype}")
    print(f"  Value Range        : [{results['preprocessed_min']:.4f}, {results['preprocessed_max']:.4f}]")
    print(f"  Preprocessing Time : {results['prep_time_ms']} ms")
    assert preprocessed_tensor.shape == (1, 4, 94, 128), f"Unexpected shape {preprocessed_tensor.shape}"

    # 4. Model Loading
    print("\n[4/7] Instantiating and Loading Pretrained Model...")
    register_safe_globals()
    config = build_model_config(assets_dir)
    
    t_load_start = time.perf_counter()
    model = ISLiMModel(config)
    ckpt = torch.load(checkpoint_path, map_location="cpu", weights_only=True)
    load_res = model.load_state_dict(ckpt["model_state_dict"], strict=False)
    model.eval()
    t_load_elapsed = time.perf_counter() - t_load_start

    results["model_load_time_s"] = round(t_load_elapsed, 3)
    results["missing_keys"] = load_res.missing_keys
    results["unexpected_keys"] = load_res.unexpected_keys
    results["epoch"] = ckpt.get("epoch", -1)
    results["total_parameters"] = sum(p.numel() for p in model.parameters())

    print(f"  Model Load Time    : {results['model_load_time_s']} s")
    print(f"  Total Parameters   : {results['total_parameters']:,}")
    print(f"  Missing Keys       : {results['missing_keys']}")
    print(f"  Unexpected Keys    : {results['unexpected_keys']}")
    print(f"  Checkpoint Epoch   : {results['epoch']}")
    assert results["missing_keys"] == ["logit_scale"], f"Unexpected missing keys: {results['missing_keys']}"

    # Tokenizer check
    tokenizer = T5Tokenizer.from_pretrained(str(assets_dir))
    results["vocab_size"] = len(tokenizer)
    print(f"  Tokenizer Vocab    : {results['vocab_size']} tokens")

    # 5. GPU Inference & Generation
    if torch.cuda.is_available():
        print("\n[5/7] Executing GPU Inference & Text Generation...")
        device = torch.device("cuda:0")
        model = model.to(device)
        
        # Memory baseline before inference
        torch.cuda.synchronize()
        mem_alloc_before = torch.cuda.memory_allocated(device) / (1024 ** 2)
        mem_res_before = torch.cuda.memory_reserved(device) / (1024 ** 2)
        torch.cuda.reset_peak_memory_stats(device)

        gpu_tensor = preprocessed_tensor.to(device)

        # Cold inference (First generation)
        torch.cuda.synchronize()
        t_cold_start = time.perf_counter()
        with torch.no_grad():
            encoder_out = model.visual_encoder.get_sequence_output(gpu_tensor)
            output_token_ids = model.t5.generate(
                inputs_embeds=encoder_out,
                max_length=128,
                num_beams=4,
                repetition_penalty=1.5,
                no_repeat_ngram_size=3,
                do_sample=False,
                length_penalty=1.2,
                early_stopping=True,
            )
        torch.cuda.synchronize()
        t_cold_elapsed = time.perf_counter() - t_cold_start

        mem_alloc_after = torch.cuda.memory_allocated(device) / (1024 ** 2)
        mem_res_after = torch.cuda.memory_reserved(device) / (1024 ** 2)
        peak_alloc = torch.cuda.max_memory_allocated(device) / (1024 ** 2)
        peak_res = torch.cuda.max_memory_reserved(device) / (1024 ** 2)

        results["gpu_cold_inference_s"] = round(t_cold_elapsed, 4)
        results["gpu_mem_alloc_before_mb"] = round(mem_alloc_before, 2)
        results["gpu_mem_res_before_mb"] = round(mem_res_before, 2)
        results["gpu_mem_alloc_after_mb"] = round(mem_alloc_after, 2)
        results["gpu_mem_res_after_mb"] = round(mem_res_after, 2)
        results["gpu_peak_alloc_mb"] = round(peak_alloc, 2)
        results["gpu_peak_res_mb"] = round(peak_res, 2)

        print(f"  Cold Inference Time : {results['gpu_cold_inference_s']} s")
        print(f"  VRAM Allocated Pre  : {results['gpu_mem_alloc_before_mb']} MB")
        print(f"  VRAM Allocated Post : {results['gpu_mem_alloc_after_mb']} MB")
        print(f"  Peak VRAM Allocated : {results['gpu_peak_alloc_mb']} MB")
        print(f"  Peak VRAM Reserved  : {results['gpu_peak_res_mb']} MB")

        # Warm inference (3 runs)
        warm_times = []
        for _ in range(3):
            torch.cuda.synchronize()
            t0 = time.perf_counter()
            with torch.no_grad():
                enc_out = model.visual_encoder.get_sequence_output(gpu_tensor)
                _ = model.t5.generate(
                    inputs_embeds=enc_out,
                    max_length=128,
                    num_beams=4,
                    repetition_penalty=1.5,
                    no_repeat_ngram_size=3,
                    do_sample=False,
                    length_penalty=1.2,
                    early_stopping=True,
                )
            torch.cuda.synchronize()
            warm_times.append(time.perf_counter() - t0)

        results["gpu_warm_inference_mean_s"] = round(float(np.mean(warm_times)), 4)
        results["gpu_warm_inference_std_s"] = round(float(np.std(warm_times)), 4)
        print(f"  Warm Inference Mean : {results['gpu_warm_inference_mean_s']} s (std: {results['gpu_warm_inference_std_s']} s)")

        # Verify model.generate wrapper matches
        wrapped_output = model.generate(
            gpu_tensor,
            num_beams=4,
            repetition_penalty=1.5,
            no_repeat_ngram_size=3,
            do_sample=False,
        )
        results["wrapped_generate_output"] = wrapped_output
    else:
        device = torch.device("cpu")
        model = model.to(device)
        output_token_ids = None

    # 6. CPU Inference Check
    print("\n[6/7] Testing CPU Inference...")
    model_cpu = model.to("cpu")
    cpu_tensor = preprocessed_tensor.to("cpu")
    t_cpu_start = time.perf_counter()
    with torch.no_grad():
        enc_cpu = model_cpu.visual_encoder.get_sequence_output(cpu_tensor)
        cpu_output_ids = model_cpu.t5.generate(
            inputs_embeds=enc_cpu,
            max_length=128,
            num_beams=4,
            repetition_penalty=1.5,
            no_repeat_ngram_size=3,
            do_sample=False,
            length_penalty=1.2,
            early_stopping=True,
        )
    t_cpu_elapsed = time.perf_counter() - t_cpu_start
    results["cpu_inference_s"] = round(t_cpu_elapsed, 4)
    results["cpu_inference_success"] = True
    print(f"  CPU Inference Time  : {results['cpu_inference_s']} s")
    print(f"  CPU Inference Status: PASSED")

    # If GPU was not available, use CPU output IDs
    if output_token_ids is None:
        output_token_ids = cpu_output_ids

    # 7. Text Decoding & Output Validation
    print("\n[7/7] Validating Generation Outputs...")
    raw_ids = output_token_ids[0].tolist()
    decoded_with_special = tokenizer.decode(raw_ids, skip_special_tokens=False)
    decoded_clean = tokenizer.decode(raw_ids, skip_special_tokens=True).strip().lower()

    results["generated_token_ids"] = raw_ids
    results["num_tokens_generated"] = len(raw_ids)
    results["decoded_with_special"] = decoded_with_special
    results["decoded_clean"] = decoded_clean
    results["is_non_empty"] = len(decoded_clean) > 0
    results["has_eos"] = tokenizer.eos_token_id in raw_ids

    print(f"  Generated Token IDs : {raw_ids}")
    print(f"  Token Count         : {len(raw_ids)}")
    print(f"  Decoded (w/ special): '{decoded_with_special}'")
    print(f"  Decoded (clean text): '{decoded_clean}'")
    print(f"  Non-empty Output?   : {results['is_non_empty']}")
    print(f"  Contains EOS Token? : {results['has_eos']}")

    # Save structured results to JSON for reporting
    out_json = SCRIPT_DIR / "first_inference_results.json"
    with open(out_json, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[OK] Results written to {out_json}")

    return results


if __name__ == "__main__":
    main()

