import cv2
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from posemodule.camera import CameraFeed


class AIWorkoutApp(MDApp):
    def __init__(self, frame_processor, camera_feed: CameraFeed):
        super().__init__()
        self._image = None
        self._camera_feed = camera_feed
        self._frame_processor = frame_processor

    def on_stop(self):
        self._camera_feed.destroy()

    def build(self):
        layout = MDBoxLayout(orientation="vertical")
        self._image = Image()
        layout.add_widget(self._image)
        Clock.schedule_interval(self.load_frame, 1.0 / 60.0)

        return layout

    def load_frame(self, *args):
        img_rgb = self._camera_feed.get_frame()
        if img_rgb is None:
            self.stop()
        else:
            self._frame_processor.process(img_rgb)
            buffer = cv2.flip(img_rgb, 0).tobytes()
            texture = Texture.create(size=(img_rgb.shape[1], img_rgb.shape[0]), colorfmt="bgr")
            texture.blit_buffer(buffer, colorfmt="bgr", bufferfmt="ubyte")
            self._image.texture = texture
