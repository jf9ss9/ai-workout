import cv2
import math
import mediapipe as mp
from typing import Tuple, List, Optional


class PoseDetector:
    def __init__(self, image_mode=False, model_complexity=1, smooth_landmarks=True,
                 min_detection_confidence=0.5, min_tracking_confidence=0.5):

        self.pose = mp.solutions.pose.Pose(image_mode, model_complexity, smooth_landmarks,
                                           min_detection_confidence, min_tracking_confidence)

    def find_pose(self, image):
        """
        Method used to extract the pose from the given image/ frame

        :param image: Image to extract the pose from
        :return: Pose landmarks which may be empty if no landmark was found
        """
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pose_landmarks = self.pose.process(img_rgb).pose_landmarks

        return pose_landmarks

    @staticmethod
    def get_landmarks_dict(pose_landmarks, ignored_landmarks: Optional[List[int]] = None) -> dict:
        """
        Method to convert MediaPipe' s pose landmarks to dictionary containing their indexes too

        :param pose_landmarks: Pose Landmarks from the processed frame
        :param ignored_landmarks: List containing the indexes of the landmark points to be ignored
        :return: Returns a dictionary containing the landmarks and their indexes as keys. See MediaPipe docu.
        """
        if pose_landmarks is None:
            return {}
        if ignored_landmarks is None:
            ignored_landmarks = []

        return {int(index): lmark for index, lmark in enumerate(pose_landmarks.landmark)
                if index not in ignored_landmarks}

    @staticmethod
    def get_angle(points: Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]]) -> float:
        """
        Static method for extracting the angle between 3 points

        :param points: Tuple containing the 3 points' s coordinates as a tuple
        :return: The angle between the 3 points in degrees
        """
        a, b, c = points
        ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))

        return ang + 360 if ang < 0 else ang
