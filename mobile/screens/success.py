from kivy.animation import Animation
from kivy.metrics import dp
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel, MDIcon
from kivy.properties import StringProperty
from kivy.core.window import Window

class SuccessScreen(MDScreen):
    message = StringProperty("")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()
        
    def setup_ui(self):
        # Contenedor principal centrado con más padding
        layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(30),  # Aumentado el spacing entre elementos
            padding=[dp(40), dp(60)],  # Padding horizontal y vertical aumentado
            size_hint=(None, None),
            size=(Window.width, Window.height),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            md_bg_color=(1, 1, 1, 1)
        )
        
        # Contenedor para el icono con espacio adicional
        icon_container = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(160),  # Altura fija para el contenedor del icono
            padding=[0, dp(20)]  # Padding vertical para el icono
        )
        
        # Icono de tick
        self.tick_icon = MDIcon(
            icon="check-circle",
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(None, None),
            size=(dp(0), dp(0)),
            theme_text_color="Custom",
            text_color=(0, 0.7, 0, 1)
        )
        
        icon_container.add_widget(self.tick_icon)
        
        # Contenedor para los mensajes
        message_container = MDBoxLayout(
            orientation='vertical',
            spacing=dp(20),  # Espacio entre los mensajes
            size_hint_y=None,
            height=dp(150),  # Altura fija para los mensajes
            padding=[dp(20), 0]  # Padding horizontal para los mensajes
        )
        
        # Mensaje principal
        self.message_label = MDLabel(
            text="¡Usuario registrado correctamente!",
            halign='center',
            theme_text_color="Primary",
            font_style='H5',
            opacity=0,
            size_hint_y=None,
            height=dp(60)
        )
        
        # Mensaje secundario
        self.submessage_label = MDLabel(
            text="Por favor, inicia sesión para continuar",
            halign='center',
            theme_text_color="Secondary",
            font_style='Body1',
            opacity=0,
            size_hint_y=None,
            height=dp(40)
        )
        
        message_container.add_widget(self.message_label)
        message_container.add_widget(self.submessage_label)
        
        # Espaciador superior (más espacio)
        layout.add_widget(MDBoxLayout(size_hint_y=0.25))
        
        # Agregar los contenedores principales
        layout.add_widget(icon_container)
        layout.add_widget(message_container)
        
        # Espaciador inferior (más espacio)
        layout.add_widget(MDBoxLayout(size_hint_y=0.35))
        
        self.add_widget(layout)
    
    def on_enter(self):
        # Animación del tick (un poco más grande)
        anim_tick = Animation(
            size=(dp(140), dp(140)),  # Tamaño aumentado
            duration=0.4,  # Duración ligeramente más larga
            t='out_back'
        )
        
        # Animación de los mensajes (un poco más suave)
        anim_message = Animation(opacity=1, duration=0.4)
        
        # Ejecutar animaciones en secuencia
        anim_tick.start(self.tick_icon)
        Clock.schedule_once(lambda dt: anim_message.start(self.message_label), 0.3)
        Clock.schedule_once(lambda dt: anim_message.start(self.submessage_label), 0.5)
        
        # Un poco más de tiempo antes de redirigir
        Clock.schedule_once(self.go_to_login, 3)
    
    def go_to_login(self, dt):
        self.manager.current = 'login'
