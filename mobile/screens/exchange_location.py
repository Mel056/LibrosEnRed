# screens/exchange_location.py
from kivy.metrics import dp
from kivy_garden.mapview import MapView, MapSource
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import MDSnackbar
import requests
from .location import CustomMapMarker

class ExchangeLocationScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.book_data = None
        self.owner_data = None
        self.setup_ui()
    
    def setup_ui(self):
        main_layout = MDBoxLayout(
            orientation='vertical',
            padding=dp(10),
            spacing=dp(10)
        )
        
        # Header
        header = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=[dp(10), dp(5)]
        )
        
        # Back button
        back_btn = MDIconButton(
            icon="arrow-left",
            on_release=self.go_back
        )
        
        title = MDLabel(
            text='Punto de Encuentro',
            font_style='H6',
            halign='center',
            theme_text_color='Primary',
            size_hint_y=None,
            height=dp(50),
        )
        
        header.add_widget(back_btn)
        header.add_widget(title)
        
        # Mapa
        map_layout = MDBoxLayout(
            size_hint_y=0.7
        )
        
        self.map_view = MapView(
            zoom=15,
            lat=-34.6037,
            lon=-58.3816,
            double_tap_zoom=True,
            map_source=MapSource(
                url="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
                attribution="Google Maps"
            )
        )
        
        map_layout.add_widget(self.map_view)
        
        # Owner info
        self.owner_info = MDLabel(
            text='',
            halign='center',
            size_hint_y=None,
            height=dp(50)
        )
        
        # Confirm button
        self.confirm_btn = MDRaisedButton(
            text='Confirmar Intercambio',
            size_hint=(None, None),
            width=dp(200),
            pos_hint={'center_x': 0.5},
            on_release=self.confirm_exchange
        )
        
        # Add widgets
        main_layout.add_widget(header)
        main_layout.add_widget(map_layout)
        main_layout.add_widget(self.owner_info)
        main_layout.add_widget(self.confirm_btn)
        
        self.add_widget(main_layout)
    
    def show_exchange_location(self, book_data):
        self.book_data = book_data
        app = MDApp.get_running_app()
        
        if not app.user_data:
            self.show_error("Usuario no logueado")
            return
        
        # Primero crear la solicitud de intercambio
        try:
            response = requests.post('http://localhost:5001/exchange/request', json={
                'book_id': book_data['id'],
                'requesting_user_id': app.user_data['user_id']
            })
            
            if response.status_code == 201:
                exchange_data = response.json()
                owner = exchange_data['exchange_details']['owner']
                
                # Guardar datos del owner
                self.owner_data = owner
                
                # Actualizar el mapa
                self.map_view.center_on(
                    float(owner['location']['latitude']),
                    float(owner['location']['longitude'])
                )
                
                # Agregar marcador
                self.map_view.add_marker(CustomMapMarker(
                    lat=float(owner['location']['latitude']),
                    lon=float(owner['location']['longitude'])
                ))
                
                # Actualizar información del dueño
                self.owner_info.text = f"Punto de encuentro con: {owner['username']}"
                
            else:
                self.show_error("Error al solicitar el intercambio")
                self.go_back(None)
                
        except requests.RequestException as e:
            self.show_error(f"Error de conexión: {e}")
            self.go_back(None)
    
    def confirm_exchange(self, instance):
        # Aquí iría la lógica para confirmar el intercambio
        self.show_info("Intercambio confirmado")
        self.manager.current = 'home'
    
    def go_back(self, instance):
        self.manager.current = 'book_detail'
    
    def show_error(self, message):
        snackbar = MDSnackbar()
        snackbar.text = message
        snackbar.bg_color = (0.8, 0, 0, 1)
        snackbar.duration = 3
        snackbar.open()
    
    def show_info(self, message):
        snackbar = MDSnackbar()
        snackbar.text = message
        snackbar.duration = 2
        snackbar.open()
