from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.metrics import dp  # Import dp for density-independent pixels
from random import choice

KV = '''
MDLabel:
    text : "Hello World;alskdfja;lskdfja;lsdkfj a;slkdfj ;alksdfj; alskfdj sad;lkfj "
    halign : "center"
    color : [1, 0, 0, 1]
    md_bg_color : [0, 1, 0, 1]
    adaptive_size : True

'''

class TestApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        return Builder.load_string(KV)

TestApp().run()