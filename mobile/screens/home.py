from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivymd.uix.label import MDLabel
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.uix.behaviors import ButtonBehavior
from kivymd.app import MDApp
from kivy.clock import Clock
import requests

class RoundedButton(Button):
    def __init__(self, background_color=(0.2, 0.6, 0.8, 1), radius=15, **kwargs):
        super().__init__(**kwargs)

        self.background_normal = '' 
        self.background_color = (0, 0, 0, 0) 

        self.size_hint = (1, None)
        self.size = kwargs.get('size', (dp(150), dp(50)))

        with self.canvas.before:
            Color(*background_color)
            self.rect = RoundedRectangle(size=self.size, pos=self.pos, radius=[dp(radius)])

        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.border.pos = self.pos
        self.border.size = self.size


from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.uix.label import Label
from kivymd.uix.label import MDIcon

class StarRating(BoxLayout):
    def __init__(self, rating, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(30)
        self.spacing = dp(5)
        rating = min(rating, 5)

        for i in range(5):
            if i < rating:
                star = MDIcon(
                    icon="star",  # Estrella llena
                    theme_text_color="Custom",
                    text_color=(1, 0.8, 0, 1),  # Color amarillo dorado
                    size_hint=(None, None),
                    size=(dp(24), dp(24))
                )
            else:
                star = MDIcon(
                    icon="star-outline",  # Estrella vacía
                    theme_text_color="Custom",
                    text_color=(0.7, 0.7, 0.7, 1),  # Color gris
                    size_hint=(None, None),
                    size=(dp(24), dp(24))
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
            Color(.1, .02, .3, 1)
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
            height = dp(120),
            width = dp(160)
        )
        
        image_container.add_widget(self.image)
        
         # Book info
        title_label = Label(
            text=title,
            text_size=(None, None),
            font_size=dp(18),
            bold=True,
            size_hint_x=1,
            size_hint_y=None,
            height=dp(30),
            color=(1, 1, 1, 1)
        )
        
        self.bind(
            width=lambda instance, value: setattr(
                title_label, "text_size", (value - self.padding[0] * 2, None)
            )
        )

        title_label.bind(
            texture_size=lambda instance, value: setattr(
                instance, "height", value[1]
            )
        )
        
        author_label = Label(
            text=f"por {author}",
            font_size=dp(14),
            size_hint_y=None,   
            size_hint_x=1,
            height=dp(25),
            color=(1, 1, 1, 1)
        )
        
        self.bind(
            width=lambda instance, value: setattr(
                author_label, "text_size", (value - self.padding[0] * 2, None)
            )
        )

        author_label.bind(
            texture_size=lambda instance, value: setattr(
                instance, "height", value[1]
            )
        )
        
        description_label = Label(
            text=description,
            font_size=dp(12),
            text_size=(dp(280), None),
            size_hint_y=None,
            height=dp(60),
            halign='center',
            color=(1, 1, 1, 1)
        )
        
        self.bind(
            width=lambda instance, value: setattr(
                description_label, "text_size", (value - self.padding[0] * 2, None)
            )
        )

        description_label.bind(
            texture_size=lambda instance, value: setattr(
                instance, "height", value[1]
            )
        )
        
        # Star rating
        rating_widget = StarRating(rating)
        
        # Add all widgets
        self.add_widget(image_container)
        self.add_widget(title_label)
        self.add_widget(author_label)
        self.add_widget(rating_widget)
        self.add_widget(description_label)
            
        for child in self.children:
            child.bind(height=self.update_height)

        Clock.schedule_once(self.update_height, 0.1)  


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
    
    def update_height(self, *args):
        if isinstance(self.padding, (list, tuple)):
            vertical_padding = self.padding[1] + self.padding[3]
        else:
            vertical_padding = self.padding * 2

        total_height = sum(child.height for child in reversed(self.children)) + \
                    self.spacing * (len(self.children) - 1) + \
                    vertical_padding
        self.height = total_height



class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        with self.canvas.before:
            Color(0.2, 0.03, 0.4, 1)  # Color de fondo suave
            self.rect = Rectangle(size=Window.size)
        Window.bind(size=self._update_rect)
        
        # Main layout with centering
        main_anchor = AnchorLayout(anchor_x='center', anchor_y='center')
        main_layout = BoxLayout(
            orientation='vertical',
            size_hint=(0.95, 0.95),
            spacing=dp(10)
        )
        
        # Title bar
        title_bar = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10),
            padding=dp(5)
        )
        
        # Top bar
        top_bar = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10),
            padding=dp(5),
        )
        
        # App title
        title_label = Label(
            text='Libros en Red',
            font_size=dp(24),
            bold=True,
            size_hint_y=None,
            height=dp(50),
            color=(1, 1, 1, 1),
        )
        
        
        profile_btn = RoundedButton(
            text="Perfil",
            background_color=(.1, .02, .3, 1), 
            radius=20, 
            size=(dp(100), dp(50))
        )
        
        profile_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'profile'))
        
        title_bar.add_widget(title_label)
        top_bar.add_widget(profile_btn)
        
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
        main_layout.add_widget(title_bar)
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
