import time
import io
import cv2

from typing import List
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.image import Image, CoreImage
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import StringProperty
from kivy.graphics.texture import Texture
from posemodule.camera import CameraFeed
from posemodule.frame import FrameProcessor
from log.logconfig import logger
from database import *
from dataclasses import dataclass


@dataclass
class AppUser:
    id: int
    username: str
    name: str
    age: str


class HomePageWindow(Screen):
    user_name = StringProperty()


class LoginWindow(Screen):
    def login(self, username, password):
        if username == "" or password == "":
            return
        elif verify_user(username, password) is True:
            self.manager.current = "homepage"
            app = App.get_running_app()
            db_user = get_user(username)
            self.manager.get_screen("homepage").user_name = db_user.name
            app.set_user(AppUser(db_user.id, db_user.username, db_user.name, db_user.age))

    def clear(self):
        for field in (self.ids.username, self.ids.password):
            field.text = ""


class RegisterWindow(Screen):

    def register(self, username, name, age, password):
        if any(elem == "" for elem in [username, name, age, password]):
            return
        elif register_user(username, name, age, password) is True:
            self.manager.current = "homepage"

    def clear(self):
        form_fields = (self.ids.name, self.ids.age, self.ids.username, self.ids.password)
        for field in form_fields:
            field.text = ""


class ExercisesWindow(Screen):
    pass


class WorkoutWindow(Screen):
    pass


class FaultsWindow(Screen):

    @staticmethod
    def fetch_faults_from_db() -> List:
        """
        Fetches the faults from the database and returns them.
        """
        connect_to_db()
        with Session(engine) as session:
            faults = session.query(Faults)
        return faults

    def display_faults(self, faults: List) -> None:
        """
        Displays the faults fetched from the database.

        :param faults: List of faults previously fetched from the database.
        """
        screen_id = self.ids.faults_list

        for fault in faults:
            data = io.BytesIO(fault.screenshot)
            img = CoreImage(data, ext="png").texture

            image = Image()
            image.texture = img

            card = MDCard(orientation='vertical', pos_hint={
                'center_x': .5, 'center_y': .7}, size_hint=(.9, None), height=400)
            card.add_widget(image)
            card.add_widget(MDLabel(text=fault.description, halign="center", size_hint=(.6, .2), ))
            screen_id.add_widget(card)


class WindowManager(ScreenManager):
    pass


class AIWorkoutApp(MDApp):
    def __init__(self, frame_processor: FrameProcessor, camera_feed: CameraFeed):
        super().__init__()
        self._camera_feed = camera_feed
        self._frame_processor = frame_processor
        self._fault_observer = FaultObserver()
        self._frame_processor.workout.subscribe_observer(self._fault_observer)
        self.root = None
        self.user = None
        self.start_time = None
        logger.info("Application started successfully")

    def set_user(self, user: int):
        self.user = user

    def on_stop(self) -> None:
        self._camera_feed.destroy()
        workout_object = self._frame_processor.workout
        create_workout(self.user.id, workout_object.get_current_workout(),
                       workout_object.get_repetitions(), int(time.time() - self.start_time))
        self._fault_observer.workout_done()
        logger.info("Application stopped normally")

    def build(self):
        """
        Builds the application based on the .kv design file.

        :return: the built structure of Builder's load_file.
        """
        try:
            self.root = Builder.load_file(r'gui\style\app.kv')
        except Exception as ex:
            logger.critical(f"Build failed: {ex}")
            self.stop()
        else:
            logger.info("Application built successfully")

        return self.root

    def start_animation(self, *args) -> None:
        """
        Start the workout animation then schedule the real camera feed.

        :param args: catch stuff
        """
        if self.user is None:
            logger.critical("User not logged in. Houston, we got hacked.")
            self.stop()
            return
        workout_screen_image = self.root.get_screen('workout').ids.workout_image

        workout_screen_image.source = "videos/bicep_curls.gif"
        workout_screen_image.anim_delay = 0.08
        workout_screen_image.anim_loop = 1
        workout_screen_image.remove_from_cache()
        logger.info("Workout animation started")
        Clock.schedule_once(self._schedule_video, timeout=5)

    def _schedule_video(self, *args) -> None:
        """
        Schedule the video/ webcam after the animation at the hiven interval.

        :param args: catch stuff
        """
        Clock.schedule_interval(self._load_frame, 1.0 / 60.0)
        self.start_time = time.time()
        logger.info(f"Frames scheduled for the video at every {1.0 / 60.0:.4f} seconds")

    def _load_frame(self, *args) -> None:
        """
        Loads a frame from CameraFeed into the Image component.

        :param args: catch stuff
        """
        img_rgb = self._camera_feed.get_frame()
        if img_rgb is None:
            workout_object = self._frame_processor.workout
            create_workout(self.user.id, workout_object.get_current_workout(),
                           workout_object.get_repetitions(), int(time.time() - self.start_time))
            self._fault_observer.workout_done()
            self.stop()
        else:
            self._fault_observer.frame = img_rgb
            self._frame_processor.process(img_rgb)
            buffer = cv2.flip(img_rgb, 0).tobytes()
            texture = Texture.create(size=(img_rgb.shape[1], img_rgb.shape[0]), colorfmt="bgr")
            texture.blit_buffer(buffer, colorfmt="bgr", bufferfmt="ubyte")
            workout_screen_image = self.root.get_screen('workout').ids.workout_image
            workout_screen_image.texture = texture


class FaultObserver:

    def __init__(self):
        self.frame = None
        self.fault_list = []

    def notify(self, description: str, workout_id: int, date) -> None:
        print(description, workout_id, date)
        self.fault_list.append(Faults(description=description, date=date,
                                      screenshot=cv2.imencode(".png", self.frame)[1].tostring(), workout_id=workout_id))

    def workout_done(self) -> None:
        for fault in self.fault_list:
            send_in_db(fault)
