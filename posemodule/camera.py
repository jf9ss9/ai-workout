import cv2


class CameraFeed:
    def __init__(self, source):
        self._capture = cv2.VideoCapture(source)
        self.frame_width = self._capture.read()[1].shape[1]
        self.frame_height = self._capture.read()[1].shape[0]

    def get_resolution(self):
        """
        Method used to get the resolution of the camera feed.

        :return: a tuple containing the width and the height in this order.
        """

        return self.frame_width, self.frame_height

    def get_frame(self):
        """
        Method used to get the current frame from the camera feed/ source.

        :return: current frame.
        """
        ret, frame = self._capture.read()
        if frame is not None:
            cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

    def destroy(self) -> None:
        """
        Destructor type method. Makes sure everything is closed/ released properly.
        """
        self._capture.release()
        cv2.destroyAllWindows()
