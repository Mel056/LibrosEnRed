import requests
from functools import partial
from kivy.metrics import dp
from kivy_garden.mapview import MapView, MapMarker, MapSource
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.snackbar import MDSnackbar
from geopy.geocoders import Nominatim
from kivy.properties import ObjectProperty, BooleanProperty
import threading

class CustomMapMarker(MapMarker):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = 'assets/marker.png'
        self.size = (dp(32), dp(32))
        self.anchor_x = 0.5
        self.anchor_y = 0.0

class LocationSelectScreen(MDScreen):
    map_view = ObjectProperty(None)
    is_dragging = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.registration_data = {}
        self.selected_location = None
        self.current_marker = None
        self.geolocator = Nominatim(user_agent="librosenred")
        self.touch_start = None
        self.start_lat = None
        self.start_lon = None
        self.is_dragging = False
        self.setup_ui()
        Clock.schedule_once(self.get_current_location, 1)
    
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
        
        title = MDLabel(
            text='Selecciona tu Punto de Encuentro',
            font_style='H6',
            halign='center',
            theme_text_color='Primary',
            size_hint_y=None,
            height=dp(50),
        )
        
        search_layout = MDBoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(48),
            spacing=dp(10),
            padding=[dp(5), 0]
        )
        
        self.search_field = MDTextField(
            hint_text="Buscar ubicación",
            mode="rectangle",
            size_hint_x=0.7
        )
        
        search_btn = MDIconButton(
            icon="magnify",
            on_release=self.search_location,
            size_hint_x=None,
            width=dp(48)
        )
        
        locate_btn = MDIconButton(
            icon="crosshairs-gps",
            on_release=lambda x: self.get_current_location(None),
            size_hint_x=None,
            width=dp(48)
        )
        
        search_layout.add_widget(self.search_field)
        search_layout.add_widget(search_btn)
        search_layout.add_widget(locate_btn)
        
        header.add_widget(title)
        header.add_widget(search_layout)
        
        # Mapa con controles de zoom
        map_layout = MDBoxLayout(
            size_hint_y=0.7
        )
        
        map_container = MDBoxLayout(
            orientation='horizontal'
        )
        
        self.map_view = MapView(
            zoom=15,
            lat=-34.6037,
            lon=-58.3816,
            double_tap_zoom=True,  # Habilita zoom con doble tap
            map_source=MapSource(
                url="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
                attribution="Google Maps"
            ),
            size_hint_x=0.95
        )
        
        # Controles de zoom
        zoom_controls = MDBoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            width=dp(40),
            height=dp(100),
            spacing=dp(5),
            pos_hint={'center_y': 0.5}
        )
        
        zoom_in = MDIconButton(
            icon="plus",
            on_release=lambda x: self.zoom_in(),
            size_hint=(None, None),
            size=(dp(40), dp(40))
        )
        
        zoom_out = MDIconButton(
            icon="minus",
            on_release=lambda x: self.zoom_out(),
            size_hint=(None, None),
            size=(dp(40), dp(40))
        )
        
        zoom_controls.add_widget(zoom_in)
        zoom_controls.add_widget(zoom_out)
        
        map_container.add_widget(self.map_view)
        map_container.add_widget(zoom_controls)
        map_layout.add_widget(map_container)
        
        # Footer
        footer = MDBoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(120),
            padding=[dp(10), dp(5)]
        )
        
        self.location_label = MDLabel(
            text='Selecciona una ubicación en el mapa',
            halign='center',
            theme_text_color='Secondary',
            size_hint_y=None,
            height=dp(100),
            font_style='Caption'
        )
        
        confirm_btn = MDRaisedButton(
            text='Confirmar Ubicación',
            size_hint=(None, None),
            width=dp(200),
            height=dp(48),
            pos_hint={'center_x': 0.5},
            on_release=self.confirm_location
        )
        
        footer.add_widget(self.location_label)
        footer.add_widget(confirm_btn)
        
        main_layout.add_widget(header)
        main_layout.add_widget(map_layout)
        main_layout.add_widget(footer)
        
        self.add_widget(main_layout)

    def on_touch_down(self, touch):
        if self.map_view.collide_point(*touch.pos) and hasattr(touch, 'button') and touch.button == 'left':
            # Guardamos la posición inicial del toque y las coordenadas actuales del mapa
            self.touch_start = touch.pos
            self.start_lat = self.map_view.lat
            self.start_lon = self.map_view.lon
            self.is_dragging = False  # Reiniciamos el estado de arrastre
            
            if touch.is_double_tap:
                self.zoom_in()
            return True
        return super().on_touch_down(touch)
    
    def on_touch_move(self, touch):
        if self.touch_start and self.map_view.collide_point(*touch.pos) and hasattr(touch, 'button') and touch.button == 'left':
            # Calculamos la distancia que se ha movido el touch
            self.is_dragging = True
            dx = touch.pos[0] - self.touch_start[0]
            dy = touch.pos[1] - self.touch_start[1]
            
            # Convertimos el desplazamiento en píxeles a coordenadas geográficas
            # Ajustamos la sensibilidad del movimiento
            scale_factor = 0.00001 * (20 - self.map_view.zoom)  # Ajusta la sensibilidad según el nivel de zoom
            
            # Calculamos las nuevas coordenadas
            new_lat = self.start_lat - dy * scale_factor
            new_lon = self.start_lon - dx * scale_factor
            
            # Actualizamos la posición del mapa
            self.map_view.center_on(new_lat, new_lon)
            return True
        return super().on_touch_move(touch)
    
    def on_touch_up(self, touch):
        if self.map_view.collide_point(*touch.pos) and hasattr(touch, 'button') and touch.button == 'left':
            # Si no estábamos arrastrando, tratamos el evento como un click normal
            if not self.is_dragging and not touch.is_double_tap:
                map_coords = self.map_view.to_widget(*touch.pos, relative=True)
                lat, lon = self.map_view.get_latlon_at(*map_coords)
                if lat and lon:
                    self.update_marker(lat, lon)
                    self.get_address_from_coords(lat, lon)
            
            # Reiniciamos las variables de control
            self.touch_start = None
            self.start_lat = None
            self.start_lon = None
            self.is_dragging = False
            return True
        return super().on_touch_up(touch)
        
    def zoom_in(self):
        if self.map_view.zoom < 20:
            self.map_view.zoom += 1

    def zoom_out(self):
        if self.map_view.zoom > 1:
            self.map_view.zoom -= 1
    
    def get_current_location(self, dt):
        # En un dispositivo real, aquí usaríamos la API de geolocalización
        # Por ahora, usamos una ubicación por defecto (Buenos Aires)
        default_lat, default_lon = -34.6037, -58.3816
        self.center_map(default_lat, default_lon)
        self.show_info("Ubicación predeterminada: Buenos Aires")
    
    def center_map(self, lat, lon):
        self.map_view.center_on(lat, lon)
        Clock.schedule_once(lambda dt: setattr(self.map_view, 'zoom', 15), 0.5)

    def update_marker(self, lat, lon):
        if self.current_marker:
            self.map_view.remove_marker(self.current_marker)
        
        self.current_marker = CustomMapMarker(lat=lat, lon=lon)
        self.map_view.add_marker(self.current_marker)
        self.selected_location = (lat, lon)
    
    def search_location(self, instance):
        search_query = self.search_field.text.strip()
        if not search_query:
            self.show_error("Por favor ingrese una ubicación para buscar")
            return
        
        def search():
            try:
                location = self.geolocator.geocode(search_query)
                if location:
                    Clock.schedule_once(
                        partial(self.handle_search_result, location), 0
                    )
                else:
                    Clock.schedule_once(
                        lambda dt: self.show_error("Ubicación no encontrada"), 0
                    )
            except Exception as e:
                Clock.schedule_once(
                    lambda dt: self.show_error(f"Error en la búsqueda: {str(e)}"), 0
                )
        
        # Ejecutar búsqueda en thread separado
        threading.Thread(target=search).start()
        self.show_info("Buscando ubicación...")
    
    def handle_search_result(self, location, dt):
        lat, lon = location.latitude, location.longitude
        self.center_map(lat, lon)
        self.update_marker(lat, lon)
        self.location_label.text = f'Ubicación: {location.address}'
        
    
    def get_address_from_coords(self, lat, lon):
        def reverse_geocode():
            try:
                location = self.geolocator.reverse((lat, lon))
                if location:
                    Clock.schedule_once(
                        lambda dt: setattr(
                            self.location_label,
                            'text',
                            f'Ubicación: {location.address}'
                        ),
                        0
                    )
            except Exception:
                Clock.schedule_once(
                    lambda dt: setattr(
                        self.location_label,
                        'text',
                        f'Ubicación: {lat:.4f}, {lon:.4f}'
                    ),
                    0
                )
        
        threading.Thread(target=reverse_geocode).start()
    
    def set_registration_data(self, username, email, password):
        self.registration_data = {
            'username': username,
            'email': email,
            'password': password
        }
    
    def confirm_location(self, instance):
        if not self.selected_location:
            self.show_error("Por favor seleccione una ubicación en el mapa")
            return
            
        lat, lon = self.selected_location
        if not self.validate_coordinates(lat, lon):
            self.show_error("Coordenadas inválidas")
            return
            
        registration_data = {
            **self.registration_data,
            'latitude': lat,
            'longitude': lon
        }
        
        try:
            print('registration_data:', registration_data)
            response = requests.post(
                'http://localhost:5001/register',
                json=registration_data,
                timeout=5
            )
            
            if response.status_code == 201:
                self.show_success("¡Registro completado exitosamente!")
                Clock.schedule_once(lambda dt: self.go_to_login(), 2)
            else:
                self.show_error(f"Error en el registro: {response.text}")
        except requests.RequestException as e:
            self.show_error(f"Error de conexión: {str(e)}")
    
    def validate_coordinates(self, lat, lon):
        return -90 <= lat <= 90 and -180 <= lon <= 180
    
    def go_to_login(self):
        self.manager.current = 'login'
    
    def show_error(self, message):
        snackbar = MDSnackbar()
        snackbar.bg_color = (0.8, 0, 0, 1)
        snackbar.duration = 3
        snackbar.open()
        Clock.schedule_once(lambda dt: setattr(snackbar, 'text', message))
    
    def show_success(self, message):
        snackbar = MDSnackbar()
        snackbar.bg_color = (0, 0.7, 0, 1)
        snackbar.duration = 3
        snackbar.open()
        Clock.schedule_once(lambda dt: setattr(snackbar, 'text', message))
    
    def show_info(self, message):
        snackbar = MDSnackbar()
        snackbar.duration = 2
        snackbar.open()
        Clock.schedule_once(lambda dt: setattr(snackbar, 'text', message))
