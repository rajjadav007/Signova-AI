"""
Unit tests for ISLiM landmark mapping and grouping.
"""

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
import numpy as np

# Ensure research/ISLiM is on sys.path
TEST_DIR = Path(__file__).resolve().parent
PROJECT_DIR = TEST_DIR.parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from preprocessing.landmark_mapping import (
    NUM_LANDMARKS,
    NUM_CHANNELS,
    POSE_INDICES,
    FACE_LIPS,
    FACE_EYES,
    FACE_EYEBROWS,
    FACE_INDICES,
    GROUP_SLICES,
    get_landmark_group,
    extract_holistic_frame,
)


class TestLandmarkMapping(unittest.TestCase):
    def test_landmark_counts_and_totals(self):
        self.assertEqual(len(POSE_INDICES), 6)
        self.assertEqual(len(FACE_LIPS), 20)
        self.assertEqual(len(FACE_EYES), 16)
        self.assertEqual(len(FACE_EYEBROWS), 10)
        self.assertEqual(len(FACE_INDICES), 46)
        # 6 pose + 21 LH + 21 RH + 46 face = 94
        self.assertEqual(6 + 21 + 21 + 46, NUM_LANDMARKS)
        self.assertEqual(NUM_LANDMARKS, 94)
        self.assertEqual(NUM_CHANNELS, 4)

    def test_group_slices(self):
        self.assertEqual(GROUP_SLICES["pose"], slice(0, 6))
        self.assertEqual(GROUP_SLICES["left_hand"], slice(6, 27))
        self.assertEqual(GROUP_SLICES["right_hand"], slice(27, 48))
        self.assertEqual(GROUP_SLICES["lips"], slice(48, 68))
        self.assertEqual(GROUP_SLICES["eyes"], slice(68, 84))
        self.assertEqual(GROUP_SLICES["eyebrows"], slice(84, 94))

    def test_get_landmark_group(self):
        self.assertEqual(get_landmark_group(0), "pose")
        self.assertEqual(get_landmark_group(5), "pose")
        self.assertEqual(get_landmark_group(6), "left_hand")
        self.assertEqual(get_landmark_group(26), "left_hand")
        self.assertEqual(get_landmark_group(27), "right_hand")
        self.assertEqual(get_landmark_group(47), "right_hand")
        self.assertEqual(get_landmark_group(48), "lips")
        self.assertEqual(get_landmark_group(67), "lips")
        self.assertEqual(get_landmark_group(68), "eyes")
        self.assertEqual(get_landmark_group(83), "eyes")
        self.assertEqual(get_landmark_group(84), "eyebrows")
        self.assertEqual(get_landmark_group(93), "eyebrows")

        with self.assertRaises(IndexError):
            get_landmark_group(-1)
        with self.assertRaises(IndexError):
            get_landmark_group(94)

    def test_extract_holistic_frame_none(self):
        kp = extract_holistic_frame(None)
        self.assertEqual(kp.shape, (94, 4))
        self.assertTrue((kp == 0.0).all())
        self.assertEqual(kp.dtype, np.float32)

    def test_extract_holistic_frame_mock(self):
        def make_lm(x, y, z, vis=0.9):
            return SimpleNamespace(x=x, y=y, z=z, visibility=vis)

        pose_lm = [make_lm(0.1 * i, 0.2 * i, 0.3 * i, 0.8) for i in range(33)]
        hand_lm = [make_lm(0.5, 0.6, 0.7) for _ in range(21)]
        face_lm = [make_lm(0.8, 0.9, -0.2) for _ in range(468)]

        results = SimpleNamespace(
            pose_landmarks=SimpleNamespace(landmark=pose_lm),
            left_hand_landmarks=SimpleNamespace(landmark=hand_lm),
            right_hand_landmarks=SimpleNamespace(landmark=hand_lm),
            face_landmarks=SimpleNamespace(landmark=face_lm),
        )

        kp = extract_holistic_frame(results)
        self.assertEqual(kp.shape, (94, 4))

        # Pose: index 0 is left shoulder (mp index 11)
        np.testing.assert_allclose(kp[0, :3], [0.1 * 11, 0.2 * 11, 0.3 * 11], rtol=1e-5)
        self.assertAlmostEqual(float(kp[0, 3]), 0.8, places=5)

        # Left hand: visibility set to 1.0
        self.assertTrue((kp[6:27, 3] == 1.0).all())
        np.testing.assert_allclose(kp[6, :3], [0.5, 0.6, 0.7])

        # Right hand: visibility set to 1.0
        self.assertTrue((kp[27:48, 3] == 1.0).all())

        # Face: z = -0.2 > -0.5 -> visibility is 1.0
        self.assertTrue((kp[48:94, 3] == 1.0).all())


if __name__ == "__main__":
    unittest.main()
