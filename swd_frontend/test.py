from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList

Window.size = (380, 768)
Window.top = 0
Window.left = 986

class Test(MDApp):

    def temp(self):
        print("reaching...")
        self.root.ids.nav.switch_tab('screen 2')

    def temp2(self):

        scroll_view = MDScrollView()

        md_list = MDList(
            spacing ="10dp",
            padding = "10dp" 
        )

        card = MDCard(
            size_hint=(None, None),
            size=("280dp", "180dp"),
            pos_hint={"center_x": .5, "center_y": .5},
            md_bg_color=[1, 0, 0, 1]
        )

        label = MDLabel(
            text="Hello",
            halign="center"
        )

        card.add_widget(label)
        md_list.add_widget(card)
        scroll_view.add_widget(md_list)
        self.root.ids.home.add_widget(scroll_view)

    def build(self):
        return Builder.load_string(
            '''
MDScreen:
    id : home

    # MDScrollView:
    #     MDList:
    #         id : list
    #         spacing : "10dp"
    #         padding : "10dp"   

    #         MDCard:
    #             md_bg_color : [1, 0, 0, 1]
    #             size_hint: None, None
    #             size: "280dp", "180dp"
    #             pos_hint: {"center_x": .5, "center_y": .5}
            
    #         MDCard:
    #             md_bg_color : [0, 1, 0, 1]
    #             size_hint: None, None
    #             size: "280dp", "180dp"
    #             pos_hint: {"center_x": .5, "center_y": .5}

    MDRaisedButton:
        text : "Press Me"
        on_release : app.temp2()
'''
        )


Test().run()