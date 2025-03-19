from kivy.lang import Builder
from kivymd.app import MDApp


class Test(MDApp):

    def temp(self):
        print("reaching...")
        self.root.ids.nav.switch_tab('screen 2')

    def build(self):
        return Builder.load_string(
            '''
MDScreen:

    MDFlatButton:
        text : "80.91 106"
        theme_text_color: "Custom"
        text_color: 1, 0, 0, 1
        pos_hint : {"center_x": .5, "center_y": .5}
'''
        )


Test().run()