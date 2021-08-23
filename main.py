from posemodule.pose import PoseDetector
from posemodule.frame import FrameProcessor
from posemodule.camera import CameraFeed
from gui.app import AIWorkoutApp


def main():
    camera_feed = CameraFeed(0)
    pose_detector = PoseDetector()
    resolution = camera_feed.get_resolution()
    frame_processor = FrameProcessor(resolution[0], resolution[1], pose_detector)
    app = AIWorkoutApp(frame_processor, camera_feed)
    app.run()
"""
    pTime = 0
    cap = cv2.VideoCapture(0)
    pose_detector = PoseDetector(model_complexity=1)
    frame_width, frame_height = cap.read()[1].shape[1], cap.read()[1].shape[0]
    print(frame_width, frame_height)
    frame_processor = FrameProcessor(frame_width, frame_height, pose_detector)
    while True:
        ret, frame = cap.read()
        if frame is None:
            break
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_processor.process(img_rgb)

        cTime = time.time()
        fps = 1 // (cTime - pTime)
        pTime = cTime

        cv2.putText(frame, str(fps), (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        cv2.imshow("Webcam Input", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
"""

if __name__ == "__main__":
    main()
