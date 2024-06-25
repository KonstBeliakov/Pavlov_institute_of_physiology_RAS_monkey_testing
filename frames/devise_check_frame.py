import utils
from widgets.second_screen_copy import SecondScreenCopy
from widgets.widget_list import WidgetList
from tkinter import *


class DeviseCheckFrame:
    def __init__(self, root, app):
        self.frame_number = 2
        self.root = root
        self.app = app
        self.devise_check_entries = WidgetList(root, 0, 0, [
            {'text': 'Порт', 'value_type': str, 'save_value': 'port'},
            {'text': 'Частота', 'value_type': int, 'min_value': 0, 'save_value': 'baudrate'}
        ])

        self.check_devise_button = Button(root, text='Подключиться к управляющей плате',
                                          command=self.devise_check)
        self.check_devise_button.grid(row=1, column=0)

        self.check_second_screen_button = Button(root, text='Проверить второй монитор',
                                                 command=self.check_second_screen)
        self.check_second_screen_button.grid(row=2, column=0)

        self.devise_check_error_label = Label(root, text='', fg='red')
        self.devise_check_error_label.grid(row=3, column=0)

        self.button_check = [
            Button(root, text='Проверить поилку', command=utils.positive_reinforcement),
            Button(root, text='Проверить подъем заслонки', command=utils.disable_anser_entry),
            Button(root, text='Проверить опускание заслонки', command=utils.anable_answer_entry)
        ]

        for i, button in enumerate(self.button_check):
            button.grid(row=6 + i, column=0)

    def devise_check(self):
        if (error_text := self.devise_check_entries.save_values(check_validity=True)) is not None:
            self.devise_check_error_label.configure(text=error_text)
        else:
            self.devise_check_error_label.configure(text='')
            utils.check_serial()

            if utils.serial_available:
                self.app.test_image[self.frame_number].configure(file='pictograms/yes.png')
            else:
                self.app.test_image[self.frame_number].configure(file='pictograms/no.png')

    def check_second_screen(self):
        self.second_screen_copy = SecondScreenCopy(self.root, 0, 5)
