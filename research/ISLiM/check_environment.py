#!/usr/bin/env python3
"""
Environment Verification Script for ISLiM (Signova AI | Phase 1 | Part 1.2)
Verifies Python version, PyTorch, CUDA, GPU detection, and required library dependencies.
Does not download model weights or execute inference.
"""

import sys
import platform

def check_environment():
    print("=" * 60)
    print("       ISLiM Python Environment Verification")
    print("=" * 60)

    # 1. System & Python
    print(f"\n[System Information]")
    print(f"  OS Platform        : {platform.platform()}")
    print(f"  Python Executable  : {sys.executable}")
    print(f"  Python Version     : {sys.version.split()[0]}")
    python_ok = sys.version_info[:2] == (3, 11)
    status_str = "OK (Python 3.11.x)" if python_ok else "WARNING (Expected Python 3.11.x)"
    print(f"  Python Status      : {status_str}")

    # 2. PyTorch & CUDA Verification
    print(f"\n[PyTorch & CUDA Acceleration]")
    try:
        import torch
        print(f"  PyTorch Version    : {torch.__version__}")
        print(f"  CUDA Built With    : {torch.version.cuda}")
        cuda_available = torch.cuda.is_available()
        print(f"  CUDA Available     : {cuda_available}")
        if cuda_available:
            device_count = torch.cuda.device_count()
            print(f"  GPU Device Count   : {device_count}")
            for i in range(device_count):
                device_name = torch.cuda.get_device_name(i)
                total_mem = torch.cuda.get_device_properties(i).total_memory / (1024 ** 3)
                print(f"  GPU {i} Name         : {device_name} ({total_mem:.2f} GB VRAM)")
        else:
            print("  GPU Acceleration   : None (CPU Only)")
    except ImportError as e:
        print(f"  PyTorch Status     : FAILED (ImportError: {e})")
        torch = None

    # 3. Required Library Checks
    required_packages = [
        ("torch", "PyTorch deep learning framework"),
        ("torchvision", "PyTorch computer vision models/transforms"),
        ("transformers", "Hugging Face Transformers (T5 decoder)"),
        ("sentence_transformers", "Sentence embeddings for semantic loss"),
        ("mediapipe", "MediaPipe holistic landmark extraction"),
        ("numpy", "Numerical processing"),
        ("cv2", "OpenCV image/video processing"),
        ("pandas", "Data manipulation & split processing"),
        ("scipy", "Scientific computing"),
        ("sacrebleu", "BLEU / translation metrics"),
        ("rouge_score", "ROUGE evaluation metric"),
        ("nltk", "Natural language toolkit"),
        ("matplotlib", "Visualization"),
        ("tqdm", "Progress bar utilities")
    ]

    print(f"\n[Required Dependencies Verification]")
    all_ok = True
    missing_packages = []

    for pkg_name, description in required_packages:
        try:
            mod = __import__(pkg_name)
            ver = getattr(mod, "__version__", "installed")
            print(f"  [OK] {pkg_name:<22}: v{ver:<12} ({description})")
        except ImportError as e:
            all_ok = False
            missing_packages.append(pkg_name)
            print(f"  [FAIL] {pkg_name:<20}: MISSING ({description}) - {e}")

    print("\n" + "=" * 60)
    if all_ok and torch is not None:
        print("  Status: ALL REQUIRED DEPENDENCIES VERIFIED SUCCESSFULLY!")
    else:
        print(f"  Status: VERIFICATION FAILED - Missing: {missing_packages}")
    print("=" * 60)

    return 0 if (all_ok and torch is not None) else 1

if __name__ == "__main__":
    sys.exit(check_environment())

