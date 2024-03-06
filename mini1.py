from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from mini22 import Minip2
from mini33 import DecodingScreen
class Minip1(Screen):
    def __init__(self, **kwargs):
        super(Minip1, self).__init__(**kwargs)

        # Create a vertical BoxLayout as the main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=0, size_hint=(1, 1))

        # Get the window size
        window_width, window_height = Window.size

        # Create a sky-blue background using a Rectangle instruction that fills the entire window
        with main_layout.canvas:
            Rectangle(pos=main_layout.pos, size=(window_width, window_height), source='des3.jpg')

        # Create a label for "HIDDEN CONTENT APP" in red with height set to 0 (removing blank space)
        mail_label = Label(
            text="HIDDEN CONTENT APP",
            color=(0, 0, 1, 1),  # Red color (RGB)
            font_size=24,
            size_hint_y=None,
            height=30,  # Set the height to fit the content
            pos_hint={'center_x': 0.5}  # Center the label horizontally
        )
        main_layout.add_widget(mail_label)

        # Create a label for "WELCOME" in dark green with height set to 0 (removing blank space)
        welcome_label = Label(
            text="WELCOME",
            color=(0, 0.5, 0, 1),  # Dark green color (RGB)
            font_size=24,
            size_hint_y=None,
            height=100,  # Set the height to fit the content
            pos_hint={'center_x': 0.5}  # Center the label horizontally
        )
        main_layout.add_widget(welcome_label)

        encode_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        encode_button = Button(text='ENCODE', background_color=(0, 1, 0, 1), height=100, width=300,
                              size_hint=(None, None))
        encode_button.bind(on_release=self.goto)
        encode_layout.add_widget(encode_button)


        decode_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        decode_button = Button(text='DECODE', background_color=(1, 0, 0, 1), height=100, width=300,
                              size_hint=(None, None))
        decode_button.bind(on_release=self.goto2)

        decode_layout.add_widget(decode_button)
        main_layout.add_widget(encode_layout)
        main_layout.add_widget(decode_layout)
        # Set the main layout as the root widget of this screen
        self.add_widget(main_layout)

    def goto(self, instance):
        self.manager.current = 'mini2'

    def goto2(self, instance):
        self.manager.current = 'mini3'


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Minip1(name='minipp1'))
        sm.add_widget(DecodingScreen(name='mini3'))
        sm.add_widget(Minip2(name='mini2'))


        return sm

if __name__ == '__main__':
    MyApp().run()
