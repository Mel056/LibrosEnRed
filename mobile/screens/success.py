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
            spacing=dp(30),
            padding=[dp(40), dp(60)],
            size_hint=(None, None),
            size=(Window.width, Window.height),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            md_bg_color=(1, 1, 1, 1)
        )
        
        # Contenedor para el icono con espacio adicional
        icon_container = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(400),
            padding=[0, dp(20)]
        )
        
        # Icono de tick más grande
        self.tick_icon = MDIcon(
            icon="check-circle",
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            font_style="Icon",  # Aseguramos que use el estilo de icono
            font_size="250sp",  # Usamos sp en lugar de dp para el tamaño de fuente
            theme_text_color="Custom",
            text_color=(0, 0.7, 0, 1)
        )
        
        icon_container.add_widget(self.tick_icon)
        
        # Contenedor para los mensajes con más espacio
        message_container = MDBoxLayout(
            orientation='vertical',
            spacing=dp(20),
            size_hint=(0.6, None),
            height=dp(150),
            padding=[dp(20), 0],
            pos_hint={'center_x': 0.5}
        )
        
        # Mensaje principal con wrapping y padding adicional
        self.message_label = MDLabel(
            text="¡Usuario registrado correctamente!",
            halign='center',
            theme_text_color="Primary",
            font_style='H5',
            opacity=0,
            size_hint_y=None,
            height=dp(60),
            text_size=(dp(300), None),
            shorten=False,
            markup=True,
            valign='middle',
            padding=[dp(20), 0]
        )
        
        # Mensaje secundario con wrapping
        self.submessage_label = MDLabel(
            text="Por favor, inicia sesión para continuar",
            halign='center',
            theme_text_color="Secondary",
            font_style='Body1',
            opacity=0,
            size_hint_y=None,
            height=dp(40),
            text_size=(dp(300), None),
            shorten=False,
            markup=True,
            valign='middle',
            padding=[dp(20), 0]
        )
        
        message_container.add_widget(self.message_label)
        message_container.add_widget(self.submessage_label)
        
        # Espaciador superior
        layout.add_widget(MDBoxLayout(size_hint_y=0.2))
        
        # Agregar los contenedores principales
        layout.add_widget(icon_container)
        layout.add_widget(message_container)
        
        # Espaciador inferior
        layout.add_widget(MDBoxLayout(size_hint_y=0.3))
        
        self.add_widget(layout)

    def on_enter(self):
        # Solo animamos la opacidad para los mensajes
        anim_message = Animation(opacity=1, duration=0.4)
        
        # Ejecutar animaciones en secuencia
        Clock.schedule_once(lambda dt: anim_message.start(self.message_label), 0.3)
        Clock.schedule_once(lambda dt: anim_message.start(self.submessage_label), 0.5)
        
        # Tiempo antes de redirigir
        Clock.schedule_once(self.go_to_login, 3)
    
    def go_to_login(self, dt):
        self.manager.current = 'login'
