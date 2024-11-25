import cv2
import numpy as np
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from pyzbar.pyzbar import decode

class QRCodeScanner(Screen):
    def __init__(self, **kwargs):
        super(QRCodeScanner, self).__init__(**kwargs)
        self.setup_ui()
        self.capture = None
        self.img = Image(size=self.size)
        self.add_widget(self.img)
        
    def setup_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20)
        
        # Back button
        back_btn = Button(
            text='Volver',
            size_hint_y=None,
            height=50
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        
        layout.add_widget(back_btn)
        
    def on_enter(self):
        # Activa la camara cuando entra a la screen
        if not self.capture:
            self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def on_leave(self):
        # Desactiva la camara cuando sale de la screen
        if self.capture:
            self.capture.release()
            self.capture = None
        Clock.unschedule(self.update)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # Convierte lo que hay en la camara
            texture = self.convert_frame_to_texture(frame)
            self.img.texture = texture

            # Decode lo que hay en la camara
            decoded_objects = decode(frame)
            for obj in decoded_objects:
                # Infromacion del QR
                print(f'Decoded Data: {obj.data.decode("utf-8")}')

    def convert_frame_to_texture(self, frame):
        # Da vuelta la imagen
        frame = cv2.flip(frame, 0) # eje x
        frame = cv2.flip(frame, 1) # eje y
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Convert the frame to a texture
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
        texture.blit_buffer(frame_rgb.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
        return texture

