"""
Video processor module coordinating video reading, landmark extraction, and output persistence.
"""

from pathlib import Path
import time
from typing import Any, Dict, Optional, Tuple, Union
import numpy as np
import torch

from .config import (
    DEFAULT_RESULTS_DIR,
    KEYPOINT_COORDS,
    NUM_KEYPOINTS,
    VideoPipelineConfig,
)
from .landmark_extractor import MediaPipeLandmarkExtractor
from .output_handler import save_json_report, save_keypoints
from .video_reader import VideoReader


class VideoProcessor:
    """
    Coordinates end-to-end video processing:
    Video file -> Frame decoding -> MediaPipe 94-landmark extraction -> .npy & .json persistence.
    """

    def __init__(self, config: Optional[VideoPipelineConfig] = None):
        self.config = config or VideoPipelineConfig()

    def process_video(
        self,
        video_path: Union[str, Path],
        output_dir: Optional[Union[str, Path]] = None,
        save_output: bool = True,
    ) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Process a single video file end-to-end.

        Args:
            video_path: Path to video file (.mp4, .avi, .mov, .mkv)
            output_dir: Optional custom directory to save results.
            save_output: Whether to persist .npy array and .json report.

        Returns:
            Tuple of:
                keypoints: (T, 94, 4) float32 numpy array
                report: Dictionary of extraction metadata, statistics, and performance
        """
        target_video = Path(video_path).resolve()
        results_dir = Path(output_dir or self.config.results_dir).resolve()

        reader: Optional[VideoReader] = None
        extractor: Optional[MediaPipeLandmarkExtractor] = None

        t_total_start = time.perf_counter()

        try:
            reader = VideoReader(target_video)
            video_meta = reader.get_metadata()

            extractor = MediaPipeLandmarkExtractor(
                model_asset_path=self.config.model_asset_path,
                min_face_detection_confidence=self.config.min_face_detection_confidence,
                min_pose_detection_confidence=self.config.min_pose_detection_confidence,
                min_hand_landmarks_confidence=self.config.min_hand_landmarks_confidence,
            )

            frames_kps = []
            pose_detected_count = 0
            left_hand_detected_count = 0
            right_hand_detected_count = 0
            face_detected_count = 0

            t_extraction_start = time.perf_counter()

            for frame_idx, rgb_frame in reader.read_frames():
                kp, detections = extractor.extract_frame(rgb_frame)
                frames_kps.append(kp)

                if detections["pose"]:
                    pose_detected_count += 1
                if detections["left_hand"]:
                    left_hand_detected_count += 1
                if detections["right_hand"]:
                    right_hand_detected_count += 1
                if detections["face"]:
                    face_detected_count += 1

            t_extraction_end = time.perf_counter()
            extraction_duration = t_extraction_end - t_extraction_start
            total_duration = t_extraction_end - t_total_start

            processed_frames = len(frames_kps)
            if processed_frames == 0:
                raise RuntimeError(f"Zero frames processed for {target_video}")

            # Stack into (T, 94, 4) float32
            keypoints_seq = np.array(frames_kps, dtype=np.float32)

            # Missing landmark statistics
            total_kp_instances = processed_frames * NUM_KEYPOINTS
            # Visibility > 0.0 indicates a detected landmark
            present_kp_instances = int(np.count_nonzero(keypoints_seq[:, :, 3] > 0.0))
            missing_kp_instances = total_kp_instances - present_kp_instances
            presence_percentage = round((present_kp_instances / total_kp_instances) * 100, 2)

            # Performance stats
            fps_throughput = (
                round(processed_frames / extraction_duration, 2)
                if extraction_duration > 0
                else 0.0
            )
            avg_time_per_frame_ms = (
                round((extraction_duration / processed_frames) * 1000, 2)
                if processed_frames > 0
                else 0.0
            )

            # Hardware stats
            device_info = {
                "cuda_available": torch.cuda.is_available(),
                "device_name": (
                    torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"
                ),
            }

            video_stem = target_video.stem
            npy_path = results_dir / f"{video_stem}_keypoints.npy"
            json_path = results_dir / f"{video_stem}_extraction_report.json"

            report: Dict[str, Any] = {
                "original_video_filename": target_video.name,
                "video_duration": video_meta["duration_seconds"],
                "video_duration_seconds": video_meta["duration_seconds"],
                "fps": video_meta["fps"],
                "frame_count": video_meta["frame_count"],
                "resolution": video_meta["resolution"],
                "processed_frames": processed_frames,
                "landmark_sequence_shape": list(keypoints_seq.shape),
                "data_type": str(keypoints_seq.dtype),
                "total_landmark_instances": total_kp_instances,
                "present_landmark_count": present_kp_instances,
                "missing_landmark_count": missing_kp_instances,
                "landmark_presence_percentage": presence_percentage,
                "subsystem_detection_rates": {
                    "pose_detected_frames": pose_detected_count,
                    "pose_detection_percentage": round((pose_detected_count / processed_frames) * 100, 2),
                    "face_detected_frames": face_detected_count,
                    "face_detection_percentage": round((face_detected_count / processed_frames) * 100, 2),
                    "left_hand_detected_frames": left_hand_detected_count,
                    "left_hand_detection_percentage": round((left_hand_detected_count / processed_frames) * 100, 2),
                    "right_hand_detected_frames": right_hand_detected_count,
                    "right_hand_detection_percentage": round((right_hand_detected_count / processed_frames) * 100, 2),
                },
                "extraction_duration": round(extraction_duration, 4),
                "extraction_duration_seconds": round(extraction_duration, 4),
                "total_processing_duration_seconds": round(total_duration, 4),
                "average_time_per_frame_ms": avg_time_per_frame_ms,
                "processed_fps": fps_throughput,
                "device": device_info,
                "output_file_path": str(npy_path) if save_output else None,
                "report_file_path": str(json_path) if save_output else None,
                "extraction_status": "SUCCESS",
            }

            if save_output:
                save_keypoints(keypoints_seq, npy_path)
                save_json_report(report, json_path)

            return keypoints_seq, report

        finally:
            if reader is not None:
                reader.release()
            if extractor is not None:
                extractor.close()
