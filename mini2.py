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


class Minip2(Screen):
    def __init__(self, **kwargs):
        super(Minip2, self).__init__(**kwargs)
        self.selected_images_to_hide = []

        # Create a vertical BoxLayout as the main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(1, 1))

        # Get the window size
        window_width, window_height = Window.size
        with main_layout.canvas:
            Rectangle(pos=main_layout.pos, size=(window_width, window_height), source='des3.jpg')

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

        # Create a button to open the file dialog for "Get Image1"
        get_image_button1 = Button(
            text="Get Image1",
            size_hint=(None, None),
            height=50,
            width=200,
            pos_hint={'center_x': 0.5}
        )

        # Create an Image widget to display the selected image (single image)
        selected_image = Image(
            size_hint=(None, None),
            size=(100, 100),  # Square size
            pos_hint={'center_x': 0.5}
        )

        # Create a button to open the file dialog for "Get Image2"
        get_image_button2 = Button(
            text="Get Image2",
            size_hint=(None, None),
            height=50,
            width=200,
            pos_hint={'center_x': 0.5}
        )

        # Create a BoxLayout to hold the selected images for "Get Image2"
        selected_images_layout2 = BoxLayout(
            orientation='horizontal',
            spacing=10,
            size_hint_y=None,
        )

        # Create an "Encode" button with red color
        encode_button = Button(
            text="Encode",
            size_hint=(None, None),
            height=50,
            width=200,
            pos_hint={'center_x': 0.5},
            background_color=(1, 0, 0, 1)  # Red color (RGB)
        )

        # Create an Image widget to display the encoded image
        encoded_image_widget = Image(
            size_hint=(None, None),
            size=(100, 100),  # Square size
            pos_hint={'center_x': 0.5}
        )

        # Create a "Download" button with sky-blue color
        download_button = Button(
            text="Download",
            size_hint=(None, None),
            height=50,
            width=200,
            pos_hint={'center_x': 0.5},
            background_color=(0, 0.7, 1, 1)  # Sky-blue color (RGB)
        )

        # Create a "Reveal" button with orange color
        reveal_button = Button(
            text="Reveal",
            size_hint=(None, None),
            height=50,
            width=200,
            pos_hint={'center_x': 0.5},
            background_color=(1, 0.5, 0, 1)  # Orange color (RGB)
        )
        reveal_button.bind(on_release=self.reveal_images)  # Bind to the reveal_images function

        back_button = Button(
            text="Back",
            size_hint=(None, None),
            height=30,
            width=100,
            pos_hint={'center_x': 0.5},
            background_color=(0, 0.5, 1, 1)  # Sky-blue color (RGB)
        )
        back_button.bind(on_release=self.go_back)  # Bind the button to the go_back method

        # Add widgets to the main layout in the desired order
        main_layout.add_widget(mail_label)
        main_layout.add_widget(welcome_label)
        main_layout.add_widget(get_image_button1)
        main_layout.add_widget(selected_image)
        main_layout.add_widget(get_image_button2)
        main_layout.add_widget(selected_images_layout2)
        main_layout.add_widget(encode_button)
        main_layout.add_widget(encoded_image_widget)  # Initially hidden
        main_layout.add_widget(download_button)
        main_layout.add_widget(reveal_button)  # Add the "Reveal" button
        main_layout.add_widget(back_button)  # Download button

        # Set the main layout as the root widget of this screen
        self.add_widget(main_layout)

        # Store the widgets for later use
        self.selected_image = selected_image
        self.selected_images_layout2 = selected_images_layout2
        self.encode_button = encode_button
        self.encoded_image_widget = encoded_image_widget

        # Bind the buttons to their respective functions
        get_image_button1.bind(on_release=lambda x: self.open_file_dialog(selected_image))
        get_image_button2.bind(on_release=lambda x: self.open_files_dialog(selected_images_layout2))
        encode_button.bind(on_release=lambda x: self.encode_and_hide_images())
        download_button.bind(on_release=lambda x: self.download_encoded_image())
    def go_back(self, instance):
        self.manager.current = 'minipp1'  # Navigate back to the "minipp1" screen

    def open_file_dialog(self, selected_image):
        file_chooser = FileChooserIconView()
        file_chooser.filters = ['*.png', '*.jpg', '*.jpeg']

        def on_submit(instance, value, touch):
            if value:
                selected_file = value[0]
                selected_image.source = selected_file

        file_chooser.bind(on_submit=on_submit)

        popup = Popup(title="Select a Single Image", content=file_chooser, size_hint=(0.9, 0.9))
        popup.open()

    def open_files_dialog(self, selected_images_layout):
        file_chooser = FileChooserIconView()
        file_chooser.filters = [
            '*.png', '*.jpg', '*.jpeg',  # Image formats
            '*.txt',  # Text files
            '*.docx',  # Word documents
        ]

        def on_submit(instance, value, touch):
            for file_path in value:
                if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                    selected_image = Image(
                        source=file_path,
                        size_hint=(None, None),
                        size=(100, 100),  # Small square size
                    )
                elif file_path.lower().endswith('.txt'):
                    selected_image = Label(
                        text=file_path,
                        size_hint=(None, None),
                        height=50,
                        width=100,
                        text_size=(None, None),
                    )
                selected_images_layout.add_widget(selected_image)
                self.selected_images_to_hide.append(selected_image)

        file_chooser.bind(on_submit=on_submit)

        popup = Popup(title="Select Images and Text Documents", content=file_chooser, size_hint=(0.9, 0.9))
        popup.open()

    def encode_and_hide_images(self):
        # Check if the single image is selected
        if not self.selected_image.source:
            # Show a popup message to insert a single image
            popup = Popup(
                title="Error",
                content=Label(text="Please select a single image."),
                size_hint=(0.5, 0.5),
            )
            popup.open()
            return

        # Check if at least one image for hiding is attached
        if not self.selected_images_layout2.children:
            # Show a popup message if no images are attached for hiding
            popup = Popup(
                title="Error",
                content=Label(text="Please attach at least one image for hiding."),
                size_hint=(0.5, 0.5),
            )
            popup.open()
            return

        # Load the selected single image
        main_image = PILImage.open(self.selected_image.source)

        # Create a list to store the images to be hidden
        images_to_hide = []

        # Calculate the size to which you want to resize the images
        resized_image_size = (100, 100)  # Adjust the size as needed

        # Collect and resize the selected images for hidinga
        for widget in self.selected_images_layout2.children:
            if isinstance(widget, Image):
                image_to_hide = PILImage.open(widget.source)
                # Resize the image_to_hide to the specified size
                image_to_hide = image_to_hide.resize(resized_image_size)
                images_to_hide.append(image_to_hide)

        # Ensure that there are exactly 4 images to hide
        if len(images_to_hide) != 4:
            # Show a popup message if not exactly 4 images are provided
            popup = Popup(
                title="Error",
                content=Label(text="Please provide exactly 4 images for hiding."),
                size_hint=(0.5, 0.5),
            )
            popup.open()
            return

        # Define positions for each hidden image (top-left, top-right, bottom-left, bottom-right)
        positions = [(0, 0), (main_image.width - resized_image_size[0], 0),
                     (0, main_image.height - resized_image_size[1]),
                     (main_image.width - resized_image_size[0], main_image.height - resized_image_size[1])]

        # Iterate through the images to hide and perform LSB steganography
        for i, image_to_hide in enumerate(images_to_hide):
            x, y = positions[i]

            for xi in range(resized_image_size[0]):
                for yi in range(resized_image_size[1]):
                    pixel = list(main_image.getpixel((xi + x, yi + y)))
                    pixel[0] = (pixel[0] & 0xFE) | ((image_to_hide.getpixel((xi, yi))[0] & 1))
                    pixel[1] = (pixel[1] & 0xFE) | ((image_to_hide.getpixel((xi, yi))[1] & 1))
                    pixel[2] = (pixel[2] & 0xFE) | ((image_to_hide.getpixel((xi, yi))[2] & 1))
                    main_image.putpixel((xi + x, yi + y), tuple(pixel))

        # Save the composite image
        main_image.save("encoded_image.png")

        # Display a success message and the encoded image
        success_popup = Popup(
            title="Success",
            content=Label(text="Images successfully encoded and hidden."),
            size_hint=(0.5, 0.5),
        )
        success_popup.open()

        # Update the displayed encoded image
        self.encoded_image_widget.source = "encoded_image.png"
    def download_encoded_image(self):
        if os.path.exists("encoded_image.png"):
            os.system("start encoded_image.png")
        else:
            popup = Popup(
                title="Error",
                content=Label(text="The encoded image file does not exist."),
                size_hint=(0.5, 0.5),
            )
            popup.open()

    def reveal_images(self, instance):
        # Create a horizontal layout to display revealed images
        revealed_images_layout = GridLayout(
            cols=4,  # Display images in 4 columns
            spacing=10,
            size_hint_y=None,
        )

        # Iterate through the selected images and add them to the layout
        for selected_image in self.selected_images_to_hide:
            if isinstance(selected_image, Image):
                # Create a new Image widget for each revealed image
                revealed_image_widget = Image(
                    source=selected_image.source,
                    size_hint=(None, None),
                    size=(100,100)  # Adjust the size as needed
                )
                revealed_images_layout.add_widget(revealed_image_widget)

        # Create a ScrollView to scroll through revealed images horizontally
        revealed_scrollview = ScrollView(size_hint=(1, 0.7), do_scroll_y=False)
        revealed_scrollview.add_widget(revealed_images_layout)

        # Create a Popup to display the revealed images
        revealed_popup = Popup(
            title="Revealed Images",
            content=revealed_scrollview,
            size_hint=(0.8, 0.8),
        )

        # Display revealed images at the top of the popup
        revealed_popup.content.pos_hint = {'top': 1}

        revealed_popup.open()

        # Display a success message
        success_popup = Popup(
            title="Images Revealed",
            content=Label(text="Images successfully revealed."),
            size_hint=(0.5, 0.5),
        )
        success_popup.open()
    def go_back(self, instance):
        self.manager.current = 'mini2_screen'

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Minip2(name='mini2_screen'))

        return sm

if __name__ == '__main__':
    MyApp().run()
