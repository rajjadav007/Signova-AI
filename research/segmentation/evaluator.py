"""
Quantitative evaluation module for sign segmentation against ground-truth annotations (Phase 4).
"""

from typing import Any, Dict, List, Optional, Tuple
import numpy as np


class SegmentationEvaluator:
    """
    Computes rigorous boundary-level and segment-level metrics:
    - Boundary Precision, Recall, F1
    - Segment-level tIoU, Precision, Recall, F1
    - Over-segmentation and under-segmentation rates
    - Missed and false boundary counts
    """

    def __init__(self, time_tolerance_seconds: float = 0.30, iou_threshold: float = 0.35):
        self.time_tolerance = time_tolerance_seconds
        self.iou_threshold = iou_threshold

    def evaluate(
        self,
        predicted_segments: List[Dict[str, Any]],
        ground_truth_segments: List[Dict[str, Any]],
        total_duration_seconds: float,
        processing_time_seconds: float,
    ) -> Dict[str, Any]:
        """
        Evaluate predicted segments against ground truth.

        Args:
            predicted_segments: List of dicts with 'start_timestamp' and 'end_timestamp'
            ground_truth_segments: List of dicts with 'start_time' and 'end_time'
            total_duration_seconds: Duration of source video in seconds
            processing_time_seconds: Time taken to process video

        Returns:
            Dictionary containing computed evaluation metrics.
        """
        num_pred = len(predicted_segments)
        num_gt = len(ground_truth_segments)

        # 1. Boundary-Level Evaluation
        # Each segment has two boundaries: start and end
        gt_starts = [float(s["start_time"]) for s in ground_truth_segments]
        gt_ends = [float(s["end_time"]) for s in ground_truth_segments]
        gt_boundaries = gt_starts + gt_ends

        pred_starts = [float(s["start_timestamp"]) for s in predicted_segments]
        pred_ends = [float(s["end_timestamp"]) for s in predicted_segments]
        pred_boundaries = pred_starts + pred_ends

        tp_boundaries = 0
        matched_gt_boundaries = set()

        for pb in pred_boundaries:
            match_idx = None
            min_dist = float("inf")
            for idx, gb in enumerate(gt_boundaries):
                dist = abs(pb - gb)
                if dist <= self.time_tolerance and dist < min_dist and idx not in matched_gt_boundaries:
                    min_dist = dist
                    match_idx = idx

            if match_idx is not None:
                tp_boundaries += 1
                matched_gt_boundaries.add(match_idx)

        fp_boundaries = len(pred_boundaries) - tp_boundaries
        fn_boundaries = len(gt_boundaries) - len(matched_gt_boundaries)

        boundary_precision = (
            tp_boundaries / len(pred_boundaries) if len(pred_boundaries) > 0 else 0.0
        )
        boundary_recall = (
            tp_boundaries / len(gt_boundaries) if len(gt_boundaries) > 0 else 0.0
        )
        boundary_f1 = (
            (2 * boundary_precision * boundary_recall / (boundary_precision + boundary_recall))
            if (boundary_precision + boundary_recall) > 0
            else 0.0
        )

        # 2. Segment-Level Evaluation (Temporal IoU)
        matched_pred_segments = 0
        matched_gt_segments = set()

        for pred in predicted_segments:
            p_start = float(pred["start_timestamp"])
            p_end = float(pred["end_timestamp"])
            best_iou = 0.0
            best_gt_idx = None

            for gt_idx, gt in enumerate(ground_truth_segments):
                g_start = float(gt["start_time"])
                g_end = float(gt["end_time"])

                inter = max(0.0, min(p_end, g_end) - max(p_start, g_start))
                union = max(p_end, g_end) - min(p_start, g_start)
                iou = inter / union if union > 0 else 0.0

                if iou >= self.iou_threshold and iou > best_iou and gt_idx not in matched_gt_segments:
                    best_iou = iou
                    best_gt_idx = gt_idx

            if best_gt_idx is not None:
                matched_pred_segments += 1
                matched_gt_segments.add(best_gt_idx)

        segment_precision = (
            matched_pred_segments / num_pred if num_pred > 0 else 0.0
        )
        segment_recall = (
            len(matched_gt_segments) / num_gt if num_gt > 0 else 0.0
        )
        segment_f1 = (
            (2 * segment_precision * segment_recall / (segment_precision + segment_recall))
            if (segment_precision + segment_recall) > 0
            else 0.0
        )

        # 3. Over-segmentation and under-segmentation rates
        over_seg_rate = max(0, num_pred - num_gt) / num_gt if num_gt > 0 else 0.0
        under_seg_rate = max(0, num_gt - num_pred) / num_gt if num_gt > 0 else 0.0

        fps_speed = (
            round(total_duration_seconds / processing_time_seconds, 2)
            if processing_time_seconds > 0
            else 0.0
        )

        return {
            "num_ground_truth_segments": num_gt,
            "num_detected_segments": num_pred,
            "boundary_metrics": {
                "tolerance_seconds": self.time_tolerance,
                "true_positive_boundaries": tp_boundaries,
                "false_positive_boundaries": fp_boundaries,
                "false_negative_boundaries": fn_boundaries,
                "precision": round(boundary_precision, 4),
                "recall": round(boundary_recall, 4),
                "f1_score": round(boundary_f1, 4),
            },
            "segment_metrics": {
                "iou_threshold": self.iou_threshold,
                "matched_segments": matched_pred_segments,
                "precision": round(segment_precision, 4),
                "recall": round(segment_recall, 4),
                "f1_score": round(segment_f1, 4),
            },
            "rates": {
                "over_segmentation_rate": round(over_seg_rate, 4),
                "under_segmentation_rate": round(under_seg_rate, 4),
            },
            "performance": {
                "video_duration_seconds": round(total_duration_seconds, 3),
                "processing_time_seconds": round(processing_time_seconds, 4),
                "realtime_factor": fps_speed,
            },
        }
