from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton


class Example(MDApp):
    def build(self):
        self.data_tables = MDDataTable(
            use_pagination=False,
            check=True,
            column_data=[
                ("S.No.", dp(30)),
                ("Name", dp(30)),
                ("MAC", dp(60)),
            ],
            row_data=[
                (
                    "1",
                    "amogh",
                    "00:00:00:00:00:01",
                ),
                (
                    "2",
                    "ajay",
                    "00:00:00:00:00:02",
                ),
                (
                    "3",
                    "ashish",
                    "00:00:00:00:00:03",
                ),
                (
                    "4",
                    "bhumika",
                    "00:00:00:00:00:04",
                ),
                (
                    "5",
                    "satyam",
                    "00:00:00:00:00:05",
                ),
                (
                    "5",
                    "satyam",
                    "00:00:00:00:00:05",
                ),
                (
                    "6",
                    "satyam",
                    "00:00:00:00:00:05",
                ),
                (
                    "7",
                    "satyam",
                    "00:00:00:00:00:05",
                ),
                (
                    "8",
                    "satyam",
                    "00:00:00:00:00:05",
                ),
                (
                    "9",
                    "satyam",
                    "00:00:00:00:00:05",
                ),
                (
                    "10",
                    "satyam",
                    "00:00:00:00:00:05",
                ),
                (
                    "11",
                    "satyam",
                    "00:00:00:00:00:05",
                ),
                (
                    "12",
                    "satyam",
                    "00:00:00:00:00:05",
                ),
                (
                    "13",
                    "satyam",
                    "00:00:00:00:00:05",
                ),
                (
                    "14",
                    "satyam",
                    "00:00:00:00:00:05",
                ),
                (
                    "15",
                    "satyam",
                    "00:00:00:00:00:05",
                ),
                (
                    "16",
                    "satyam",
                    "00:00:00:00:00:05",
                ),
                (
                    "17",
                    "satyam",
                    "00:00:00:00:00:05",
                ),
                (
                    "18",
                    "satyam",
                    "00:00:00:00:00:05",
                ),
                (
                    "19",
                    "satyam",
                    "00:00:00:00:00:05",
                ),
                (
                    "20",
                    "satyam",
                    "00:00:00:00:00:05",
                ),
                (
                    "21",
                    "satyam",
                    "00:00:00:00:00:05",
                ),
            ],
            elevation=2,
        )
        self.data_tables.bind(on_row_press=self.on_row_press)
        # self.data_tables.bind(on_check_press=self.on_check_press)
        
        screen = MDScreen()
        screen.add_widget(self.data_tables)
        screen.add_widget(MDRaisedButton(
            text = "Press Me!",
            on_release = lambda x : self.temp()
            )
        )
        return screen

    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked.'''

        instance_row.ids.check.state = "down"
        print(instance_row.ids.check.state)

    def temp(self):
        print(self.data_tables)

        

Example().run()