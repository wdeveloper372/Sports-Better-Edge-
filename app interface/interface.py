from kivy.app import App
from kivy.lang import Builder

kv = Builder.load_string("""

BoxLayout:
    orientation: "vertical"
    Button:
        text: "Click Me!"
""")

class MainApp(App):
    def build(self):
        return kv

MainApp().run()