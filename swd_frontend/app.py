from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.uix.snackbar import Snackbar
from kivy.clock import Clock
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.transition.transition import MDSwapTransition
from kivymd.uix.transition.transition import MDSlideTransition

from kivy.metrics import dp
from kivymd.uix.label import MDLabel
from kivymd.uix.spinner import MDSpinner
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.filemanager import MDFileManager

import os
import requests
import threading
import re

WINDOWS_MODE = True
DEBUG = True
LIVE_DOMAIN = False


if (WINDOWS_MODE) == True:
    Window.size = (380, 768)
    Window.top = 0
    Window.left = 986
if (LIVE_DOMAIN):
    DOMAIN = "https://student-tools-five.vercel.app/"
else:
    DOMAIN = "http://127.0.0.1:8000/"

UI = """

MDScreenManager:

    MDScreen:

        name : "sign_in"

        MDBoxLayout:

            orientation : "vertical"
            spacing : "0dp"

            MDTopAppBar:

                id : home_screen_top_app_bar
                title : "Sign in"
                left_action_items : [["menu", lambda x : app.temp()]]
                md_bg_color : app.theme_color
                elevation : 0

            MDBoxLayout:

                orientation : "vertical"
                spacing : "20dp"
                padding : "20dp"
                # md_bg_color : [0, 0, 1, 1]

                MDTextField:

                    id : sign_in_username
                    hint_text: "Username"
                    mode: "rectangle"
                    line_color_focus : app.theme_color
                    hint_text_color_focus : app.theme_color
                    text_color_focus: "black"

                    icon_right: "account"
                    icon_right_color_focus: app.theme_color

                MDTextField:

                    id : sign_in_password
                    hint_text: "Enter your password"
                    mode: "rectangle"
                    line_color_focus : app.theme_color
                    hint_text_color_focus : app.theme_color
                    text_color_focus: "black"
                    password : True

                    icon_right: "lock"
                    icon_right_color_focus: app.theme_color

                MDBoxLayout:

                    orientation : "horizontal"
                    spacing : "0dp"
                    padding : "0dp"
                    size_hint : (1, 0.05)
                    # md_bg_color : [1, 1, 0, 1]

                    MDCheckbox:
                        id : sign_in_show_password_checkbox
                        size_hint: None, None
                        size: "48dp", "48dp"
                        pos_hint: {'center_x': .1, 'center_y': .8}
                        on_release : app.show_hide_sign_in_password()
                        color_active : app.theme_color

                    MDLabel:
                        text : "Show Password"
                        pos_hint : {'center_x': .5, 'center_y': .8}

                    
                    MDTextButton:
                        id : sign_up_in_sign_in_page
                        text : "Forgot Password?"
                        pos_hint : {'center_x': .5, 'center_y': .8}
                        on_release : app.redirect_to_reset_password_page()
                        color : app.theme_color

                MDWidget:
                    # md_bg_color : [1, 0, 1, 1]
                    size_hint : (1, 0.001)

                MDRaisedButton:

                    id : sign_in
                    text : "Sign in"
                    font_size : "18sp"
                    pos_hint : {'center_x' : 0.5, 'center_y' : 0.5}
                    on_release : app.sign_in()
                    md_bg_color : app.theme_color

                    md_bg_color_disabled : app.theme_color
                    disabled_color : [1, 1, 1, 0]

                    elevation : 0
                    shadow_softness : 80
                    shadow_softness_size : 2

                    MDSpinner:
                        id : sign_in_spinner
                        color : [1, 1, 1, 1]
                        size_hint: None, None
                        size: dp(16), dp(16)
                        line_width : 1.5
                        active: False

                MDWidget:
                    md_bg_color : [1, 0, 1, 1]
                    size_hint : (1, 0.002)

                MDBoxLayout:
                    orientation : "vertical"
                    spacing : "10dp"
                    padding : "0dp"
                    size_hint : (1, 0.1)
                    # md_bg_color : [1, 0, 0, 1]

                    MDLabel:
                        text : "Don't have an account?"

                    MDTextButton:
                        id : sign_up_in_sign_in_page
                        text : "Sign up"
                        on_release : app.redirect_to_sign_up_page()
                        color : app.theme_color
                

                MDWidget:
                    # md_bg_color : [1, 0, 0, 1]
                    size_hint : (1, 0.7)

        MDWidget:

    MDScreen:

        name : "password_reset"

        MDBoxLayout:

            orientation : "vertical"
            spacing : "0dp"
            # md_bg_color : [1, 0, 0, 1]

            MDTopAppBar:

                id : home_screen_top_app_bar
                title : "Reset Password"
                left_action_items : [["arrow-left", lambda x : app.redirect_to_sign_in_page()]]
                md_bg_color : app.theme_color
                elevation : 0

            MDBoxLayout:

                orientation : "vertical"
                spacing : "20dp"
                padding : "20dp"
                # md_bg_color : [0, 1, 0, 1]

                MDTextField:

                    id : reset_password_username
                    hint_text: "Username"
                    mode: "rectangle"
                    line_color_focus : app.theme_color
                    hint_text_color_focus : app.theme_color
                    text_color_focus: "black"

                    icon_right: "account"
                    icon_right_color_focus: app.theme_color

                MDBoxLayout:
                    orientation : "horizontal"
                    spacing : "10dp"
                    padding : "0dp"
                    size_hint : (1, 0.05)
                    # md_bg_color : [1, 1, 0, 1]

                    MDTextField:

                        id : reset_password_email
                        hint_text: "Enter your email"
                        mode: "rectangle"
                        line_color_focus : app.theme_color
                        hint_text_color_focus : app.theme_color
                        text_color_focus: "black"
                        pos_hint : {'center_x' : 0.5, 'center_y' : 0.5}

                        icon_right: "email"
                        icon_right_color_focus: app.theme_color

                    MDRaisedButton:

                        id : reset_password_send_otp
                        text : "Send OTP"
                        font_size : "18sp"
                        pos_hint : {'center_x' : 0.5, 'center_y' : 0.45}
                        on_release : app.reset_password_send_otp()
                        md_bg_color : app.theme_color

                        md_bg_color_disabled : app.theme_color
                        disabled_color : [1, 1, 1, 0]
                    
                        elevation : 0
                        shadow_softness : 80
                        shadow_softness_size : 2

                    
                        MDSpinner:
                            id : reset_password_otp_sending_spinner
                            color : [1, 1, 1, 1]
                            size_hint: None, None
                            size: dp(16), dp(16)
                            line_width : 1.5
                            active: False

                MDTextField:

                    id : reset_password_otp
                    hint_text: "Enter OTP"
                    mode: "rectangle"
                    line_color_focus : app.theme_color
                    hint_text_color_focus : app.theme_color
                    text_color_focus: "black"

                MDTextField:

                    id : reset_password_password
                    hint_text: "Enter your password"
                    mode: "rectangle"
                    line_color_focus : app.theme_color
                    hint_text_color_focus : app.theme_color
                    text_color_focus: "black"
                    password : True

                    icon_right: "lock"
                    icon_right_color_focus: app.theme_color

                MDTextField:

                    id : reset_password_confirm_password
                    hint_text: "Confirm your password"
                    mode: "rectangle"
                    line_color_focus : app.theme_color
                    hint_text_color_focus : app.theme_color
                    text_color_focus: "black"
                    password : True

                    icon_right: "lock"
                    icon_right_color_focus: app.theme_color

                MDBoxLayout:

                    orientation : "horizontal"
                    spacing : "0dp"
                    padding : "0dp"
                    size_hint : (1, 0.01)
                    # md_bg_color : [1, 1, 0, 1]

                    MDCheckbox:
                        id : reset_password_show_password_checkbox
                        size_hint: None, None
                        size: "48dp", "48dp"
                        pos_hint: {'center_x': .1, 'center_y': .8}
                        on_release : app.show_hide_reset_password_password()
                        color_active : app.theme_color

                    MDLabel:
                        text : "Show Password"
                        pos_hint : {'center_x': .5, 'center_y': .8}

                MDWidget:
                    # md_bg_color : [1, 0, 1, 1]
                    size_hint : (1, 0.001)

                MDRaisedButton:

                    id : reset_password
                    text : "Reset Password"
                    font_size : "18sp"
                    pos_hint : {'center_x' : 0.5, 'center_y' : 0.5}
                    on_release : app.reset_password()
                    md_bg_color : app.theme_color

                    md_bg_color_disabled : app.theme_color
                    disabled_color : [1, 1, 1, 0]

                    elevation : 0
                    shadow_softness : 80
                    shadow_softness_size : 2

                    MDSpinner:
                        id : reset_password_spinner
                        color : [1, 1, 1, 1]
                        size_hint: None, None
                        size: dp(16), dp(16)
                        line_width : 1.5
                        active: False
                MDWidget:
                    size_hint : (1, 0.15)
                    # md_bg_color : [1, 1, 0, 1]
    MDScreen:

        name : "sign_up"

        MDBoxLayout:

            orientation : "vertical"
            spacing : "0dp"
            # md_bg_color : [1, 0, 0, 1]

            MDTopAppBar:

                id : home_screen_top_app_bar
                title : "Sign up"
                left_action_items : [["arrow-left", lambda x : app.redirect_to_sign_in_page()]]
                md_bg_color : app.theme_color
                elevation : 0

            MDBoxLayout:

                orientation : "vertical"
                spacing : "20dp"
                padding : "20dp"
                # md_bg_color : [0, 1, 0, 1]

                MDTextField:

                    id : sign_up_username
                    hint_text: "Username"
                    mode: "rectangle"
                    line_color_focus : app.theme_color
                    hint_text_color_focus : app.theme_color
                    text_color_focus: "black"

                    icon_right: "account"
                    icon_right_color_focus: app.theme_color

                MDTextField:

                    id : sign_up_password
                    hint_text: "Enter your password"
                    mode: "rectangle"
                    line_color_focus : app.theme_color
                    hint_text_color_focus : app.theme_color
                    text_color_focus: "black"
                    password : True

                    icon_right: "lock"
                    icon_right_color_focus: app.theme_color

                MDTextField:

                    id : sign_up_confirm_password
                    hint_text: "Confirm your password"
                    mode: "rectangle"
                    line_color_focus : app.theme_color
                    hint_text_color_focus : app.theme_color
                    text_color_focus: "black"
                    password : True

                    icon_right: "lock"
                    icon_right_color_focus: app.theme_color

                MDBoxLayout:

                    orientation : "horizontal"
                    spacing : "0dp"
                    padding : "0dp"
                    size_hint : (1, 0.2)
                    # md_bg_color : [0, 0, 1, 1]

                    MDCheckbox:
                        id : sign_up_show_password_checkbox
                        size_hint: None, None
                        size: "48dp", "48dp"
                        pos_hint: {'center_x': .1, 'center_y': .8}
                        on_release : app.show_hide_sign_up_password()
                        color_active : app.theme_color

                    MDLabel:
                        text : "Show Password"
                        pos_hint : {'center_x': .5, 'center_y': .8}

                MDBoxLayout:
                    orientation : "horizontal"
                    spacing : "10dp"
                    padding : "0dp"
                    size_hint : (1, 0.4)
                    # md_bg_color : [1, 1, 0, 1]

                    MDTextField:

                        id : sign_up_email
                        hint_text: "Enter your email"
                        mode: "rectangle"
                        line_color_focus : app.theme_color
                        hint_text_color_focus : app.theme_color
                        text_color_focus: "black"
                        pos_hint : {'center_x' : 0.5, 'center_y' : 0.5}

                        icon_right: "email"
                        icon_right_color_focus: app.theme_color

                    MDRaisedButton:

                        id : sign_up_send_otp
                        text : "Send OTP"
                        font_size : "18sp"
                        pos_hint : {'center_x' : 0.5, 'center_y' : 0.45}
                        on_release : app.sign_up_send_otp()
                        md_bg_color : app.theme_color

                        md_bg_color_disabled : app.theme_color
                        disabled_color : [1, 1, 1, 0]
                    
                        elevation : 0
                        shadow_softness : 80
                        shadow_softness_size : 2

                    
                        MDSpinner:
                            id : register_otp_sending_spinner
                            color : [1, 1, 1, 1]
                            size_hint: None, None
                            size: dp(16), dp(16)
                            line_width : 1.5
                            active: False


                MDTextField:

                    id : sign_up_otp
                    hint_text: "Enter OTP"
                    mode: "rectangle"
                    line_color_focus : app.theme_color
                    hint_text_color_focus : app.theme_color
                    text_color_focus: "black"

                MDBoxLayout:

                    orientation : "horizontal"
                    spacing : "0dp"
                    padding : "0dp"
                    size_hint : (1, 0.2)
                    # md_bg_color : [1, 1, 0, 1]

                    MDCheckbox:
                        id : sign_up_student_account_checkbox
                        size_hint: (None, None)
                        size: "48dp", "48dp"
                        pos_hint: {'center_x': .1, 'center_y': .8}
                        color_active : app.theme_color
                        active : True

                    MDLabel:
                        text : "Student Account"
                        pos_hint : {'center_x': .5, 'center_y': .8}

                MDWidget:
                    # md_bg_color : [1, 0, 1, 1]
                    size_hint : (1, 0.01)

                MDRaisedButton:

                    id : sign_up
                    text : "Sign up"
                    font_size : "18sp"
                    pos_hint : {'center_x' : 0.5, 'center_y' : 0.5}
                    on_release : app.sign_up()
                    md_bg_color : app.theme_color

                    md_bg_color_disabled : app.theme_color
                    disabled_color : [1, 1, 1, 0]

                    elevation : 0
                    shadow_softness : 80
                    shadow_softness_size : 2

                    MDSpinner:
                        id : sign_up_spinner
                        color : [1, 1, 1, 1]
                        size_hint: None, None
                        size: dp(16), dp(16)
                        line_width : 1.5
                        active: False
                
                MDWidget:
                    md_bg_color : [1, 0, 1, 1]
                    size_hint : (1, 0.01)

                MDBoxLayout:
                    orientation : "vertical"
                    spacing : "10dp"
                    padding : "0dp"
                    size_hint : (1, 0.3)
                    # md_bg_color : [0, 1, 1, 1]

                    MDLabel:
                        text : "Already have an account?"

                    MDTextButton:
                        text : "Sign in"
                        on_release : app.redirect_to_sign_in_page()
                        color : app.theme_color
            
                MDWidget:
                    # md_bg_color : [1, 0, 1, 1]
                    size_hint : (1, 0.5)
            
            # MDWidget:
    
    MDScreen:
        
        name : "home"

        MDNavigationLayout:

            MDScreenManager:
                
                MDScreen:

                    MDBoxLayout:

                        orientation : "vertical"
                        spacing : "0dp"

                        MDTopAppBar:

                            id : home_screen_top_app_bar
                            title : "Student Tools"
                            left_action_items : [["menu", lambda x: nav_drawer.set_state("open")]]
                            right_action_items : [["dots-vertical", lambda x: app.temp()]]
                            md_bg_color : app.theme_color
                            elevation : 0

                        MDBottomNavigation:
                            id : bottom_nav
                            panel_color : app.theme_color
                            text_color_normal: (0.99, 0.99, 0.99, 0.4)
                            text_color_active : (0.99, 0.99, 0.99, 1)
                            

                            MDBottomNavigationItem:
                                
                                name: "dashboard"
                                text: "Dashboard"
                                icon: "view-dashboard"
                                

                                MDLabel:
                                    text: "Dashboard"
                                    halign: "center"

                            MDBottomNavigationItem:
                                id : docs
                                name: "docs"
                                text: "Docs"
                                icon: "file-multiple"
                                on_tab_press : app.docs_press()
                                on_leave : app.docs_leave()

                                # MDLabel:
                                #     text: "Docs"
                                #     halign: "center"

                                # MDFloatingActionButton:
                                #     icon: "plus"
                                #     md_bg_color: app.theme_color
                                    

                                #     elevation : 0
                                #     shadow_softness : 80
                                #     shadow_softness_size : 2

                                #     pos_hint: {'center_x': .9, 'center_y': .07}

                            MDBottomNavigationItem:
                                name: "forums"
                                text: "Forums"
                                icon: "forum"
                                

                                MDLabel:
                                    text: "Forums"
                                    halign: "center"

                                MDFloatingActionButton:
                                    icon: "pencil"
                                    md_bg_color: app.theme_color
                                    style : "standard"

                                    elevation : 0
                                    shadow_softness : 80
                                    shadow_softness_size : 2

                                    pos_hint: {'center_x': .9, 'center_y': .07}

            MDNavigationDrawer:

                id: nav_drawer
                radius: (0, 16, 16, 0)

                MDNavigationDrawerMenu:

                    MDNavigationDrawerHeader:
                        title: "Student Tools"
                        title_color: "#4a4939"
                        # text: "Header text"
                        spacing: "4dp"
                        padding: "12dp", 0, 0, "32dp"

                    MDNavigationDrawerLabel:
                        text: "Tools"

                    MDNavigationDrawerItem:
                        icon: "view-dashboard"
                        text: "Dashboard"
                        text_color : [0, 0, 0, 1]   
                        icon_color : app.theme_color
                        focus_color: "#e7e4c0"
                        selected_color: app.theme_color
                        on_release : app.nav_drawer_dashboard()
                        

                    MDNavigationDrawerItem:
                        icon: "file-multiple"
                        text: "Docs"
                        text_color : [0, 0, 0, 1]
                        icon_color : app.theme_color
                        focus_color: "#e7e4c0"
                        selected_color: app.theme_color
                        on_release : app.nav_drawer_docs()
                    
                    MDNavigationDrawerItem:
                        icon: "forum"
                        text: "Forums"
                        text_color : [0, 0, 0, 1]
                        icon_color : app.theme_color
                        focus_color: "#e7e4c0"
                        selected_color: app.theme_color
                        on_release : app.nav_drawer_forums()


                    MDNavigationDrawerDivider:

                    MDNavigationDrawerItem:
                        icon: "cog"
                        text: "Settings"
                        text_color : [0, 0, 0, 1]
                        icon_color : app.theme_color
                        focus_color: "#e7e4c0"
                        selected_color: app.theme_color
                        on_release : app.nav_drawer_settings()

                    MDNavigationDrawerItem:
                        icon: "help-circle-outline"
                        text: "Help & Support"
                        text_color : [0, 0, 0, 1]
                        icon_color : app.theme_color
                        focus_color: "#e7e4c0"
                        selected_color: app.theme_color
                        on_release : app.nav_drawer_help_support()

                    MDNavigationDrawerDivider:

                    MDNavigationDrawerItem:
                        icon: "logout"
                        text: "Logout"
                        text_color : [0.7, 0, 0, 1]
                        icon_color : [0.7, 0, 0, 1]
                        focus_color: "#e7e4c0"
                        selected_color: [1, 0, 0, 1]
                        on_release : app.nav_drawer_logout()
        MDWidget: 
"""


class App(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.theme_color = [123/255, 2/255, 144/255, 255/255]
        self.domain = DOMAIN

        self.control_dict = {
            "sign_up_otp_sent_snackbar": False,
            "sign_up_otp_sent_snackbar_message": None,
            "sign_up_snackbar": False,
            "sign_up_snackbar_message": None,
            "account_created": False,
            "sign_in_snackbar": False,
            "sign_in_snackbar_message": None,
            "logged_in": False,
            "reset_password_otp_sent_snackbar": False,
            "reset_password_otp_sent_snackbar_message": None,
            "reset_password_snackbar": False,
            "reset_password_snackbar_message": None,
            "password_reset": False,
            "logout": False,
            "logout_snackbar_message": None,

            "docs_snackbar": False,
            "docs_snackbar_message": None,
            "show_docs_message": False,
            "docs_message": None,
            "show_files": False,
            "files": None,

            "file_path": None,
            "file_upload_snackbar" : False,
            "file_upload_snackbar_message" : None,

            "file_name" : None,
            "file_download_snackbar_message" : None,
            "file_download_snackbar" : False,

            "file_delete_snackbar_message" : None,
            "file_delete_snackbar" : False,
        }

        Clock.schedule_interval(self.control_method, 1/10)

        self.config_dict = {
            "username": None,
            "is_student": None,
            "session_id": None
        }

        self.file_manager = MDFileManager(
            select_path=self.select_path, exit_manager=self.exit_file_manager)
        self.file_manager.background_color_toolbar = self.theme_color
        self.file_manager.background_color_selection_button = self.theme_color
        self.file_manager.icon_color = self.theme_color
        self.file_manager.select_directory_on_press_button = lambda x: self.file_manager.close()

    def control_method(self, dt):

        if (self.control_dict["sign_up_otp_sent_snackbar"]):

            self.control_dict["sign_up_otp_sent_snackbar"] = False
            self.root.ids.sign_up_send_otp.disabled = False

            Snackbar(
                text=self.control_dict["sign_up_otp_sent_snackbar_message"],
                snackbar_x="9dp",
                snackbar_y="9dp",
                size_hint_x=0.95,
                duration=1.5
            ).open()

        if (self.control_dict["sign_up_snackbar"]):

            self.control_dict["sign_up_snackbar"] = False
            self.root.ids.sign_up.disabled = False

            Snackbar(
                text=self.control_dict["sign_up_snackbar_message"],
                snackbar_x="9dp",
                snackbar_y="9dp",
                size_hint_x=0.95,
                duration=1.5
            ).open()

        if (self.control_dict["account_created"]):

            self.control_dict["account_created"] = False
            self.redirect_to_sign_in_page()
            self.reset_signup_screen()

        if (self.control_dict["sign_in_snackbar"]):

            self.control_dict["sign_in_snackbar"] = False
            self.root.ids.sign_in.disabled = False
            Snackbar(
                text=self.control_dict["sign_in_snackbar_message"],
                snackbar_x="9dp",
                snackbar_y="9dp",
                size_hint_x=0.95,
                duration=1.5
            ).open()

        if (self.control_dict["logged_in"]):

            self.control_dict["logged_in"] = False
            self.root.ids.sign_in.disabled = False
            self.root.transition = MDSlideTransition()
            self.root.transition.direction = "up"
            self.root.current = "home"
            self.reset_signin_screen()

        if (self.control_dict["reset_password_otp_sent_snackbar"]):

            self.control_dict["reset_password_otp_sent_snackbar"] = False
            self.root.ids.reset_password_send_otp.disabled = False

            Snackbar(
                text=self.control_dict["reset_password_otp_sent_snackbar_message"],
                snackbar_x="9dp",
                snackbar_y="9dp",
                size_hint_x=0.95,
                duration=1.5
            ).open()

        if (self.control_dict["password_reset"]):

            self.control_dict["password_reset"] = False
            self.redirect_to_sign_in_page()
            self.reset_reset_password_screen()

        if (self.control_dict["reset_password_snackbar"]):

            self.control_dict["reset_password_snackbar"] = False
            self.root.ids.reset_password.disabled = False

            Snackbar(
                text=self.control_dict["reset_password_snackbar_message"],
                snackbar_x="9dp",
                snackbar_y="9dp",
                size_hint_x=0.95,
                duration=1.5
            ).open()

        if (self.control_dict["logout"]):

            self.control_dict["logout"] = False
            Snackbar(
                text=self.control_dict["logout_snackbar_message"],
                snackbar_x="9dp",
                snackbar_y="9dp",
                size_hint_x=0.95,
                duration=1.5
            ).open()

        if (self.control_dict["docs_snackbar"]):

            self.control_dict["docs_snackbar"] = False
            Snackbar(
                text=self.control_dict["docs_snackbar_message"],
                snackbar_x="9dp",
                snackbar_y="9dp",
                size_hint_x=0.95,
                duration=1.5
            ).open()

        if (self.control_dict["show_docs_message"]):

            self.control_dict["show_docs_message"] = False
            self.docs_spinner.active = False

            try:
                self.root.ids.docs.remove_widget(self.docs_message)
            except:
                pass
            try:
                self.root.ids.docs.remove_widget(self.docs_floating_button)
            except:
                pass
            try:
                self.root.ids.docs.remove_widget(self.file_list_scroll_view)
            except:
                pass
            try:
                self.root.ids.docs.remove_widget(self.docs_spinner)
            except:
                pass

            self.docs_message = MDLabel(
                text=self.control_dict["docs_message"],
                halign="center"
            )
            self.root.ids.docs.add_widget(self.docs_message)

            self.docs_floating_button = MDFloatingActionButton(
                icon="plus",
                md_bg_color=self.theme_color,
                elevation=0,
                shadow_color=[1, 1, 1, 1],
                pos_hint={'center_x': .9, 'center_y': .07},
                on_release=lambda x: self.upload_file_dialog_callback()
            )
            self.root.ids.docs.add_widget(self.docs_floating_button)

        if (self.control_dict["show_files"]):

            self.control_dict["show_files"] = False
            self.docs_spinner.active = False

            try:
                self.root.ids.docs.remove_widget(self.docs_message)
            except:
                pass
            try:
                self.root.ids.docs.remove_widget(self.docs_floating_button)
            except:
                pass
            try:
                self.root.ids.docs.remove_widget(self.file_list_scroll_view)
            except:
                pass
            try:
                self.root.ids.docs.remove_widget(self.docs_spinner)
            except:
                pass

            file_list = MDList()

            for file in self.control_dict["files"]:
                file_list.add_widget(
                    OneLineListItem(
                        text=file,
                        on_release = lambda x : self.file_actions(x.text)
                    )
                )

            self.file_list_scroll_view = MDScrollView()
            self.file_list_scroll_view.add_widget(file_list)

            self.docs_floating_button = MDFloatingActionButton(
                icon="plus",
                md_bg_color=self.theme_color,
                elevation=0,
                shadow_color=[1, 1, 1, 1],
                pos_hint={'center_x': .9, 'center_y': .07},
                on_release=lambda x: self.upload_file_dialog_callback()
            )

            self.root.ids.docs.add_widget(self.file_list_scroll_view)
            self.root.ids.docs.add_widget(self.docs_floating_button)

        if(self.control_dict["file_upload_snackbar"]):

            self.control_dict["file_upload_snackbar"] = False

            self.upload_file_spinner.active = False
            self.upload_file_button.disabled = False
            self.upload_file_dialog.dismiss()
            self.docs_press()

            Snackbar(
                text=self.control_dict["file_upload_snackbar_message"],
                snackbar_x="9dp",
                snackbar_y="9dp",
                size_hint_x=0.95,
                duration=1.5
            ).open()

        if(self.control_dict["file_download_snackbar"]):
            self.control_dict["file_download_snackbar"] = False
            Snackbar(
                text=self.control_dict["file_download_snackbar_message"],
                snackbar_x="9dp",
                snackbar_y="9dp",
                size_hint_x=0.95,
                duration=1.5
            ).open()

        if(self.control_dict["file_delete_snackbar"]):
            self.control_dict["file_delete_snackbar"] = False
            
            self.delete_file_spinner.active = False
            self.delete_file_button.disabled = False
            self.file_actions_dialog.dismiss()
            self.docs_press()

            Snackbar(
                text=self.control_dict["file_delete_snackbar_message"],
                snackbar_x="9dp",
                snackbar_y="9dp",
                size_hint_x=0.95,
                duration=1.5
            ).open()

    def select_path(self, path):
        '''
        It will be called when you click on the file name
        or the catalog selection button.

        :param path: path to the selected directory or file;
        '''
        self.control_dict["file_path"] = path
        self.file_manager.close()

        self.upload_file_spinner = MDSpinner(
            color=[1, 1, 1, 1],
            size_hint=(None, None),
            size=(dp(16), dp(16)),
            line_width=1.5,
            active=False
        )

        self.upload_file_button = MDFlatButton(
            self.upload_file_spinner,
            text="UPLOAD",
            # theme_text_color = "Custom",
            on_release=lambda button: self.upload_file()
        )

        self.upload_file_dialog = MDDialog(
            title="Upload Document",
            text="Do you want to upload this document?\n" + path,
            size_hint=(0.9, 0.2),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda button: self.upload_file_dialog.dismiss()
                ),
                self.upload_file_button,
            ],
            auto_dismiss=False
        )
        self.upload_file_dialog.open()



    def exit_file_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''
        self.file_manager.close()

    def upload_file_thread(self):

        url = self.domain + "/api/upload_file/"

        data = {
            "username" : self.config_dict["username"],
            "session_id" : self.config_dict["session_id"]
        }

        file = {
            "file" : open(f"{self.control_dict["file_path"]}", "rb"),
        }

        try:
            response = requests.post(url, data = data, files = file)
        except:
            self.upload_file_dialog.dismiss()
            self.control_dict["file_upload_snackbar_message"] = "Failed to connect to server."
            self.control_dict["file_upload_snackbar"] = True
            return

        # print(response.json())

        self.upload_file_dialog.dismiss()
        self.control_dict["file_upload_snackbar_message"] = response.json()["message"]    
        self.control_dict["file_upload_snackbar"] = True

    def upload_file(self):
        self.upload_file_button.disabled = True
        self.upload_file_button.disabled_color = [245/255, 245/255, 245/255, 1]
        self.upload_file_spinner.color = self.theme_color
        self.upload_file_spinner.active = True

        threading.Thread(target=self.upload_file_thread).start()

    def show_hide_sign_in_password(self):

        if self.root.ids.sign_in_show_password_checkbox.active:
            self.root.ids.sign_in_password.password = False
        else:
            self.root.ids.sign_in_password.password = True

    def show_hide_sign_up_password(self):
        if (self.root.ids.sign_up_show_password_checkbox.active):
            self.root.ids.sign_up_password.password = False
            self.root.ids.sign_up_confirm_password.password = False
        else:
            self.root.ids.sign_up_password.password = True
            self.root.ids.sign_up_confirm_password.password = True

    def show_hide_reset_password_password(self):
        if (self.root.ids.reset_password_show_password_checkbox.active):
            self.root.ids.reset_password_password.password = False
            self.root.ids.reset_password_confirm_password.password = False
        else:
            self.root.ids.reset_password_password.password = True
            self.root.ids.reset_password_confirm_password.password = True

    def redirect_to_sign_up_page(self):
        self.root.transition = MDSlideTransition()
        self.root.transition.direction = "left"
        self.root.current = "sign_up"

    def redirect_to_sign_in_page(self):

        self.root.transition = MDSlideTransition()
        self.root.transition.direction = "right"
        self.root.current = "sign_in"

    def redirect_to_reset_password_page(self):

        self.root.transition = MDSlideTransition()
        self.root.transition.direction = "left"
        self.root.current = "password_reset"

    def sign_in_thread(self):  # Thread_3

        url = self.domain + "/api/login/"

        data = {
            "username": self.root.ids.sign_in_username.text,
            "password": self.root.ids.sign_in_password.text
        }

        try:
            response = requests.post(url, data=data)
        except:
            self.root.ids.sign_in_spinner.active = False
            self.control_dict["sign_in_snackbar_message"] = "Failed to connect to server."
            self.control_dict["sign_in_snackbar"] = True
            return

        self.root.ids.sign_in_spinner.active = False

        if (response.status_code == 200):
            self.control_dict["logged_in"] = True
            self.config_dict["username"] = response.json()["username"]
            self.config_dict["is_student"] = response.json()["is_student"]
            self.config_dict["session_id"] = response.json()["session_id"]
        else:
            self.control_dict["sign_in_snackbar_message"] = response.json()[
                "message"]
            self.control_dict["sign_in_snackbar"] = True

    def sign_in(self):

        if (self.root.ids.sign_in_username.text == ""):
            Snackbar(
                text="Username is required.",
                snackbar_x="9dp",
                snackbar_y="9dp",
                size_hint_x=0.95,
                duration=1.5
            ).open()
            return

        if (self.root.ids.sign_in_password.text == ""):
            Snackbar(
                text="Password is required.",
                snackbar_x="9dp",
                snackbar_y="9dp",
                size_hint_x=0.95,
                duration=1.5
            ).open()
            return

        self.root.ids.sign_in.disabled = True
        self.root.ids.sign_in_spinner.active = True
        threading.Thread(target=self.sign_in_thread).start()

    def sign_up_send_otp_thread(self):  # Thread_1

        url = self.domain + "api/generate_registration_otp/"
        data = {"email": self.root.ids.sign_up_email.text}

        try:
            response = requests.post(url, data=data)
        except:
            self.root.ids.register_otp_sending_spinner.active = False
            self.control_dict["sign_up_otp_sent_snackbar_message"] = "Failed to connect to server."
            self.control_dict["sign_up_otp_sent_snackbar"] = True
            return

        self.root.ids.register_otp_sending_spinner.active = False
        self.control_dict["sign_up_otp_sent_snackbar_message"] = response.json()[
            "message"]
        self.control_dict["sign_up_otp_sent_snackbar"] = True

    def sign_up_send_otp(self):

        if (self.root.ids.sign_up_email.text == ""):
            Snackbar(
                text="Email is required.",
                snackbar_x="9dp",
                snackbar_y="9dp",
                size_hint_x=0.95,
                duration=1.5
            ).open()
            return

        self.root.ids.sign_up_send_otp.disabled = True
        self.root.ids.register_otp_sending_spinner.active = True
        threading.Thread(target=self.sign_up_send_otp_thread).start()

    def reset_password_send_otp_thread(self):
        url = self.domain + "api/generate_reset_password_otp/"
        data = {"username": self.root.ids.reset_password_username.text,
                "email": self.root.ids.reset_password_email.text
                }

        try:
            response = requests.post(url, data=data)
        except:
            self.root.ids.reset_password_otp_sending_spinner.active = False
            self.control_dict["reset_password_otp_sent_snackbar_message"] = "Failed to connect to server."
            self.control_dict["reset_password_otp_sent_snackbar"] = True
            return

        self.root.ids.reset_password_otp_sending_spinner.active = False
        self.control_dict["reset_password_otp_sent_snackbar_message"] = response.json()[
            "message"]
        self.control_dict["reset_password_otp_sent_snackbar"] = True

    def reset_password_send_otp(self):
        if (self.root.ids.reset_password_username.text == ""):
            Snackbar(
                text="Username is required.",
                snackbar_x="9dp",
                snackbar_y="9dp",
                size_hint_x=0.95,
                duration=1.5
            ).open()
            return

        if (self.root.ids.reset_password_email.text == ""):
            Snackbar(
                text="Email is required.",
                snackbar_x="9dp",
                snackbar_y="9dp",
                size_hint_x=0.95,
                duration=1.5
            ).open()
            return

        self.root.ids.reset_password_send_otp.disabled = True
        self.root.ids.reset_password_otp_sending_spinner.active = True
        threading.Thread(target=self.reset_password_send_otp_thread).start()

    def sign_up_thread(self):   # Thread_2

        url = self.domain + "api/registration/"
        data = {
            "username": self.root.ids.sign_up_username.text,
            "password": self.root.ids.sign_up_password.text,
            "email": self.root.ids.sign_up_email.text,
            "is_student": self.root.ids.sign_up_student_account_checkbox.active,
            "otp": int(self.root.ids.sign_up_otp.text)
        }

        try:
            response = requests.post(url, data=data)
        except:
            self.root.ids.sign_up_spinner.active = False
            self.control_dict["sign_up_snackbar_message"] = "Failed to connect to server."
            self.control_dict["sign_up_snackbar"] = True
            return

        self.root.ids.sign_up_spinner.active = False
        self.control_dict["sign_up_snackbar_message"] = response.json()[
            "message"]
        self.control_dict["sign_up_snackbar"] = True

        if (response.status_code == 201):
            self.control_dict["account_created"] = True

    def sign_up(self):

        if (self.root.ids.sign_up_username.text == ""):
            Snackbar(
                text="Username is required.",
                snackbar_x="9dp",
                snackbar_y="9dp",
                size_hint_x=0.95,
                duration=1.5
            ).open()
            return

        if (self.root.ids.sign_up_password.text == ""):
            Snackbar(
                text="Password is required.",
                snackbar_x="9dp",
                snackbar_y="9dp",
                size_hint_x=0.95,
                duration=1.5
            ).open()
            return

        if (self.root.ids.sign_up_password.text != self.root.ids.sign_up_confirm_password.text):
            Snackbar(
                text="Passwords do not match.",
                snackbar_x="9dp",
                snackbar_y="9dp",
                size_hint_x=0.95,
                duration=1.5
            ).open()
            return

        is_strong, message = self.check_password_strength(
            self.root.ids.sign_up_password.text)

        if (not is_strong):
            Snackbar(
                text=message,
                snackbar_x="9dp",
                snackbar_y="9dp",
                size_hint_x=0.95,
                duration=1.5
            ).open()

        if (self.root.ids.sign_up_email.text == ""):
            Snackbar(
                text="Email is required.",
                snackbar_x="9dp",
                snackbar_y="9dp",
                size_hint_x=0.95,
                duration=1.5
            ).open()
            return

        if (self.root.ids.sign_up_otp.text == ""):
            Snackbar(
                text="OTP is required.",
                snackbar_x="9dp",
                snackbar_y="9dp",
                size_hint_x=0.95,
                duration=1.5
            ).open()
            return

        self.root.ids.sign_up.disabled = True
        self.root.ids.sign_up_spinner.active = True
        threading.Thread(target=self.sign_up_thread).start()

    def reset_password_thread(self):

        url = self.domain + "api/reset_password/"
        data = {
            "username": self.root.ids.reset_password_username.text,
            "email": self.root.ids.reset_password_email.text,
            "otp": int(self.root.ids.reset_password_otp.text),
            "new_password": self.root.ids.reset_password_password.text,
        }

        print(data)

        try:
            response = requests.post(url, data=data)
        except:
            self.root.ids.reset_password_spinner.active = False
            self.control_dict["reset_password_snackbar_message"] = "Failed to connect to server."
            self.control_dict["reset_password_snackbar"] = True
            return

        self.root.ids.reset_password_spinner.active = False
        self.control_dict["reset_password_snackbar_message"] = response.json()[
            "message"]
        self.control_dict["reset_password_snackbar"] = True

        if (response.status_code == 200):
            self.control_dict["password_reset"] = True

    def reset_password(self):
        if (self.root.ids.reset_password_username.text == ""):
            Snackbar(
                text="Username is required.",
                snackbar_x="9dp",
                snackbar_y="9dp",
                size_hint_x=0.95,
                duration=1.5
            ).open()
            return

        if (self.root.ids.reset_password_email.text == ""):
            Snackbar(
                text="Email is required.",
                snackbar_x="9dp",
                snackbar_y="9dp",
                size_hint_x=0.95,
                duration=1.5
            ).open()
            return

        if (self.root.ids.reset_password_otp.text == ""):
            Snackbar(
                text="OTP is required.",
                snackbar_x="9dp",
                snackbar_y="9dp",
                size_hint_x=0.95,
                duration=1.5
            ).open()
            return

        if (self.root.ids.reset_password_password.text == ""):
            Snackbar(
                text="Password is required.",
                snackbar_x="9dp",
                snackbar_y="9dp",
                size_hint_x=0.95,
                duration=1.5
            ).open()
            return

        if (self.root.ids.reset_password_password.text != self.root.ids.reset_password_confirm_password.text):
            Snackbar(
                text="Passwords do not match.",
                snackbar_x="9dp",
                snackbar_y="9dp",
                size_hint_x=0.95,
                duration=1.5
            ).open()
            return

        is_strong, message = self.check_password_strength(
            self.root.ids.reset_password_password.text)

        if (not is_strong):
            Snackbar(
                text=message,
                snackbar_x="9dp",
                snackbar_y="9dp",
                size_hint_x=0.95,
                duration=1.5
            ).open()
            return

        self.root.ids.reset_password.disabled = True
        self.root.ids.reset_password_spinner.active = True
        threading.Thread(target=self.reset_password_thread).start()

    def check_password_strength(self, password):
        # Check length
        if len(password) < 8:
            return False, "Password must be at least 8 characters."

        # Check for uppercase letters
        if not re.search(r'[A-Z]', password):
            return False, "Password needs an uppercase letter."

        # Check for lowercase letters
        if not re.search(r'[a-z]', password):
            return False, "Password needs a lowercase letter."

        # Check for digits
        if not re.search(r'[0-9]', password):
            return False, "Password needs a digit."

        # Check for special characters
        if not re.search(r'[\W_]', password):
            return False, "Password needs a special character."

        return True, "Password is strong."

    def reset_signup_screen(self):

        self.root.ids.sign_up_username.text = ""
        self.root.ids.sign_up_password.text = ""
        self.root.ids.sign_up_confirm_password.text = ""
        self.root.ids.sign_up_email.text = ""
        self.root.ids.sign_up_otp.text = ""
        self.root.ids.sign_up_password.password = True
        self.root.ids.sign_up_confirm_password.password = True
        self.root.ids.sign_up_show_password_checkbox.active = False
        self.root.ids.sign_up_student_account_checkbox.active = True

    def reset_reset_password_screen(self):
        self.root.ids.reset_password_username.text = ""
        self.root.ids.reset_password_email.text = ""
        self.root.ids.reset_password_otp.text = ""
        self.root.ids.reset_password_password.text = ""
        self.root.ids.reset_password_confirm_password.text = ""
        self.root.ids.reset_password_password.password = True
        self.root.ids.reset_password_confirm_password.password = True
        self.root.ids.reset_password_show_password_checkbox.active = False

    def reset_signin_screen(self):

        self.root.ids.sign_in_username.text = ""
        self.root.ids.sign_in_password.text = ""
        self.root.ids.sign_in_password.password = True
        self.root.ids.sign_in_show_password_checkbox.active = False

    def nav_drawer_dashboard(self):
        self.root.ids.nav_drawer.set_state("close")
        self.root.ids.bottom_nav.switch_tab("dashboard")

    def nav_drawer_docs(self):
        self.root.ids.nav_drawer.set_state("close")
        self.root.ids.bottom_nav.switch_tab("docs")

    def nav_drawer_forums(self):
        self.root.ids.nav_drawer.set_state("close")
        self.root.ids.bottom_nav.switch_tab("forums")

    def nav_drawer_settings(self):
        pass

    def nav_drawer_help_support(self):
        pass

    def nav_drawer_logout(self):

        self.logout_dialog = MDDialog(
            title="Logout",
            text="Are you sure you want to logout?",
            size_hint=(0.9, 0.2),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda x: self.logout_dialog.dismiss()
                ),
                MDFlatButton(
                    text="LOGOUT",
                    on_release=lambda x: self.logout()
                )
            ],
        )
        self.logout_dialog.open()

    def reset_config_dict(self):

        self.config_dict["username"] = None
        self.config_dict["is_student"] = None
        self.config_dict["session_id"] = None

    def reset_control_dict(self):
        
        self.control_dict["sign_up_otp_sent_snackbar"] = False
        self.control_dict["sign_up_otp_sent_snackbar_message"] =  None
        self.control_dict["sign_up_snackbar"] = False
        self.control_dict["sign_up_snackbar_message"] = None
        self.control_dict["account_created"] = False
        self.control_dict["sign_in_snackbar"] = False
        self.control_dict["sign_in_snackbar_message"] = None
        self.control_dict["logged_in"] = False
        self.control_dict["reset_password_otp_sent_snackbar"] = False
        self.control_dict["reset_password_otp_sent_snackbar_message"] = None
        self.control_dict["reset_password_snackbar"] = False
        self.control_dict["reset_password_snackbar_message"] = None
        self.control_dict["password_reset"] = False
        self.control_dict["logout"] = False
        self.control_dict["logout_snackbar_message"] = None

        self.control_dict["docs_snackbar"] = False
        self.control_dict["docs_snackbar_message"] = None
        self.control_dict["show_docs_message"] = False
        self.control_dict["docs_message"] = None
        self.control_dict["show_files"] = False
        self.control_dict["files"] = None

        self.control_dict["file_path"] = None
        self.control_dict["file_upload_snackbar"] = False
        self.control_dict["file_upload_snackbar_message"] = None,

        self.control_dict["file_name"] = None,
        self.control_dict["file_download_snackbar_message"] = None,
        self.control["file_download_snackbar"] = False

    def logout_thread(self):

        url = self.domain + "api/logout/"

        data = {
            "username": self.config_dict["username"],
            "session_id": self.config_dict["session_id"]
        }

        response = requests.post(url, data=data)

        self.control_dict["logout_snackbar_message"] = response.json()[
            "message"]
        self.control_dict["logout"] = True

        self.reset_config_dict()
        self.reset_control_dict()

    def logout(self):

        threading.Thread(target=self.logout_thread).start()

        self.logout_dialog.dismiss()
        self.root.transition = MDSwapTransition()
        self.root.current = "sign_in"
        
        self.root.ids.nav_drawer.set_state("close")
        self.root.ids.bottom_nav.switch_tab("dashboard")
        try:
            self.root.ids.docs.remove_widget(self.docs_message)
        except:
            pass
        
        try:
            self.root.ids.docs.remove_widget(self.docs_floating_button)
        except:
            pass

        try:
            self.root.ids.docs.remove_widget(self.file_list_scroll_view)
        except:
            pass
        
        

    def docs_press_thread(self):

        url = self.domain + "api/list_files/"
        data = {
            "username": self.config_dict["username"],
            "session_id": self.config_dict["session_id"]
        }

        try:
            response = requests.post(url, data=data)
        except:
            self.docs_spinner.active = False
            self.control_dict["docs_snackbar_message"] = "Failed to connect to server."
            self.control_dict["docs_snackbar"] = True
            return

        # self.docs_spinner.active = False
        files = response.json()["files"]

        if (files != self.control_dict["files"]):

            self.control_dict["files"] = files
            if (len(files) == 0):
                self.control_dict["docs_message"] = "No files found."
                self.control_dict["show_docs_message"] = True
            else:
                self.control_dict["show_files"] = True

    def docs_press(self):
        if (self.control_dict["files"] == None):
            self.docs_spinner = MDSpinner(
                color=self.theme_color,
                size_hint=(None, None),
                size=(dp(32), dp(32)),
                line_width=2,
                active=True,
                pos_hint={'center_x': .5, 'center_y': .5}
            )
            self.root.ids.docs.add_widget(self.docs_spinner)

        threading.Thread(target=self.docs_press_thread).start()

    def docs_leave(self):
        pass

    def upload_file_dialog_callback(self):
        self.file_manager.show(os.path.expanduser("~"))

    def file_actions(self, file_name):

        self.control_dict["file_name"] = file_name

        self.download_file_spinner = MDSpinner(
            color=[1, 1, 1, 1],
            size_hint=(None, None),
            size=(dp(16), dp(16)),
            line_width=1.5,
            active=False
        )

        self.download_file_button = MDFlatButton(
            self.download_file_spinner,
            text="DOWNLOAD",
            on_release=lambda button: self.download_file()
        )
        
        self.delete_file_spinner = MDSpinner(
            color=[1, 1, 1, 1],
            size_hint=(None, None),
            size=(dp(16), dp(16)),
            line_width=1.5,
            active=False
        )

        self.delete_file_button = MDFlatButton(
            self.delete_file_spinner,
            text="DELETE",
            on_release=lambda button: self.delete_file()
        )

        self.file_actions_dialog = MDDialog(
            title="Select an action",
            text=f"{file_name}",
            size_hint=(0.9, 0.2),
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    on_release=lambda button: self.file_actions_dialog.dismiss()
                ),
                self.delete_file_button,
                self.download_file_button,
            ],
            auto_dismiss=False
        )
        self.file_actions_dialog.open()

    def download_file_thread(self):
        url = self.domain + "/api/download_file/"

        data = {"username" : self.config_dict["username"],
                "file_name": self.control_dict["file_name"],
                "session_id" : self.config_dict["session_id"]}  # Send filename in request body

        try:
            response = requests.post(url, data = data)  # Stream the file
        except:
            self.file_actions_dialog.dismiss()
            self.control_dict["file_download_snackbar_message"] = "Failed to connect to server."
            self.control_dict["file_download_snackbar"] = True
            return

        download_path = os.path.join(os.path.join(os.path.expanduser('~'), 'Downloads'), self.control_dict["file_name"])
        
        if (response.status_code == 200):
            with open(download_path, "wb") as file:
                file.write(response.content)  # Write the binary response to a file
        else:
            print(f"Failed to download file: {response.json()}")

        self.file_actions_dialog.dismiss()
        self.control_dict["file_download_snackbar_message"] = "File downloaded successfully!"   
        self.control_dict["file_download_snackbar"] = True

    def download_file(self):
        self.download_file_button.disabled = True
        self.download_file_button.disabled_color = [245/255, 245/255, 245/255, 1]
        self.download_file_spinner.color = self.theme_color
        self.download_file_spinner.active = True

        threading.Thread(target=self.download_file_thread).start()

    def delete_file_thread(self):
        url = self.domain + "/api/delete_file/"

        data = {
            "username" : self.config_dict["username"],
            "file_name" : self.control_dict["file_name"],
            "session_id" : self.config_dict["session_id"]
        }

        try:
            response = requests.post(url, data = data)
        except:
            self.upload_file_dialog.dismiss()
            self.control_dict["file_delete_snackbar_message"] = "Failed to connect to server."
            self.control_dict["file_delete_snackbar"] = True
            return

        self.control_dict["file_delete_snackbar_message"] = response.json()["message"]    
        self.control_dict["file_delete_snackbar"] = True

    def delete_file(self):
        self.delete_file_button.disabled = True
        self.delete_file_button.disabled_color = [245/255, 245/255, 245/255, 1]
        self.delete_file_spinner.color = self.theme_color
        self.delete_file_spinner.active = True

        threading.Thread(target=self.delete_file_thread).start()

    def temp(self):
        if (DEBUG):
            print(self.config_dict)
            print(self.control_dict)
            print((os.path.join(os.path.join(os.path.expanduser('~'), 'Downloads'), 'test.txt')))
            # self.root.transition.direction = "left"
            # self.root.current = "home"

    def on_start(self):
        if (DEBUG):
            self.fps_monitor_start()

    def build(self):
        return Builder.load_string(UI)

if __name__ == "__main__":
    App().run()
