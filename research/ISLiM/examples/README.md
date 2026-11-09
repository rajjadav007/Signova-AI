# ISLiM Inference Examples

This directory demonstrates how to use the standalone ISLiM Python inference application.

## Prerequisites

Activate the virtual environment from `research/ISLiM`:

```powershell
.\.venv\Scripts\Activate.ps1
```

## Running the Example

Execute the example script:

```bash
python examples/example_inference.py
```

The script:
1. Loads the pretrained model once into memory on GPU (or CPU fallback).
2. Performs official beam search generation on `results/real_video_keypoints.npy`.
3. Performs greedy generation on the same keypoints.
4. Prints structured timing, shapes, and decoded English sentences.
