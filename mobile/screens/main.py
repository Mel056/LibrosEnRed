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
import qrcode


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
            
       

class BookCard(BoxLayout):
    def __init__(self, title, author, description, rating, image_url, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(400)
        self.padding = dp(15)
        self.spacing = dp(10)
        self.pos_hint = {'center_x': 0.5}
        
        # Card background
        with self.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)
        
        # Contenedor para la imagen usando AnchorLayout
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
        
        # Añadir imagen al contenedor
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
        exchange_btn = Button(
            text='Solicitar Intercambio',
            size_hint=(None, None),
            size=(dp(200), dp(40)),
            pos_hint={'center_x': 0.5},
            background_color=(0.2, 0.6, 1, 1)
        )
        
        exchange_btn.bind(on_press=self.generate_qr_code)
        
        # Add all widgets
        self.add_widget(image_container)
        self.add_widget(title_label)
        self.add_widget(author_label)
        self.add_widget(rating_widget)
        self.add_widget(description_label)
        self.add_widget(exchange_btn)
        
        # QR code display
        self.qr_image = Image()
        self.add_widget(self.qr_image)
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
        
    def generate_qr_code(self, instance):
        user_id = "1234"
        book_id = "1234"

        if not user_id or not book_id:
            ""

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
        # self.generate_button.text = "Generate QR Code"

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Set background color
        with self.canvas.before:
            Color(0.9, 0.9, 0.95, 1)  # Color de fondo suave
            self.rect = Rectangle(size=Window.size)
        Window.bind(size=self._update_rect)
        
        self.setup_ui()
    
    def _update_rect(self, instance, value):
        self.rect.size = instance.size
    
    def setup_ui(self):
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
        map_btn = Button(
            text='🗺️ Mapa',
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
        
        map_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'map'))
        qrscanner_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'qrscanner'))
        
        top_bar.add_widget(profile_btn)
        top_bar.add_widget(title_label)
        top_bar.add_widget(map_btn)
        top_bar.add_widget(qrscanner_btn)
        
        # Books list
        scroll_layout = ScrollView()
        books_layout = GridLayout(
            cols=1,
            spacing=dp(20),
            size_hint_y=None,
            padding=dp(10)
        )
        books_layout.bind(minimum_height=books_layout.setter('height'))
        
        # Sample books with actual books and descriptions
        sample_books = [
            {
                'title': 'Cien años de soledad',
                'author': 'Gabriel García Márquez',
                'description': 'La obra cumbre del realismo mágico que narra la historia de la familia Buendía a lo largo de siete generaciones en el pueblo mítico de Macondo.',
                'rating': 5,
                'image_url': 'https://images.cdn3.buscalibre.com/fit-in/360x360/61/8d/618d227e8967274cd9589a549adff52d.jpg'
            },
            {
                'title': '1984',
                'author': 'George Orwell',
                'description': 'Una inquietante visión distópica de un futuro dominado por el totalitarismo y la vigilancia masiva.',
                'rating': 4,
                'image_url': 'https://images.cdn1.buscalibre.com/fit-in/360x360/6d/d7/6dd771b778bb1e198e9cd6762b721a3d.jpg'
            },
            {
                'title': 'El Principito',
                'author': 'Antoine de Saint-Exupéry',
                'description': 'Un clásico atemporal que explora temas de amor, amistad y el significado de la vida a través de los ojos de un pequeño príncipe.',
                'rating': 5,
                'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1c/El_principito.jpg/800px-El_principito.jpg'
            }
        ]
        
        for book in sample_books:
            books_layout.add_widget(
                BookCard(
                    title=book['title'],
                    author=book['author'],
                    description=book['description'],
                    rating=book['rating'],
                    image_url=book['image_url']
                )
            )
        
        scroll_layout.add_widget(books_layout)
        
        # Add all elements to main layout
        main_layout.add_widget(top_bar)
        main_layout.add_widget(scroll_layout)
        
        main_anchor.add_widget(main_layout)
        self.add_widget(main_anchor)
