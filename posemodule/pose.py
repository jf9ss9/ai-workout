import mediapipe as mp
import cv2
import math
from typing import Tuple, List, Optional


class PoseDetector:
    def __init__(self, image_mode=False, model_complexity=1, smooth_landmarks=True,
                 min_detection_confidence=0.5, min_tracking_confidence=0.5):

        self.pose = mp.solutions.pose.Pose(image_mode, model_complexity, smooth_landmarks,
                                           min_detection_confidence, min_tracking_confidence)

    def find_pose(self, image):
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pose_landmarks = self.pose.process(img_rgb).pose_landmarks

        return pose_landmarks

    @staticmethod
    def get_landmarks_dict(pose_landmarks, ignored_landmarks: Optional[List[float]] = None) -> dict:
        if pose_landmarks is None:
            return {}
        if ignored_landmarks is None:
            ignored_landmarks = []

        return {int(index): lmark for index, lmark in enumerate(pose_landmarks.landmark)
                if index not in ignored_landmarks}

    @staticmethod
    def get_angle(points: Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]]) -> float:
        a, b, c = points
        ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))

        return ang if ang < 0 else ang
