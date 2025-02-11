from customtkinter import *

from widgets import *
import utils


class DeviseCheckFrame:
    def __init__(self, root, app):
        self.frame_number = 2
        self.root = root
        self.app = app
        self.devise_check_entries = WidgetList(root, 0, 0, [
            {'text': 'Порт', 'value_type': str, 'save_value': 'port'},
            {'text': 'Частота', 'value_type': int, 'min_value': 0, 'save_value': 'baudrate'}
        ])
        self.main_frame = CTkFrame(root)
        self.main_frame.grid(row=0, column=0)
        # -------------------- ARDUINO FRAME --------------------
        self.arduino_frame = CTkFrame(self.main_frame)
        self.arduino_frame.grid(row=0, column=0, sticky='ns', padx=5, pady=5)

        self.arduino_frame_header = CTkLabel(master=self.arduino_frame, text='Проверка управляющей платы')
        self.arduino_frame_header.grid(row=0, column=0)

        self.port_available_label = CTkLabel(master=self.arduino_frame, text='Управляющая плата не подключена', text_color="#f66")
        self.port_available_label.grid(row=1, column=0)

        self.check_devise_button = CTkButton(self.arduino_frame, text='Подключиться к управляющей плате',
                                             command=self.devise_check)
        self.check_devise_button.grid(row=2, column=0, padx=4, pady=2)

        self.button_check = [
            CTkButton(self.arduino_frame, text='Проверить поилку', command=utils.positive_reinforcement),
            CTkButton(self.arduino_frame, text='Проверить подъем заслонки', command=utils.disable_anser_entry),
            CTkButton(self.arduino_frame, text='Проверить опускание заслонки', command=utils.anable_answer_entry)
        ]

        for i, button in enumerate(self.button_check):
            button.grid(row=i + 3, column=0, padx=4, pady=2)

        # -------------------- SECOND SCREEN FRAME --------------------

        self.second_screen_frame = CTkFrame(self.main_frame)
        self.second_screen_frame.grid(row=0, column=1, sticky='ns', padx=5, pady=5)

        self.second_screen_frame_header = CTkLabel(master=self.second_screen_frame, text='Проверка второго монитора')
        self.second_screen_frame_header.grid(row=0, column=0)

        self.paint_second_screen_button = CTkButton(self.second_screen_frame, text=f'Закрасить экспериментальное окно',
                                                    command=utils.paint_second_monitor)

        self.paint_second_screen_button.grid(row=1, column=0, padx=4, pady=2)

        self.check_second_screen_button = CTkButton(self.second_screen_frame, text='Проверить второй монитор',
                                                    command=self.check_second_screen)
        self.check_second_screen_button.grid(row=2, column=0, padx=4, pady=2)

        # --------------------------------------------------------------

        self.devise_check_error_label = CTkLabel(root, text='', text_color='red')
        self.devise_check_error_label.grid(row=1, column=0)

        self.devise_check()

    def devise_check(self):
        if (error_text := self.devise_check_entries.save_values(check_validity=True)) is not None:
            self.devise_check_error_label.configure(text=error_text)
        else:
            self.devise_check_error_label.configure(text='')
            utils.check_serial()

            if utils.serial_available:
                self.port_available_label.configure(text="Управляющая плата подключена", text_color="#6f6")
            else:
                self.port_available_label.configure(text="Управляющая плата не подключена", text_color="#f66")

    def check_second_screen(self):
        self.second_screen_copy = SecondScreenCopy(self.second_screen_frame, 0, 3)
