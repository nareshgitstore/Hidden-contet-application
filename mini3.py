import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from PIL import Image as PILImage
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

class DecodingScreen(Screen):
    def __init__(self, **kwargs):
        super(DecodingScreen, self).__init__(**kwargs)
        self.encoded_image = None
        self.selected_images_to_hide = []

        # Create a vertical BoxLayout as the main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(1, 1))

        # Get the window size
        window_width, window_height = Window.size
        with main_layout.canvas:
            Rectangle(pos=main_layout.pos, size=(window_width, window_height), source='des4.jpg')

        # Create a label for "HIDDEN CONTENT APP" in red and center it
        mail_label = Label(
            text="HIDDEN CONTENT APP",
            color=(0, 0, 1, 1),  # Red color (RGB)
            font_size=24,
            size_hint_y=None,
            height=50,  # Set the height to fit the content
            pos_hint={'center_x': 0.5}
        )

        # Create a label for "WELCOME" in green and center it
        welcome_label = Label(
            text="WELCOME",
            color=(0, 1, 0, 1),  # Green color (RGB)
            font_size=24,
            size_hint_y=None,
            height=50,  # Set the height to fit the content
            pos_hint={'center_x': 0.5}
        )

        # Create a button to open the file dialog for "Get Encoded Image"
        get_encoded_image_button = Button(
            text="Get Encoded Image",
            size_hint=(None, None),
            height=50,
            width=200,
            pos_hint={'center_x': 0.5}
        )

        # Create an Image widget to display the selected encoded image
        encoded_image = Image(
            size_hint=(None, None),
            size=(300, 300),  # Adjust size as needed
            pos_hint={'center_x': 0.5}
        )

        # Create a ScrollView to display the decoded images vertically
        self.decoded_images_layout = GridLayout(
            cols=4,  # Display images in 4 columns
            spacing=10,
            size_hint_y=None,
        )
        scroll_view = ScrollView()
        scroll_view.add_widget(self.decoded_images_layout)

        # Create a "Decode" button with orange color
        decode_button = Button(
            text="Decode",
            size_hint=(None, None),
            height=50,
            width=200,
            pos_hint={'center_x': 0.5},
            background_color=(1, 0.5, 0, 1)  # Orange color (RGB)
        )
        decode_button.bind(on_release=self.decode_images)  # Bind to the decode_images function

        back_button = Button(
            text="Back",
            size_hint=(None, None),
            height=30,
            width=100,
            pos_hint={'center_x': 0.5},
            background_color=(0, 0.5, 1, 1)  # Sky-blue color (RGB)
        )

        # Add widgets to the main layout in the desired order
        main_layout.add_widget(mail_label)
        main_layout.add_widget(welcome_label)
        main_layout.add_widget(get_encoded_image_button)
        main_layout.add_widget(encoded_image)
        main_layout.add_widget(scroll_view)
        main_layout.add_widget(decode_button)  # Add the "Decode" button
       #main_layout.add_widget(back_button)  # Back button

        # Set the main layout as the root widget of this screen
        self.add_widget(main_layout)

        # Store the widgets for later use
        self.get_encoded_image_button = get_encoded_image_button
        self.encoded_image = encoded_image

        # Bind the buttons to their respective functions
        get_encoded_image_button.bind(on_release=lambda x: self.open_encoded_image())

    def open_encoded_image(self):
        file_chooser = FileChooserIconView()
        file_chooser.filters = ['*.png', '*.jpg', '*.jpeg']

        def on_submit(instance, value, touch):
            if value:
                selected_file = value[0]
                self.encoded_image.source = selected_file
                # Add the selected image to the list
                image_widget = Image(source=selected_file)
                self.selected_images_to_hide.append(image_widget)

        file_chooser.bind(on_submit=on_submit)

        popup = Popup(title="Select the Encoded Image", content=file_chooser, size_hint=(0.9, 0.9))
        popup.open()

    def decode_images(self, instance):
        # Clear the existing decoded images
        self.decoded_images_layout.clear_widgets()
        self.selected_images_to_hide.clear()  # Clear the list

        try:
            if (self.encoded_image.source.lower().endswith('.png')) and (
                    os.path.basename(self.encoded_image.source) == 'encoded_image.png'):
                encoded_img = PILImage.open(self.encoded_image.source)

                corner_size_download = (100, 100)
                corner_size_display = (100, 100)
                corner_positions = [(0, 0), (encoded_img.width - corner_size_download[0], 0),
                                    (0, encoded_img.height - corner_size_download[1]),
                                    (encoded_img.width - corner_size_download[0],
                                     encoded_img.height - corner_size_download[1])]

                decoded_images = []

                for i, position in enumerate(corner_positions):
                    left, top = position
                    right = left + corner_size_download[0]
                    bottom = top + corner_size_download[1]

                    corner_image = encoded_img.crop((left, top, right, bottom))
                    extracted_image = PILImage.new("RGB", corner_image.size)

                    for x in range(corner_image.width):
                        for y in range(corner_image.height):
                            pixel_encoded = corner_image.getpixel((x, y))
                            pixel_decoded = [0 if pixel_encoded[0] & 1 == 0 else 255,
                                             0 if pixel_encoded[1] & 1 == 0 else 255,
                                             0 if pixel_encoded[2] & 1 == 0 else 255]

                            extracted_image.putpixel((x, y), (pixel_decoded[0], pixel_decoded[1], pixel_decoded[2]))

                    corner_image_path = f"decoded_image{i}.png"
                    extracted_image = extracted_image.resize(corner_size_display)
                    extracted_image.save(corner_image_path)

                    decoded_images.append(corner_image_path)

                if len(decoded_images) == 4:
                    decoded_images_layout = GridLayout(
                        cols=2,
                        spacing=20,
                        size_hint_y=None,
                    )

                    for image_path in decoded_images:
                        corner_image_widget = Image(
                            source=image_path,
                            size_hint=(None, None),
                            size=corner_size_display,
                        )
                        self.selected_images_to_hide.append(corner_image_widget)
                        decoded_images_layout.add_widget(corner_image_widget)

                    decoded_scrollview = ScrollView(size_hint=(1, 0.7))
                    decoded_scrollview.add_widget(decoded_images_layout)

                    decoded_popup = Popup(
                        title="Decoded Images",
                        content=decoded_scrollview,
                        size_hint=(0.8, 0.8),
                    )
                    decoded_popup.content.pos_hint = {'top': 1}
                    decoded_popup.open()
                else:
                    self.selected_images_to_hide.clear()
                    self.selected_images_to_hide.append(self.encoded_image)

                    popup = Popup(
                        title="Error",
                        content=Label(text="Incorrect encoded image"),
                        size_hint=(0.5, 0.5),
                    )
                    popup.open()

                success_popup = Popup(
                    title="Images Decoded",
                    content=Label(text="Images successfully decoded."),
                    size_hint=(0.5, 0.5),
                )
                success_popup.open()
            else:
                popup = Popup(
                    title="Error",
                    content=Label(text="Incorrect encoded image"),
                    size_hint=(0.5, 0.5),
                )
                popup.open()
        except Exception as e:
            error_popup = Popup(
                title="Error",
                content=Label(text=f"Error decoding images: {str(e)}"),
                size_hint=(0.5, 0.5),
            )
            error_popup.open()


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        decoding_screen = DecodingScreen(name='mini3')
        sm.add_widget(decoding_screen)
        return sm

if __name__ == '__main__':
    MyApp().run()
