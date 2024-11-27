from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class MapScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()
    
    def setup_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20)
        
        # Placeholder message
        placeholder = Label(
            text='Mapa en desarrollo...\nEsta función estará disponible próximamente',
            halign='center'
        )
        
        # Back button
        back_btn = Button(
            text='Volver',
            size_hint_y=None,
            height=50
        )
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        
        layout.add_widget(placeholder)
        layout.add_widget(back_btn)
        
        self.add_widget(layout)
