from posemodule.pose import PoseDetector
from posemodule.frame import FrameProcessor
from posemodule.camera import CameraFeed
from posemodule.workouts import BicepCurls
from gui.app import AIWorkoutApp


def main():
    camera_feed = CameraFeed("videos/Untitled.mp4")
    pose_detector = PoseDetector(model_complexity=1)
    workout_type = BicepCurls(10, camera_feed.get_resolution())
    frame_processor = FrameProcessor(camera_feed.get_resolution(), pose_detector, workout_type)
    app = AIWorkoutApp(frame_processor, camera_feed)
    app.run()


if __name__ == "__main__":
    main()
