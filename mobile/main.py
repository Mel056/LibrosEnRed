# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from screens.login import LoginScreen
from screens.main import MainScreen
from screens.map import MapScreen

# Set window size for desktop testing
Window.size = (360, 640)

class BookExchangeApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(MapScreen(name='map'))
        return sm

if __name__ == '__main__':
    BookExchangeApp().run()
