from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.core.window import Window
from kivymd.uix.button import MDIconButton
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
import requests


class ResponsiveView:
    """Mixin para manejar diseño responsivo"""
    def get_responsive_value(self, mobile_value, tablet_value, desktop_value):
        width = Window.width
        if width < dp(600):  # Mobile
            return dp(mobile_value)
        elif width < dp(1024):  # Tablet
            return dp(tablet_value)
        else:  # Desktop
            return dp(desktop_value)

class StarButton(MDIconButton):
    def __init__(self, rating_value, is_filled=False, **kwargs):
        super().__init__(**kwargs)
        self.rating_value = rating_value
        self.icon = 'star' if is_filled else 'star-outline'
        self.theme_text_color = "Custom"
        self.text_color = (1, 0.8, 0, 1) if is_filled else (0.7, 0.7, 0.7, 1)
        self.size = (dp(40), dp(40))
        self.size_hint = (None, None)

class InteractiveStarRating(BoxLayout):
    def __init__(self, book_id, **kwargs):
        super().__init__(**kwargs)
        self.book_id = book_id
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(60)
        self.spacing = dp(5)
        self.stars = []
        
        # Main container for centering
        center_layout = AnchorLayout(
            anchor_x='center',
            anchor_y='center',
            size_hint_x=1
        )
        
        # Container for the stars with fixed width
        stars_container = BoxLayout(
            orientation='horizontal',
            size_hint=(None, None),
            height=dp(60),
            width=dp(250),
            spacing=dp(10),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        # Create empty stars
        for i in range(5):
            star = StarButton(
                rating_value=i + 1,
                is_filled=False,  # Initialize all stars as empty
                on_press=self.on_star_press
            )
            self.stars.append(star)
            stars_container.add_widget(star)
        
        center_layout.add_widget(stars_container)
        self.add_widget(center_layout)
    
    def on_star_press(self, star_button):
        rating_value = star_button.rating_value
        app = MDApp.get_running_app()
        
        if not app.user_data:
            print("Error: Usuario no logueado")
            return
        
        # Actualizar visualmente las estrellas
        for i, star in enumerate(self.stars):
            is_filled = i < rating_value
            star.icon = 'star' if is_filled else 'star-outline'
            star.text_color = (1, 0.8, 0, 1) if is_filled else (0.7, 0.7, 0.7, 1)
        
        # Enviar calificación a la API
        try:
            response = requests.post('http://localhost:5001/rating/books', json={
                'book_id': self.book_id,
                'rater_id': app.user_data['user_id'],  # Usar el ID del usuario logueado
                'rating': rating_value
            })
            
            if response.status_code == 200:
                print("Calificación guardada exitosamente")
            else:
                print(f"Error al guardar la calificación: {response.status_code}")
                
        except requests.RequestException as e:
            print(f"Error de conexión: {e}")

class AvailabilityBadge(AnchorLayout):
    def __init__(self, is_available, **kwargs):
        super().__init__(**kwargs)
        self.anchor_x = 'center'
        self.size_hint_y = None
        self.height = dp(40)
        
        bg_color = (0.2, 0.8, 0.2, 1) if is_available else (0.8, 0.2, 0.2, 1)
        text = "Disponible" if is_available else "No Disponible"
        
        # Contenedor con fondo de color
        self.container = BoxLayout(
            size_hint=(None, None),
            padding=[dp(20), dp(8)],
            height=dp(40)
        )
        
        # Label
        self.label = Label(
            text=text,
            color=(1, 1, 1, 1),
            bold=True,
            size_hint=(None, None),
            font_size=dp(16)
        )
        
        # Forzar actualización del tamaño del label
        self.label.texture_update()
        self.label.size = self.label.texture_size
        
        # Ajustar el tamaño del contenedor al contenido
        self.container.width = self.label.width + dp(40)
        
        # Dibujar el fondo redondeado
        with self.container.canvas.before:
            Color(*bg_color)
            self.rect = RoundedRectangle(
                pos=self.container.pos,
                size=self.container.size,
                radius=[dp(20)]
            )
        
        self.container.bind(pos=self._update_rect, size=self._update_rect)
        self.container.add_widget(self.label)
        self.add_widget(self.container)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

class BookDetailScreen(Screen, ResponsiveView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.book_data = None
        Window.bind(size=self._on_window_resize)
        
        
        with self.canvas.before:
            Color(0.95, 0.95, 0.97, 1)
            self.rect = Rectangle(size=Window.size)
        
        self.scroll_layout = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width=0,  # Ocultar la barra de scroll
            bar_color=[0, 0, 0, 0],  # Hacer la barra transparente
            effect_cls='ScrollEffect'  # Eliminar el efecto de rebote
        )
        
        self.main_layout = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            size_hint_y=None,
            padding=[dp(20), dp(30), dp(20), dp(20)]  # Left, Top, Right, Bottom
        )
        self.main_layout.bind(minimum_height=self.main_layout.setter('height'))
        
        # Header with back button
        self.header = BoxLayout(
            size_hint_y=None,
            height=self.get_responsive_value(50, 60, 70),
            padding=[0, dp(10), 0, dp(10)]
        )
        
        back_container = AnchorLayout(
            size_hint=(None, None),
            size=(dp(45), dp(45)),
            padding=0
        )
        
        with back_container.canvas.before:
            Color(0.2, 0.6, 1, 1)  # Color azul
            RoundedRectangle(
                pos=back_container.pos,
                size=back_container.size,
                radius=[dp(8)]
            )
        
        self.back_button = MDIconButton(
            icon="arrow-left",
            size_hint=(None, None),
            size=(dp(45), dp(45)),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.back_button.bind(on_press=self.go_back)
        back_container.bind(pos=self._update_back_button_bg, size=self._update_back_button_bg)
        back_container.add_widget(self.back_button)
        self.header.add_widget(back_container)
        
        # Image container with responsive height
        self.image_container = AnchorLayout(
            size_hint_y=None,
            height=self.get_responsive_value(200, 250, 300)
        )
        
        # Labels
        self.title_label = Label(
            text='',
            font_size=self.get_responsive_value(20, 24, 28),
            bold=True,
            size_hint_y=None,
            height=dp(40),
            color=(0.1, 0.1, 0.1, 1)
        )
        
        self.author_label = Label(
            text='',
            font_size=self.get_responsive_value(16, 18, 20),
            size_hint_y=None,
            height=dp(30),
            color=(0.3, 0.3, 0.3, 1)
        )
        
        self.availability_container = AnchorLayout(
            size_hint_y=None,
            height=dp(50)
        )
        
        # Description container
        self.description_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            padding=[0, dp(10)],
            spacing=dp(10)
        )
        
        self.description_label = Label(
            text='',
            font_size=dp(14),
            color=(0.2, 0.2, 0.2, 1),
            size_hint_y=None,
            halign='left',
            valign='top'
        )
        self.description_label.bind(size=self._update_text_size)
        Window.bind(size=self._update_text_size)
        
        # Rating container
        self.rating_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            spacing=dp(10)
        )
        
        self.rating_label = Label(
            text='Califica este libro:',
            font_size=dp(16),
            size_hint_y=None,
            height=dp(25),
            color=(0.2, 0.2, 0.2, 1)
        )
        
        # Exchange button container
        self.exchange_button_container = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(70),
            padding=[0, dp(15), 0, dp(15)]
        )
        
        # Add all widgets
        self.main_layout.add_widget(self.header)
        self.main_layout.add_widget(self.image_container)
        self.main_layout.add_widget(self.title_label)
        self.main_layout.add_widget(self.author_label)
        self.main_layout.add_widget(self.availability_container)
        self.description_container.add_widget(self.description_label)
        self.main_layout.add_widget(self.description_container)
        self.main_layout.add_widget(self.rating_container)
        self.main_layout.add_widget(self.exchange_button_container)
        
        self.scroll_layout.add_widget(self.main_layout)
        self.add_widget(self.scroll_layout)
    
    def _update_rect(self, instance, value):
        self.rect.size = instance.size
    
    def _update_text_size(self, *args):
        # Actualizar el text_size basado en el ancho de la ventana
        padding = dp(40)  # 20dp de padding a cada lado
        self.description_label.text_size = (Window.width - padding, None)
        
        # Actualizar la altura del contenedor
        if self.description_label.texture_size[1]:
            self.description_label.height = self.description_label.texture_size[1]
            self.description_container.height = self.description_label.height + dp(20)
    
    def _on_window_resize(self, instance, value):
        # Actualizar valores responsivos
        self.header.height = self.get_responsive_value(50, 60, 70)
        self.image_container.height = self.get_responsive_value(200, 250, 300)
        self.title_label.font_size = self.get_responsive_value(20, 24, 28)
        self.author_label.font_size = self.get_responsive_value(16, 18, 20)
        self._update_text_size()
    
    def _update_back_button_bg(self, instance, value):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(0.2, 0.6, 1, 1)
            RoundedRectangle(
                pos=instance.pos,
                size=instance.size,
                radius=[dp(8)]
            )
    
    def load_book_data(self, book_id):
        try:
            response = requests.get(f'http://localhost:5001/books?id={book_id}')
            if response.status_code == 200:
                books = response.json()
                if books:
                    book = books[0]  # Tomamos el primer libro ya que buscamos por ID
                    self.update_book_data({
                        'id': book['id'],
                        'title': book['name'],
                        'author': book['author'],
                        'description': book['description'] or 'Sin descripción disponible',
                        'rating': round(float(book['average_rating'])) if book['average_rating'] else 0,
                        'image_url': book['photo'] or 'ruta/a/imagen/por/defecto.jpg',
                        'availability_status': book['availability_status'],
                        'owner_id': book['owner_id']  # Agregamos el owner_id
                    })
                else:
                    print("Libro no encontrado")
            else:
                print(f"Error al obtener el libro: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error de conexión: {e}")

    def go_back(self, instance):
        self.manager.current = 'home'
    
    def update_book_data(self, book_data):
        self.book_data = book_data
        
        # Update image
        self.image_container.clear_widgets()
        cover_image = AsyncImage(
            source=book_data.get('image_url', ''),
            size_hint=(None, None),
            size=(dp(180), dp(240)),
            allow_stretch=True,
            keep_ratio=True
        )
        self.image_container.add_widget(cover_image)
        
        self.title_label.text = book_data.get('title', '')
        self.author_label.text = f"{book_data.get('author', '')}"
        
        # Usar el estado real del libro
        is_available = book_data.get('availability_status', False)
        
        self.availability_container.clear_widgets()
        self.availability_container.add_widget(AvailabilityBadge(is_available))
        
        self.description_label.text = book_data.get('description', '')
        self._update_text_size()
        
        self.rating_container.clear_widgets()
        self.rating_container.add_widget(self.rating_label)
        self.rating_container.add_widget(
            InteractiveStarRating(
                book_id=book_data['id']
            )
        )
        
        self.exchange_button_container.clear_widgets()
        if is_available:
            exchange_button = Button(
                text='Solicitar Intercambio',
                size_hint=(None, None),
                size=(dp(200), dp(45)),
                pos_hint={'center_x': 0.5},
                background_color=(0.2, 0.6, 1, 1),
                color=(1, 1, 1, 1),
                bold=True
            )
            exchange_button.bind(on_press=self.request_exchange)
            self.exchange_button_container.add_widget(exchange_button)
    
    def request_exchange(self, instance):
        if self.book_data:
            # Navegar a la pantalla de intercambio
            exchange_screen = self.manager.get_screen('exchange_location')
            exchange_screen.show_exchange_location(self.book_data)
            self.manager.current = 'exchange_location'
