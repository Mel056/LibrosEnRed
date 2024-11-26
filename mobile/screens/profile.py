from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout


class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        self.name = "profile"
        
        self.setup_ui()

    def setup_ui(self):
        # Main layout for the profile screen
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))

        # Profile Picture
        profile_picture = AsyncImage(
            source="https://images.unsplash.com/photo-1511367461989-f85a21fda167",  # Add a URL or local path to an image
            size_hint=(None, None),
            size=(dp(150), dp(150)),
            pos_hint={"center_x": 0.5}
        )

        # Profile Name
        profile_name = Label(
            text="Pedro",
            font_size=dp(24),
            bold=True,
            size_hint_y=None,
            height=dp(40),
            color=(0, 0, 0, 1),
            pos_hint={"center_x": 0.5}
        )

        # Profile Description
        profile_description = Label(
            text="Descripcion",
            font_size=dp(14),
            size_hint_y=None,
            height=dp(100),
            color=(0.3, 0.3, 0.3, 1),
            text_size=(dp(300), None),
            halign='center',
            pos_hint={"center_x": 0.5}
        )

        # Edit Profile Button
        edit_button = Button(
            text="Editar Perfil",
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(dp(200), dp(40)),
            pos_hint={"center_x": 0.5},
            on_press=self.edit_profile
        )

        # Back Button
        back_button = Button(
            text="Back",
            background_color=(0.6, 0.2, 0.2, 1),
            color=(1, 1, 1, 1),
            size_hint=(None, None),
            size=(dp(200), dp(40)),
            pos_hint={"center_x": 0.5},
        )
        
        back_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'home'))
        
        

        # Add all widgets to the main layout
        main_layout.add_widget(profile_picture)
        main_layout.add_widget(profile_name)
        main_layout.add_widget(profile_description)
        main_layout.add_widget(edit_button)
        main_layout.add_widget(back_button)

        # ScrollView to handle overflow if the description is long
        scroll_layout = ScrollView(size_hint=(1, None), height=dp(400))
        scroll_layout.add_widget(main_layout)

        self.add_widget(scroll_layout)

    def edit_profile(self, instance):
        # Logic to edit the profile (can open a new screen or modal)
        print("Edit Profile clicked")

    def go_back(self, instance):
        # Go back to the previous screen
        self.manager.current = "home"  # Assuming "home" is the name of the previous screen
