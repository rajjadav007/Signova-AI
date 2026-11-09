"""
ISLiM 94-Landmark mapping and extraction specifications.

Groups:
  - Body/Pose: 6 landmarks (0-5)
  - Left Hand: 21 landmarks (6-26)
  - Right Hand: 21 landmarks (27-47)
  - Lips: 20 landmarks (48-67)
  - Eyes: 16 landmarks (68-83)
  - Eyebrows: 10 landmarks (84-93)
Total: 94 keypoints, 4 channels [x, y, z, visibility].
"""

from typing import Any, Dict, List, Optional
import numpy as np

NUM_LANDMARKS = 94
NUM_CHANNELS = 4

# MediaPipe Pose Landmark Indices (11, 12, 13, 14, 23, 24)
POSE_LANDMARK_MAP = {
    0: ("LEFT_SHOULDER", 11),
    1: ("RIGHT_SHOULDER", 12),
    2: ("LEFT_ELBOW", 13),
    3: ("RIGHT_ELBOW", 14),
    4: ("LEFT_HIP", 23),
    5: ("RIGHT_HIP", 24),
}
POSE_INDICES = [11, 12, 13, 14, 23, 24]

# Hand Landmarks: 21 per hand (wrist + 4 joints * 5 fingers)
HAND_LANDMARK_COUNT = 21
LEFT_HAND_RANGE = (6, 27)
RIGHT_HAND_RANGE = (27, 48)

# MediaPipe Face Mesh Indices
FACE_LIPS = [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 409, 270, 95, 88, 178, 87, 14, 78, 308]
FACE_EYES = [33, 133, 160, 158, 153, 144, 145, 246, 362, 263, 387, 385, 380, 373, 374, 249]
FACE_EYEBROWS = [107, 66, 105, 63, 70, 336, 296, 334, 293, 300]
FACE_INDICES = FACE_LIPS + FACE_EYES + FACE_EYEBROWS

LIPS_RANGE = (48, 68)
EYES_RANGE = (68, 84)
EYEBROWS_RANGE = (84, 94)

GROUP_SLICES = {
    "pose": slice(0, 6),
    "left_hand": slice(6, 27),
    "right_hand": slice(27, 48),
    "lips": slice(48, 68),
    "eyes": slice(68, 84),
    "eyebrows": slice(84, 94),
}


def get_landmark_group(index: int) -> str:
    """Return semantic group name for landmark index 0-93."""
    if not 0 <= index < NUM_LANDMARKS:
        raise IndexError(f"Landmark index {index} out of range [0, {NUM_LANDMARKS - 1}].")
    if index < 6:
        return "pose"
    if index < 27:
        return "left_hand"
    if index < 48:
        return "right_hand"
    if index < 68:
        return "lips"
    if index < 84:
        return "eyes"
    return "eyebrows"


def extract_holistic_frame(results: Any) -> np.ndarray:
    """
    Extract 94 landmarks from MediaPipe Holistic output.
    Returns (94, 4) float32 array [x, y, z, visibility].
    """
    kp = np.zeros((NUM_LANDMARKS, NUM_CHANNELS), dtype=np.float32)
    if results is None:
        return kp

    # 1. Pose: indices 0-5
    pose = getattr(results, "pose_landmarks", None)
    if pose and getattr(pose, "landmark", None):
        for i, idx in enumerate(POSE_INDICES):
            if idx < len(pose.landmark):
                lm = pose.landmark[idx]
                vis = getattr(lm, "visibility", 1.0)
                kp[i] = [lm.x, lm.y, lm.z, vis]

    # 2. Left Hand: indices 6-26
    lh = getattr(results, "left_hand_landmarks", None)
    if lh and getattr(lh, "landmark", None):
        for i in range(min(HAND_LANDMARK_COUNT, len(lh.landmark))):
            lm = lh.landmark[i]
            kp[6 + i] = [lm.x, lm.y, lm.z, 1.0]

    # 3. Right Hand: indices 27-47
    rh = getattr(results, "right_hand_landmarks", None)
    if rh and getattr(rh, "landmark", None):
        for i in range(min(HAND_LANDMARK_COUNT, len(rh.landmark))):
            lm = rh.landmark[i]
            kp[27 + i] = [lm.x, lm.y, lm.z, 1.0]

    # 4. Face (Lips, Eyes, Eyebrows): indices 48-93
    face = getattr(results, "face_landmarks", None)
    if face and getattr(face, "landmark", None):
        for i, idx in enumerate(FACE_INDICES):
            if idx < len(face.landmark):
                lm = face.landmark[idx]
                vis = 1.0 if lm.z > -0.5 else 0.5
                kp[48 + i] = [lm.x, lm.y, lm.z, vis]

    return kp

