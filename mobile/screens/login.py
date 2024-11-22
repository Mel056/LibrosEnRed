# screens/login.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()
    
    def setup_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Logo placeholder
        logo = Label(
            text='📚 Book Exchange',
            font_size='24sp',
            size_hint_y=None,
            height=100
        )
        
        # Input fields
        self.username = TextInput(
            multiline=False,
            hint_text='Usuario',
            size_hint_y=None,
            height=40,
            padding=[10, 10, 10, 10]
        )
        self.password = TextInput(
            multiline=False,
            hint_text='Contraseña',
            password=True,
            size_hint_y=None,
            height=40,
            padding=[10, 10, 10, 10]
        )
        
        # Login button
        login_btn = Button(
            text='Iniciar Sesión',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.6, 1, 1)
        )
        login_btn.bind(on_press=self.login)
        
        # Add widgets to layout
        layout.add_widget(logo)
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(login_btn)
        
        self.add_widget(layout)
    
    def login(self, instance):
        username = self.username.text
        password = self.password.text
        # Aquí irá la lógica de autenticación
        print(f"Intento de login con usuario: {username}")
        self.manager.current = 'main'
