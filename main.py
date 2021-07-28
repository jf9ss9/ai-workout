import cv2
import time
from posemodule.pose import PoseDetector
from posemodule.frame import FrameProcessor


def main():
    pTime = 0
    cap = cv2.VideoCapture("fiftypullups.mp4")
    pose_detector = PoseDetector(model_complexity=1)
    frame_width, frame_height = cap.read()[1].shape[1], cap.read()[1].shape[0]
    frame_processor = FrameProcessor(frame_width, frame_height)
    while True:
        ret, frame = cap.read()
        if frame is None:
            break
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        landmarks = pose_detector.find_pose(img_rgb)
        frame_processor.draw_landmarks(frame, landmarks, ignored_landmarks=set(range(33))-set([12,14,16,11,13,15]))
        frame_processor.draw_angle(frame, landmarks, points_index=(12, 14, 16))

        cTime = time.time()
        fps = 1 // (cTime - pTime)
        pTime = cTime

        cv2.putText(frame, str(fps), (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        cv2.imshow("Webcam Input", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
