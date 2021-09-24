import cv2
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from posemodule.camera import CameraFeed
from posemodule.frame import FrameProcessor


class AIWorkoutApp(MDApp):
    def __init__(self, frame_processor: FrameProcessor, camera_feed: CameraFeed):
        super().__init__()
        self._image = Image()
        self._camera_feed = camera_feed
        self._frame_processor = frame_processor

    def on_stop(self) -> None:
        self._camera_feed.destroy()

    def build(self):
        box_layout = MDBoxLayout(orientation="vertical")
        box_layout.add_widget(self._image)
        start_btn = MDRaisedButton(text="START", pos_hint={"center_x": .5, "center_y": .5})
        start_btn.bind(on_press=self.start_animation)
        box_layout.add_widget(start_btn)

        return box_layout

    def start_animation(self, *args) -> None:
        """
        Start the workout animation then schedule the real camera feed.

        :param args: catch stuff
        """
        self._image.source = "videos/pushup.gif"
        self._image.anim_delay = 0.08
        self._image.anim_loop = 1
        self._image.remove_from_cache()
        Clock.schedule_once(self._schedule_video, timeout=0)

    def _schedule_video(self, *args) -> None:
        """
        Schedule the video/ webcam after the animation at the hiven interval.

        :param args: catch stuff
        """
        Clock.schedule_interval(self._load_frame, 1.0 / 60.0)

    def _load_frame(self, *args) -> None:
        """
        Loads a frame from CameraFeed into the Image component.

        :param args: catch stuff
        """
        img_rgb = self._camera_feed.get_frame()
        if img_rgb is None:
            self.stop()
        else:
            self._frame_processor.process(img_rgb)
            buffer = cv2.flip(img_rgb, 0).tobytes()
            texture = Texture.create(size=(img_rgb.shape[1], img_rgb.shape[0]), colorfmt="bgr")
            texture.blit_buffer(buffer, colorfmt="bgr", bufferfmt="ubyte")
            self._image.texture = texture
