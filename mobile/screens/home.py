# screens/main.py
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.uix.behaviors import ButtonBehavior
from kivymd.app import MDApp
import qrcode
import requests


class StarRating(BoxLayout):
    def __init__(self, rating, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(30)
        self.spacing = dp(5)
        
        for i in range(5):
            star = Label(
                text='★' if i < rating else '☆',
                color=(1, 0.8, 0, 1) if i < rating else (0.7, 0.7, 0.7, 1),
                size_hint=(None, None),
                size=(dp(20), dp(20))
            )
            self.add_widget(star)


class BookCard(ButtonBehavior, BoxLayout):
    def __init__(self, title, author, description, rating, image_url, book_data, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(400)
        self.padding = dp(15)
        self.spacing = dp(10)
        self.pos_hint = {'center_x': 0.5}
        self.book_data = book_data
        
        # Card background
        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)
        
        # Image container
        image_container = AnchorLayout(
            size_hint=(1, None),
            height=dp(180),
            anchor_x='center',
            anchor_y='center'
        )
        
        # Book cover image
        self.image = AsyncImage(
            source=image_url,
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(None, None),
            size=(dp(120), dp(160))
        )
        
        image_container.add_widget(self.image)
        
        # Book info
        title_label = Label(
            text=title,
            font_size=dp(18),
            bold=True,
            size_hint_y=None,
            height=dp(30),
            color=(0.2, 0.2, 0.2, 1)
        )
        
        author_label = Label(
            text=f"por {author}",
            font_size=dp(14),
            size_hint_y=None,
            height=dp(25),
            color=(0.4, 0.4, 0.4, 1)
        )
        
        description_label = Label(
            text=description,
            font_size=dp(12),
            text_size=(dp(280), None),
            size_hint_y=None,
            height=dp(60),
            halign='center',
            color=(0.3, 0.3, 0.3, 1)
        )
        
        # Star rating
        rating_widget = StarRating(rating)
        
        # Exchange button
        self.exchange_btn = Button(
            text='Solicitar Intercambio',
            size_hint=(None, None),
            size=(dp(200), dp(40)),
            pos_hint={'center_x': 0.5},
            background_color=(0.2, 0.6, 1, 1)
        )
        
        self.exchange_btn.bind(on_press=self.generate_qr_code)
        
        # Add all widgets
        self.add_widget(image_container)
        self.add_widget(title_label)
        self.add_widget(author_label)
        self.add_widget(rating_widget)
        self.add_widget(description_label)
        self.add_widget(self.exchange_btn)
        
        # QR code display
        self.qr_image = Image()
        self.add_widget(self.qr_image)

        # Bind the on_press event
        self.bind(on_press=self.on_card_press)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def on_card_press(self, instance):
        app = MDApp.get_running_app()
        screen_manager = app.root
        
        if screen_manager:
            screen_manager.current = 'book_detail'
            detail_screen = screen_manager.get_screen('book_detail')
            detail_screen.load_book_data(self.book_data['id'])
        
    def generate_qr_code(self, instance):
        user_id = "1234"
        book_id = "1234"

        if not user_id or not book_id:
            return

        # Combine user ID and book ID
        qr_data = f"UserID: {user_id}, BookID: {book_id}"

        # Generate QR code
        qr = qrcode.make(qr_data)

        # Convert QR code to a Kivy texture
        qr_image = qr.convert('RGB')
        qr_image_data = qr_image.tobytes()
        texture = Texture.create(size=qr_image.size, colorfmt='rgb')
        texture.blit_buffer(qr_image_data, bufferfmt='ubyte', colorfmt='rgb')
        texture.flip_vertical()

        # Display QR code in the Image widget
        self.qr_image.texture = texture

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        with self.canvas.before:
            Color(0.9, 0.9, 0.95, 1)
            self.rect = Rectangle(size=Window.size)
        Window.bind(size=self._update_rect)
        
        # Main layout with centering
        main_anchor = AnchorLayout(anchor_x='center', anchor_y='center')
        main_layout = BoxLayout(
            orientation='vertical',
            size_hint=(0.95, 0.95),
            spacing=dp(10)
        )
        
        # Top bar
        top_bar = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10),
            padding=dp(5)
        )
        
        # App title
        title_label = Label(
            text='Libros en Red',
            font_size=dp(24),
            bold=True,
            size_hint_y=None,
            height=dp(50),
            color=(0.2, 0.2, 0.2, 1)
        )
        
        # Navigation buttons
        profile_btn = Button(
            text='👤 Perfil',
            background_color=(0.2, 0.6, 1, 1),
            size_hint_x=None,
            width=dp(100)
        )

        qrscanner_btn = Button(
            text='📷 QR',
            background_color=(0.2, 0.6, 1, 1),
            size_hint_x=None,
            width=dp(100)
        )
        
        qrscanner_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'qrscanner'))
        
        top_bar.add_widget(profile_btn)
        top_bar.add_widget(title_label)
        top_bar.add_widget(qrscanner_btn)
        
        # Books list
        self.scroll_layout = ScrollView()
        self.books_layout = GridLayout(
            cols=1,
            spacing=dp(20),
            size_hint_y=None,
            padding=dp(10)
        )
        self.books_layout.bind(minimum_height=self.books_layout.setter('height'))
        
        self.scroll_layout.add_widget(self.books_layout)
        
        # Add all elements to main layout
        main_layout.add_widget(top_bar)
        main_layout.add_widget(self.scroll_layout)
        
        main_anchor.add_widget(main_layout)
        self.add_widget(main_anchor)
        
        # Cargar libros cuando se inicializa la pantalla
        self.load_books()
    
    def _update_rect(self, instance, value):
        self.rect.size = instance.size

    def load_books(self):
        try:
            response = requests.get('http://localhost:5001/books')
            if response.status_code == 200:
                books = response.json()
                self.update_books_layout(books)
            else:
                print(f"Error al obtener libros: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error de conexión: {e}")
    
    def update_books_layout(self, books):
        self.books_layout.clear_widgets()
        
        for book in books:
            book_data = {
                'id': book['id'],
                'title': book['name'],
                'author': book['author'],
                'description': book['description'] or 'Sin descripción disponible',
                'rating': round(float(book['average_rating'])) if book['average_rating'] else 0,
                'image_url': book['photo'] or 'ruta/a/imagen/por/defecto.jpg',
                'availability_status': book['availability_status']
            }
            
            self.books_layout.add_widget(
                BookCard(
                    title=book_data['title'],
                    author=book_data['author'],
                    description=book_data['description'],
                    rating=book_data['rating'],
                    image_url=book_data['image_url'],
                    book_data=book_data
                )
            )
