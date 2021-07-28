import cv2
import mediapipe as mp
import posemodule.pose as pose
from .constants import POSE_CONNECTIONS
from typing import Tuple


class FrameProcessor:
    def __init__(self, width, height):
        self._width = width
        self._height = height

    def draw_landmarks(self, frame, pose_landmarks, cv2_mode=True, ignored_landmarks=None) -> None:
        if ignored_landmarks is None:
            ignored_landmarks = []
        if not cv2_mode:
            mp.solutions.drawing_utils.draw_landmarks(frame, pose_landmarks, POSE_CONNECTIONS)
        else:
            landmarks_dict = pose.PoseDetector.get_landmarks_dict(pose_landmarks, ignored_landmarks)
            self.__draw_landmarks_cv2(frame, landmarks_dict, POSE_CONNECTIONS)

    def __draw_landmarks_cv2(self, frame, landmarks, pose_connections) -> None:
        for connection in pose_connections:
            lmpoint_1, lmpoint_2 = connection[0].value, connection[1].value
            if (lmpoint_1 in landmarks) and (lmpoint_2 in landmarks):
                x_1, y_1 = int(landmarks[lmpoint_1].x * self._width), \
                           int(landmarks[lmpoint_1].y * self._height)
                x_2, y_2 = int(landmarks[lmpoint_2].x * self._width), \
                           int(landmarks[lmpoint_2].y * self._height)
                cv2.line(frame, (x_1, y_1), (x_2, y_2), (0, 255, 0), 2)

        for lm_id, landmark in landmarks.items():
            x_scaled, y_scaled = int(landmark.x * self._width), int(landmark.y * self._height)
            cv2.circle(frame, (x_scaled, y_scaled), 5, (0, 0, 255), cv2.FILLED)

    def draw_angle(self, frame, pose_landmarks, points_index: Tuple[int, int, int], emphasize_points: bool = True):
        # If pose_landmarks is not a dictionary returned by PoseDetector.get_landmarks_dict, then convert it
        if type(pose_landmarks) is not dict:
            pose_landmarks = pose.PoseDetector.get_landmarks_dict(pose_landmarks)

        # Draw points/ angles only if the pose detector detected them
        if all(idx in pose_landmarks.keys() for idx in points_index):
            points = tuple((int(pose_landmarks[idx].x * self._width),
                            int(pose_landmarks[idx].y * self._height)) for idx in points_index)

            angle = pose.PoseDetector.get_angle(points)
            if emphasize_points:
                for point in points:
                    cv2.circle(frame, point, 10, (255, 0, 0), 2)
            cv2.putText(frame, str(int(angle)), points[1], cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
