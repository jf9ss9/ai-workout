import datetime

import cv2
import mediapipe as mp
import posemodule.pose as pose
from typing import Tuple
from .constants import POSE_CONNECTIONS
from .pose import PoseDetector
from .workouts import BicepCurls
from .camera import Resolution


class FrameProcessor:

    def __init__(self, resolution: Resolution, pose_detector: PoseDetector, workout: BicepCurls):
        self._width = resolution.width
        self._height = resolution.height
        self._pose_detector = pose_detector
        self.workout = workout

    def draw_landmarks(self, frame, pose_landmarks, cv2_mode=True, ignored_landmarks=None) -> None:
        """
        Method used for drawing the pose on a frame.

        :param frame: The frame/ image to draw on
        :param pose_landmarks: Pose landmarks from the processed frame
        :param cv2_mode: By default True. If False, MediaPipe's own drawing module is used
        :param ignored_landmarks: Landmarks to be ignored when drawing the points
        """
        if ignored_landmarks is None:
            ignored_landmarks = []
        if not cv2_mode:
            mp.solutions.drawing_utils.draw_landmarks(frame, pose_landmarks, POSE_CONNECTIONS)
        else:
            landmarks_dict = pose.PoseDetector.get_landmarks_dict(pose_landmarks, ignored_landmarks)
            self.__draw_landmarks_cv2(frame, landmarks_dict, POSE_CONNECTIONS)

    def __draw_landmarks_cv2(self, frame, landmarks, pose_connections) -> None:
        """
        Private method for self.draw_landmark's cv2 mode.

        :param frame: The frame/ image to draw on
        :param landmarks: Dictionary containing the landmarks and their indexes
        :param pose_connections: The graph representing the connections
        """
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
        """
        Method used for drawing the angle and to highlight the 3 points.

        :param frame: The frame/ image to draw on
        :param pose_landmarks: Pose landmarks from the processed frame
        :param points_index: The landmark points to get the angle from. See MediaPipe docu.
        :param emphasize_points: By default True. If False, the processed points are not highlighted
        """
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

    def draw_repetitions(self, frame):
        cv2.putText(frame, str(self.workout.get_repetitions()), (400, 200), cv2.FONT_HERSHEY_PLAIN, 8, (0, 0, 255), 8)

    def process(self, frame) -> None:
        """
        "ETL" type of method used to process a frame (extract, transform, load). \n
        The landmarks are extracted from the frame, then FrameProcessor's draw_landmark is called
        followed by the draw_angle method.

        :param frame: The frame/ image to process/ draw/ transform
        """

        landmarks = self._pose_detector.find_pose(frame)
        self.draw_landmarks(frame, landmarks, ignored_landmarks=(range(11)))
        self.draw_angle(frame, landmarks, points_index=(23, 25, 27))
        self.workout.start_workout(landmarks)
        self.draw_repetitions(frame)



