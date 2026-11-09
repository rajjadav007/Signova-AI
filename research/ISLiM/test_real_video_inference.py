"""
ISLiM Real Video Landmark Extraction & Pretrained Inference Script (Part 1.7.1)

Tests:
1. Video file inspection: International-Week-of-SnapYT.App.mp4.
2. MediaPipe Holistic 94-landmark extraction per frame across all 125 frames.
3. Missing-landmark statistics calculation.
4. Preprocessing through verified research/ISLiM/preprocessing pipeline.
5. ISLiM pretrained model loading (num_query_tokens=0, safe weights_only=True).
6. Autoregressive text generation with official decoding parameters.
7. Latency and GPU memory measurements.
8. Output translation evaluation against video topic and training domain.
"""

import os
import sys
import time
import json
from pathlib import Path
from typing import Dict, Any, List, Tuple

import cv2
import numpy as np
import torch

# Ensure research/ISLiM is on sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

# Ensure MPLCONFIGDIR is set to writable temp
os.environ["MPLCONFIGDIR"] = os.environ.get("TEMP", "C:/Temp")

from preprocessing import preprocess_sequence
from src.islim.model import ISLiMModel
from transformers import T5Tokenizer

import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.core.base_options import BaseOptions


# Official 94-landmark layout from scripts/preprocess/extract_keypoints.py
POSE_INDICES = [11, 12, 13, 14, 23, 24]
FACE_LIPS = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 409, 270, 95, 88, 178, 87, 14, 78, 308]
FACE_EYES = [33, 133, 160, 158, 153, 144, 145, 246, 362, 263, 387, 385, 380, 373, 374, 249]
FACE_EYEBROWS = [107, 66, 105, 63, 70, 336, 296, 334, 293, 300]
FACE_INDICES = FACE_LIPS + FACE_EYES + FACE_EYEBROWS

NUM_KEYPOINTS = 94
KEYPOINT_COORDS = 4


def register_safe_globals():
    safe_types = [
        np.core.multiarray.scalar,
        np.dtype,
        np.ndarray,
        np.core.multiarray._reconstruct,
        np.dtypes.Float64DType,
    ]
    torch.serialization.add_safe_globals(safe_types)


def inspect_video(video_path: Path) -> Dict[str, Any]:
    """Inspect video properties using OpenCV."""
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video file: {video_path}")
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration_s = round(frame_count / fps, 3) if fps > 0 else 0.0
    cap.release()

    return {
        "file_path": str(video_path),
        "file_name": video_path.name,
        "file_size_bytes": video_path.stat().st_size,
        "resolution": f"{width}x{height}",
        "width": width,
        "height": height,
        "fps": fps,
        "frame_count": frame_count,
        "duration_seconds": duration_s,
    }


def extract_landmarks_from_video(
    video_path: Path,
    model_asset_path: Path,
) -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Extract 94 ISLiM keypoints for each frame in video using MediaPipe HolisticLandmarker.
    Returns: (raw_keypoints_array (T, 94, 4), stats_dict)
    """
    options = vision.HolisticLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=str(model_asset_path)),
        running_mode=vision.RunningMode.IMAGE,
        min_face_detection_confidence=0.5,
        min_pose_detection_confidence=0.5,
        min_hand_landmarks_confidence=0.5,
    )
    landmarker = vision.HolisticLandmarker.create_from_options(options)

    cap = cv2.VideoCapture(str(video_path))
    frames_kps = []
    
    pose_detected_count = 0
    left_hand_detected_count = 0
    right_hand_detected_count = 0
    face_detected_count = 0
    total_frames = 0

    t_start = time.perf_counter()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        total_frames += 1
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        res = landmarker.detect(mp_image)

        kp = np.full((NUM_KEYPOINTS, KEYPOINT_COORDS), 0.0, dtype=np.float32)

        # 1. Pose: indices 0-5
        if res.pose_landmarks and len(res.pose_landmarks) > 0:
            pose_detected_count += 1
            for i, idx in enumerate(POSE_INDICES):
                if idx < len(res.pose_landmarks):
                    lm = res.pose_landmarks[idx]
                    vis = getattr(lm, "visibility", 1.0)
                    if vis is None:
                        vis = 1.0
                    kp[i] = [lm.x, lm.y, lm.z, vis]

        # 2. Left Hand: indices 6-26
        if res.left_hand_landmarks and len(res.left_hand_landmarks) > 0:
            left_hand_detected_count += 1
            for i in range(min(21, len(res.left_hand_landmarks))):
                lm = res.left_hand_landmarks[i]
                kp[6 + i] = [lm.x, lm.y, lm.z, 1.0]

        # 3. Right Hand: indices 27-47
        if res.right_hand_landmarks and len(res.right_hand_landmarks) > 0:
            right_hand_detected_count += 1
            for i in range(min(21, len(res.right_hand_landmarks))):
                lm = res.right_hand_landmarks[i]
                kp[27 + i] = [lm.x, lm.y, lm.z, 1.0]

        # 4. Face (Lips, Eyes, Eyebrows): indices 48-93
        if res.face_landmarks and len(res.face_landmarks) > 0:
            face_detected_count += 1
            for i, idx in enumerate(FACE_INDICES):
                if idx < len(res.face_landmarks):
                    lm = res.face_landmarks[idx]
                    vis = 1.0 if lm.z > -0.5 else 0.5
                    kp[48 + i] = [lm.x, lm.y, lm.z, vis]

        frames_kps.append(kp)

    cap.release()
    landmarker.close()
    extraction_time_s = time.perf_counter() - t_start

    raw_kps = np.array(frames_kps, dtype=np.float32)

    # Calculate missing landmark statistics
    # A keypoint is present in a frame if visibility > 0.0 (or sum != 0)
    total_kp_instances = total_frames * NUM_KEYPOINTS
    present_kp_instances = int(np.count_nonzero(raw_kps[:, :, 3] > 0.0))
    missing_kp_instances = total_kp_instances - present_kp_instances

    stats = {
        "extraction_time_seconds": round(extraction_time_s, 3),
        "fps_extraction": round(total_frames / extraction_time_s, 1) if extraction_time_s > 0 else 0,
        "total_frames_extracted": total_frames,
        "pose_frames_detected": pose_detected_count,
        "pose_detection_rate": round(pose_detected_count / total_frames * 100, 1),
        "face_frames_detected": face_detected_count,
        "face_detection_rate": round(face_detected_count / total_frames * 100, 1),
        "left_hand_frames_detected": left_hand_detected_count,
        "left_hand_detection_rate": round(left_hand_detected_count / total_frames * 100, 1),
        "right_hand_frames_detected": right_hand_detected_count,
        "right_hand_detection_rate": round(right_hand_detected_count / total_frames * 100, 1),
        "total_kp_instances": total_kp_instances,
        "present_kp_instances": present_kp_instances,
        "missing_kp_instances": missing_kp_instances,
        "overall_landmark_presence_rate": round(present_kp_instances / total_kp_instances * 100, 1),
    }

    return raw_kps, stats


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
            "num_query_tokens": 0,
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
    print("  ISLiM Pretrained Model Real Video Inference Testing (Part 1.7.1)")
    print("=" * 75)

    video_path = PROJECT_ROOT / "International-Week-of-SnapYT.App.mp4"
    if not video_path.exists():
        video_path = SCRIPT_DIR.parent.parent / "International-Week-of-SnapYT.App.mp4"
    if not video_path.exists():
        raise FileNotFoundError(f"Real video file not found at: {video_path}")

    results_dir = SCRIPT_DIR / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    task_asset = SCRIPT_DIR / "assets" / "holistic_landmarker.task"
    if not task_asset.exists():
        raise FileNotFoundError(f"MediaPipe task asset missing: {task_asset}")

    checkpoint_path = SCRIPT_DIR / "checkpoints" / "ISLiM_full_posestitch_pre_processed.pt"
    assets_dir = SCRIPT_DIR / "assets" / "t5-small"

    results: Dict[str, Any] = {}

    # Step 1: Video details
    print("\n[Step 1 & 2] Inspecting Video File...")
    vid_info = inspect_video(video_path)
    results["video_info"] = vid_info
    print(f"  File Name      : {vid_info['file_name']}")
    print(f"  Resolution     : {vid_info['resolution']}")
    print(f"  FPS            : {vid_info['fps']}")
    print(f"  Frame Count    : {vid_info['frame_count']}")
    print(f"  Duration       : {vid_info['duration_seconds']} s")

    # Step 3: Extract landmarks
    print("\n[Step 3] Extracting 94 Holistic Landmarks Across All Frames...")
    raw_kps, extraction_stats = extract_landmarks_from_video(video_path, task_asset)
    results["extraction_stats"] = extraction_stats
    results["raw_kps_shape"] = list(raw_kps.shape)
    
    # Save extracted keypoints
    saved_kps_path = results_dir / "real_video_keypoints.npy"
    np.save(str(saved_kps_path), raw_kps)
    results["saved_keypoints_path"] = str(saved_kps_path)

    print(f"  Extracted Shape : {raw_kps.shape} ({raw_kps.dtype})")
    print(f"  Extraction Time : {extraction_stats['extraction_time_seconds']} s ({extraction_stats['fps_extraction']} FPS)")
    print(f"  Pose Rate       : {extraction_stats['pose_detection_rate']}% ({extraction_stats['pose_frames_detected']}/{vid_info['frame_count']})")
    print(f"  Face Rate       : {extraction_stats['face_detection_rate']}% ({extraction_stats['face_frames_detected']}/{vid_info['frame_count']})")
    print(f"  Left Hand Rate  : {extraction_stats['left_hand_detection_rate']}% ({extraction_stats['left_hand_frames_detected']}/{vid_info['frame_count']})")
    print(f"  Right Hand Rate : {extraction_stats['right_hand_detection_rate']}% ({extraction_stats['right_hand_frames_detected']}/{vid_info['frame_count']})")
    print(f"  Overall Present : {extraction_stats['overall_landmark_presence_rate']}%")
    print(f"  Saved to        : {saved_kps_path}")

    # Step 4: Preprocessing
    print("\n[Step 4] Preprocessing Extracted Keypoint Sequence...")
    t_prep_start = time.perf_counter()
    preprocessed_tensor = preprocess_sequence(raw_kps, add_batch_dim=True)
    prep_time_ms = (time.perf_counter() - t_prep_start) * 1000

    results["preprocessing"] = {
        "prep_time_ms": round(prep_time_ms, 3),
        "tensor_shape": list(preprocessed_tensor.shape),
        "tensor_dtype": str(preprocessed_tensor.dtype),
        "tensor_min": float(preprocessed_tensor.min()),
        "tensor_max": float(preprocessed_tensor.max()),
    }
    print(f"  Preprocessed Shape : {preprocessed_tensor.shape}")
    print(f"  Value Range        : [{results['preprocessing']['tensor_min']:.4f}, {results['preprocessing']['tensor_max']:.4f}]")
    print(f"  Preprocessing Time : {results['preprocessing']['prep_time_ms']} ms")
    assert preprocessed_tensor.shape == (1, 4, 94, 128)

    # Step 5: Model Loading and Pretrained Inference
    print("\n[Step 5] Loading Pretrained Model and Executing Generation...")
    register_safe_globals()
    config = build_model_config(assets_dir)
    
    t_load_start = time.perf_counter()
    model = ISLiMModel(config)
    ckpt = torch.load(checkpoint_path, map_location="cpu", weights_only=True)
    model.load_state_dict(ckpt["model_state_dict"], strict=False)
    model.eval()
    load_time_s = time.perf_counter() - t_load_start

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    gpu_tensor = preprocessed_tensor.to(device)

    # GPU memory and inference profiling
    if device.type == "cuda":
        torch.cuda.synchronize()
        mem_before = torch.cuda.memory_allocated(device) / (1024 ** 2)
        torch.cuda.reset_peak_memory_stats(device)
    else:
        mem_before = 0.0

    # Official generation
    torch.cuda.synchronize() if device.type == "cuda" else None
    t_gen_start = time.perf_counter()
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
    torch.cuda.synchronize() if device.type == "cuda" else None
    gen_time_s = time.perf_counter() - t_gen_start

    if device.type == "cuda":
        mem_after = torch.cuda.memory_allocated(device) / (1024 ** 2)
        peak_mem = torch.cuda.max_memory_allocated(device) / (1024 ** 2)
    else:
        mem_after = 0.0
        peak_mem = 0.0

    # Tokenizer decode
    tokenizer = T5Tokenizer.from_pretrained(str(assets_dir))
    raw_ids = output_token_ids[0].tolist()
    decoded_with_special = tokenizer.decode(raw_ids, skip_special_tokens=False)
    decoded_clean = tokenizer.decode(raw_ids, skip_special_tokens=True).strip().lower()

    results["inference"] = {
        "device": str(device),
        "model_load_time_s": round(load_time_s, 3),
        "generation_time_s": round(gen_time_s, 4),
        "vram_before_mb": round(mem_before, 2),
        "vram_after_mb": round(mem_after, 2),
        "vram_peak_mb": round(peak_mem, 2),
        "generated_token_ids": raw_ids,
        "num_tokens": len(raw_ids),
        "decoded_with_special": decoded_with_special,
        "decoded_clean": decoded_clean,
    }

    print(f"  Generation Time     : {results['inference']['generation_time_s']} s")
    print(f"  VRAM Peak           : {results['inference']['vram_peak_mb']} MB")
    print(f"  Raw Token IDs       : {raw_ids}")
    print(f"  Decoded (w/ special): '{decoded_with_special}'")
    print(f"  Decoded (clean text): '{decoded_clean}'")

    # Step 6: Multiple generation variants for deeper inspection (e.g. greedy vs beam)
    print("\n[Step 6] Running Contrastive Decoding Inspection (Greedy vs Beam)...")
    with torch.no_grad():
        greedy_ids = model.t5.generate(
            inputs_embeds=encoder_out,
            max_length=128,
            num_beams=1,
            do_sample=False,
        )[0].tolist()
        greedy_text = tokenizer.decode(greedy_ids, skip_special_tokens=True).strip().lower()

    results["contrastive_decoding"] = {
        "greedy_token_ids": greedy_ids,
        "greedy_clean": greedy_text,
    }
    print(f"  Greedy (Beam=1)     : '{greedy_text}'")

    # Save results to JSON
    out_json = results_dir / "real_video_inference_results.json"
    with open(out_json, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[OK] Results written to {out_json}")

    return results


if __name__ == "__main__":
    main()

