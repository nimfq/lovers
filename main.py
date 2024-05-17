from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
import random
from plyer import notification
from compliments import compliments

# Установка размера окна для эмуляции на ПК (для тестирования)
Window.size = (360, 640)

KV = '''
ScreenManager:
    LoadingScreen:
    MainScreen:

<LoadingScreen>:
    name: 'loading'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        MDLabel:
            text: "LOVE"
            halign: 'center'
            theme_text_color: 'Custom'
            text_color: (1, 0.5, 0.5, 1)  # Pink color
            font_style: 'H3'
            bold: True
            shadow_color: (0, 0, 0, 0.5)
            shadow_offset: (2, -2)
            size_hint_y: None
            height: dp(50)
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(400)  # Adjust the height to center the kitten better
            Image:
                id: kitten
                source: 'kitten.png'
                size_hint: None, None
                size: dp(100), dp(100)
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        MDSpinner:
            size_hint: None, None
            size: dp(46), dp(46)
            pos_hint: {'center_x': 0.5, 'center_y': 0.1}
            active: True

<MainScreen>:
    name: 'main'
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(20)
        padding: dp(20)
        MDLabel:
            text: "LOVE YOU"
            halign: 'center'
            theme_text_color: 'Custom'
            text_color: (1, 0.5, 0.5, 1)  # Pink color
            font_style: 'H3'
            bold: True
            shadow_color: (0, 0, 0, 0.5)
            shadow_offset: (2, -2)
            size_hint_y: None
            height: dp(50)
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(200)
            Image:
                id: kitten
                source: 'kitten.png'
                size_hint: None, None
                size: dp(100), dp(100)
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        MDLabel:
            text: "Эти комплименты тебе от Богдана, чтобы ты не грустила, когда меня нет рядом"
            halign: 'center'
            theme_text_color: 'Primary'
            size_hint_y: None
            height: self.texture_size[1]
        MDLabel:
            id: compliment_label
            text: "Нажми на кнопку для получения комплимента!"
            halign: 'center'
            theme_text_color: 'Secondary'
            size_hint_y: None
            height: self.texture_size[1]
        MDRaisedButton:
            text: "Получить комплимент"
            pos_hint: {'center_x': 0.5}
            on_press: app.show_compliment()
'''

class LoadingScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class ComplimentApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Pink"
        self.theme_cls.theme_style = "Light"
        self.title = "Lovers"  # Set the application title
        self.icon = "icon.png"  # Set the path to the icon file
        return Builder.load_string(KV)

    def on_start(self):
        Clock.schedule_once(self.start_kitten_walking, 0)
        Clock.schedule_once(self.switch_to_main, 3)

    def switch_to_main(self, dt):
        self.root.current = 'main'
        # Animate kitten only if it's not already animated
        if not hasattr(self, 'kitten_animation_started'):
            self.animate_kitten_main()
            self.kitten_animation_started = True

    def start_kitten_walking(self, dt):
        kitten = self.root.get_screen('loading').ids.kitten
        kitten.x = -kitten.width  # Start from outside the screen
        kitten.pos_hint = {'center_y': 0.5}  # Center vertically
        self.kitten_walking_animation = Animation(x=Window.width, duration=2.8)
        self.kitten_walking_animation.bind(on_complete=self.stop_kitten_walking)
        self.kitten_walking_animation.start(kitten)

    def stop_kitten_walking(self, animation, kitten):
        # Simply stop the animation once the kitten is out of the screen
        kitten.x = Window.width  # Ensure the kitten is out of the screen

    def animate_kitten_main(self):
        kitten = self.root.get_screen('main').ids.kitten
        kitten.x = -kitten.width  # Start from outside the screen
        animation = Animation(x=(Window.width - kitten.width) / 2, duration=2)  # Move to center
        animation.start(kitten)

    def show_compliment(self):
        compliment = random.choice(compliments)
        self.root.get_screen('main').ids.compliment_label.text=compliment
        self.play_meow()

    def play_meow(self):
        sound = SoundLoader.load('meow.mp3')
        if sound:
            sound.play()

    def daily_compliment(self, dt):
        compliment = random.choice(compliments)
        notification.notify(
            title="Ежедневный комплимент",
            message=compliment,
            timeout=10
        )


if __name__ == '__main__':
    ComplimentApp().run()
