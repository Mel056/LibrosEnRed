# screens/profile.py
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
import requests
from datetime import datetime

class CommentCard(MDCard):
    def __init__(self, comment_data, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(120)
        self.padding = dp(15)
        self.spacing = dp(10)
        self.md_bg_color = (0.9, 0.9, 0.9, 1)
        self.radius = [dp(10)]
        
        # Usuario que comentó
        commenter = MDLabel(
            text=comment_data.get('commenter_username', 'Usuario desconocido'),
            bold=True,
            font_style='Subtitle1'
        )
        
        # Comentario
        comment = MDLabel(
            text=comment_data.get('comment', 'Sin comentario'),
            font_style='Body1'
        )
        
        # Formatear la fecha
        date_str = comment_data.get('created_at', '')
        if date_str:
            try:
                # Parsear la fecha del formato original
                date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
                # Formatear la fecha al nuevo formato
                formatted_date = date_obj.strftime('%H:%M %d/%m/%Y')
            except ValueError:
                formatted_date = date_str
        else:
            formatted_date = ''
        
        # Fecha
        date = MDLabel(
            text=formatted_date,
            font_style='Caption',
            theme_text_color='Secondary'
        )
        
        self.add_widget(commenter)
        self.add_widget(comment)
        self.add_widget(date)

class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.2, 0.03, 0.4, 1)  # Color de fondo suave
            self.rect = Rectangle(size=Window.size)
        self.setup_ui()
        
    def setup_ui(self):
        # Layout principal
        main_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(20),
            padding=dp(16)
        )
        
        # Header con botón de retorno
        header = MDBoxLayout(
            size_hint_y=None,
            height=dp(56)
        )
        
        back_button = MDIconButton(
            icon="arrow-left",
            pos_hint={"center_y": .5},
            on_press=self.go_back,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)  # Agregar - Blanco
        )
        
        title = MDLabel(
            text="Mi Perfil",
            font_style="H5",
            pos_hint={"center_y": .5},
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)  # Agregar - Blanco
        )
        
        header.add_widget(back_button)
        header.add_widget(title)
        
        # Contenedor scrolleable para el contenido
        scroll = ScrollView()
        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(20),
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter('height'))
        
        # Información básica del usuario
        self.user_info = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(200),
            spacing=dp(10)
        )
        
        # Sección de comentarios
        comments_title = MDLabel(
            text="Comentarios recibidos",
            font_style="H6",
            size_hint_y=None,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),  # Agregar - Blanco
            height=dp(40)
        )
        
        self.comments_container = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None
        )
        self.comments_container.bind(minimum_height=self.comments_container.setter('height'))
        
        content.add_widget(self.user_info)
        content.add_widget(comments_title)
        content.add_widget(self.comments_container)
        
        scroll.add_widget(content)
        
        main_layout.add_widget(header)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def on_enter(self):
        # Cargar datos del usuario cuando se entra a la pantalla
        self.load_user_data()
    
    def load_user_data(self):
        app = MDApp.get_running_app()
        if not app.user_data:
            return
        
        try:
            response = requests.get(f'http://localhost:5001/users?id={app.user_data["user_id"]}')
            if response.status_code == 200:
                users = response.json()
                if users:
                    user = users[0]
                    # Parsear los comentarios que vienen como string JSON
                    import json
                    received_comments = json.loads(user['received_comments']) if user['received_comments'] else []
                    self.update_user_info(user)
                    self.update_comments(received_comments)
        except requests.RequestException as e:
            print(f"Error al cargar datos del usuario: {e}")

    
    def update_user_info(self, user_data):
        self.user_info.clear_widgets()

        # Crear un layout horizontal para la info y la foto
        info_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(200),
            spacing=dp(20)
        )

        # Layout vertical para la información
        text_info = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_x=0.7
        )

        # Username con título
        username_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(2),
            size_hint_y=None,
            height=dp(50)
        )
        username_layout.add_widget(MDLabel(
            text="USUARIO",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.7),
            font_style="Caption"
        ))
        username_layout.add_widget(MDLabel(
            text=user_data['username'],
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H5"
        ))

        # Email con título
        email_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(2),
            size_hint_y=None,
            height=dp(50)
        )
        email_layout.add_widget(MDLabel(
            text="EMAIL",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.7),
            font_style="Caption"
        ))
        email_layout.add_widget(MDLabel(
            text=user_data['email'],
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        ))

        # Rating con título
        try:
            rating = float(user_data['average_rating']) if user_data['average_rating'] else 0.0
            rating_text = f"{rating:.1f}"
        except (ValueError, TypeError):
            rating_text = "0.0"

        rating_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(2),
            size_hint_y=None,
            height=dp(50)
        )
        rating_layout.add_widget(MDLabel(
            text="RATING PROMEDIO",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.7),
            font_style="Caption"
        ))
        rating_layout.add_widget(MDLabel(
            text=rating_text,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        ))

        # Total libros con título
        books_layout = MDBoxLayout(
            orientation='vertical',
            spacing=dp(2),
            size_hint_y=None,
            height=dp(50)
        )
        books_layout.add_widget(MDLabel(
            text="TOTAL DE LIBROS",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 0.7),
            font_style="Caption"
        ))
        books_layout.add_widget(MDLabel(
            text=str(user_data.get('total_books', 0)),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1)
        ))

        # Agregar todos los layouts de información
        text_info.add_widget(username_layout)
        text_info.add_widget(email_layout)
        text_info.add_widget(rating_layout)
        text_info.add_widget(books_layout)

        # Layout para la foto de perfil
        photo_layout = MDBoxLayout(
            size_hint_x=0.3,
            padding=[0, dp(20)]
        )

        # Foto de perfil
        from kivy.uix.image import AsyncImage
        profile_photo = AsyncImage(
            source=user_data.get('profile_photo', user_data['profile_photo']),
            allow_stretch=True,
            keep_ratio=True
        )
        photo_layout.add_widget(profile_photo)

        # Agregar ambos layouts al layout principal
        info_layout.add_widget(text_info)
        info_layout.add_widget(photo_layout)
        
        self.user_info.add_widget(info_layout)

    def update_comments(self, comments):
        self.comments_container.clear_widgets()
        
        if not comments or len(comments) == 0:
            self.comments_container.add_widget(MDLabel(
                text="No hay comentarios aún",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                halign="center"
            ))
            return
        
        # Los comentarios vienen en un formato JSON, necesitamos parsearlo
        for comment in comments:
            self.comments_container.add_widget(CommentCard(comment))
    
    def go_back(self, instance):
        self.manager.current = 'home'
