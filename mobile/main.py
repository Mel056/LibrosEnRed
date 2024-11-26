# main.py
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from screens.login import LoginScreen
from screens.home import HomeScreen
from screens.map import MapScreen
from screens.qrscanner import QRCodeScanner
from screens.register import RegisterScreen
from screens.location import LocationSelectScreen
from screens.success import SuccessScreen
from screens.book_detail import BookDetailScreen
from screens.profile import ProfileScreen

# from kivy.lang import Builder
# Builder.load_file('bookexchange.kv')

# Set window size for desktop testing
Window.size = (360, 640)

class BookExchangeApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MapScreen(name='map'))
        sm.add_widget(LocationSelectScreen(name='location_select'))
        sm.add_widget(QRCodeScanner(name='qrscanner'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(SuccessScreen(name='success'))
        sm.add_widget(BookDetailScreen(name='book_detail'))
        sm.add_widget(ProfileScreen(name='profile'))
        return sm

if __name__ == '__main__':
    BookExchangeApp().run()
