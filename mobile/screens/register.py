import re
from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton


class RegisterScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()
    
    def setup_ui(self):
        layout = MDBoxLayout(
            orientation='vertical', 
            padding=(dp(20), dp(50)), 
            spacing=dp(20),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        # Título
        title = MDLabel(
            text='Registro', 
            font_style='H4',
            halign='center',
            theme_text_color='Primary'
        )
        
        # Campo de usuario
        self.username = MDTextField(
            hint_text='Nombre de Usuario',
            mode='rectangle',
            icon_left='account',
            size_hint_x=None,
            width=dp(300),
            pos_hint={'center_x': 0.5}
        )
        
        # Campo de email
        self.email = MDTextField(
            hint_text='Correo Electrónico',
            mode='rectangle',
            icon_left='email',
            size_hint_x=None,
            width=dp(300),
            pos_hint={'center_x': 0.5}
        )
        
        # Campo de contraseña
        self.password = MDTextField(
            hint_text='Contraseña',
            mode='rectangle',
            password=True,
            icon_left='lock',
            size_hint_x=None,
            width=dp(300),
            pos_hint={'center_x': 0.5}
        )
        
        # Botón de continuar
        continue_btn = MDRaisedButton(
            text='Continuar',
            size_hint_x=None,
            width=dp(300),
            pos_hint={'center_x': 0.5},
            on_release=self.validate_and_proceed
        )
        
        # Agregar widgets al layout
        layout.add_widget(title)
        layout.add_widget(self.username)
        layout.add_widget(self.email)
        layout.add_widget(self.password)
        layout.add_widget(continue_btn)
        
        self.add_widget(layout)
    
    def validate_and_proceed(self, instance):
        # Validaciones básicas
        username = self.username.text.strip()
        email = self.email.text.strip()
        password = self.password.text.strip()
        
        # Validar username
        if not username or len(username) < 3:
            self.show_error("Nombre de usuario debe tener al menos 3 caracteres")
            return
        
        # Validar email
        if not self.is_valid_email(email):
            self.show_error("Por favor ingrese un correo electrónico válido")
            return
        
        # Validar contraseña
        if not self.is_valid_password(password):
            self.show_error("La contraseña debe tener al menos 6 caracteres")
            return
        
        # Configura el mensaje de éxito antes de proceder a la ubicación
        success_screen = self.manager.get_screen('success')
        success_screen.show_success(
            "¡Usuario registrado correctamente!",
            "Por favor, inicia sesión para continuar",
            'login'
        )
        
        # Ir a la pantalla de selección de ubicación
        self.manager.get_screen('location_select').set_registration_data(
            username, email, password
        )
        self.manager.current = 'location_select'
    
    def is_valid_email(self, email):
        # Regex simple para validación de email
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None
    
    def is_valid_password(self, password):
        # Validación básica de contraseña
        return len(password) >= 6
    
    def show_error(self, message):
        # Mostrar diálogo de error
        dialog = MDDialog(
            title="Error de Registro",
            text=message,
            buttons=[
                MDFlatButton(
                    text="OK",
                    on_release=lambda *args: dialog.dismiss()
                )
            ]
        )
        dialog.open()
