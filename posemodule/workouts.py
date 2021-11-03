import datetime
from abc import ABC, abstractmethod
from enum import Enum
from .pose import PoseDetector
from .camera import Resolution
from log.logconfig import logger
from database import *


class States(Enum):
    UP = 1
    DOWN = 2


class Workout(ABC):

    def __init__(self, repetition_goals: int, resolution: Resolution):
        self._repetitions = 0
        self.repetition_goals = repetition_goals
        self.resolution = resolution
        self._failure_alerted = False
        self.observer = None
        self.workout_id = self._generate_id()

    @staticmethod
    def _generate_id():
        return get_max_workout_id() + 1

    def get_repetitions(self):
        return self._repetitions

    def get_current_workout(self):
        return self.__class__.__name__

    @abstractmethod
    def start_workout(self):
        pass

    def subscribe_observer(self, observer):
        self.observer = observer


class BicepCurls(Workout):
    def __init__(self, repetition_goals: int, resolution):
        super().__init__(repetition_goals, resolution)
        self.relevant_points = (12, 14, 16)
        self.state_list = [States.UP]

    def start_workout(self, pose_landmarks):
        pose_landmarks = PoseDetector.get_landmarks_dict(pose_landmarks)
        self.failure_check(pose_landmarks)
        if all(idx in pose_landmarks.keys() for idx in self.relevant_points):
            points = tuple((int(pose_landmarks[idx].x * self.resolution.width),
                            int(pose_landmarks[idx].y * self.resolution.height)) for idx in self.relevant_points)

            angle = PoseDetector.get_angle(points)
            self.determine_state(angle)
            self.increase_repetitions()

    def determine_state(self, angle: float):
        if angle > 310 and (self.state_list[-1] == States.DOWN):
            self.state_list.append(States.UP)
        elif angle < 200 and (self.state_list[-1] == States.UP):
            self.state_list.append(States.DOWN)

    def increase_repetitions(self):
        if len(self.state_list) >= 3:
            if (self.state_list[0] == self.state_list[2]) and (self.state_list[1] != self.state_list[0]):
                self._repetitions += 1
                self._failure_alerted = False
            else:
                # raise Exception("Wrong workout")
                print("Wrong Workout")
            last_state = self.state_list[-1]
            self.state_list.clear()
            self.state_list.append(last_state)
            print(self._repetitions)

    def failure_check(self, pose_landmarks):
        if not self._failure_alerted:
            try:
                points = PoseDetector.convert_points_index_to_screen_coordinates(self.resolution,
                                                                                 pose_landmarks,
                                                                                 (14, 12, 24))
            except Exception as ex:
                logger.warning(str(ex))
            else:
                angle_14_12_24 = PoseDetector.get_angle(points)

                if angle_14_12_24 < (360-25):
                    self.observer.notify("Failure: Hold your arms closer to your body.", self.workout_id,
                                         datetime.datetime.now())
                    self._failure_alerted = True



