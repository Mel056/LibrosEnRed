# screens/login.py
import requests
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.screen import MDScreen


class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()
    
    def setup_ui(self):
        # Configuración del layout principal
        layout = BoxLayout(
            orientation='vertical', 
            padding=(dp(20), dp(50)), 
            spacing=dp(20),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        # Logo y título
        title = Label(
            text='Libros En Red', 
            font_size=dp(32), 
            color=(0.2, 0.2, 0.2, 1),
            size_hint_y=None, 
            height=dp(100)
        )
        
        # Campos de texto estilizados
        self.username = MDTextField(
            hint_text='Usuario',
            mode='rectangle',
            icon_left='account',
            size_hint_x=None,
            width=dp(300),
            pos_hint={'center_x': 0.5}
        )
        
        self.password = MDTextField(
            hint_text='Contraseña',
            mode='rectangle',
            password=True,
            icon_left='lock',
            size_hint_x=None,
            width=dp(300),
            pos_hint={'center_x': 0.5}
        )
        
        # Botón de inicio de sesión
        login_btn = MDRaisedButton(
            text='Iniciar Sesión',
            md_bg_color=(0.2, 0.6, 1, 1),
            size_hint_x=None,
            width=dp(300),
            pos_hint={'center_x': 0.5},
            on_release=self.login
        )
        
        # Botón de registro
        register_btn = MDRaisedButton(
            text='Registrarse',
            md_bg_color=(0.4, 0.4, 0.4, 1),
            text_color=(1, 1, 1, 1),
            size_hint_x=None,
            width=dp(300),
            pos_hint={'center_x': 0.5},
            on_release=self.go_to_register
        )
        
        # Agregar widgets al layout
        layout.add_widget(title)
        layout.add_widget(self.username)
        layout.add_widget(self.password)
        layout.add_widget(login_btn)
        layout.add_widget(register_btn)
        
        self.add_widget(layout)
    
    def login(self, instance):
        username = self.username.text
        password = self.password.text
        
        try:
            # Llamada a la API de login
            response = requests.post('http://localhost:5001/login', json={
                'username': username,
                'password': password
            })
            
            if response.status_code == 200:
                # Login exitoso
                print("Login exitoso")
                self.manager.current = 'home'
            else:
                # Manejar error de login
                print("Credenciales incorrectas")

        except requests.RequestException as e:
            print(f"Error de conexión: {e}")
    
    def go_to_register(self, instance):
        try:
            # Navegar a la pantalla de registro o abrir diálogo de registro
            self.manager.current = 'register'
        except Exception as e:
            print(f"Error al navegar: {e}")

# Nota: Este código asume que tienes kivymd instalado
# Necesitarás instalar: pip install kivymd requests
