import datetime
import threading
from try_again_window import TryAgainWindow
from time import perf_counter, sleep
import win32api
import pandas as pd

from customtkinter import *

import utils
from monkey_windows import *
from settings_windows import *
from widgets import *
from settings import settings, APPLICATION_RUNNING


class RunFrame:
    def __init__(self, root, app):
        self.log_label = None
        self.try_again_window = None
        self.window = None
        self.experiment_settings_window = None

        self.root = root
        self.app = app
        self.started = False

        self.run_frame_top = CTkFrame(root)
        self.run_frame_top.grid(row=0, column=0)
        self.run_frame = CTkFrame(self.run_frame_top)
        self.run_frame.grid(row=0, column=0, sticky='ns')

        self.run_frame_header_label = CTkLabel(self.run_frame, text='Настройки эксперимента')
        self.run_frame_header_label.grid(row=0, column=0)

        self.choose_experiment_label = CTkLabel(self.run_frame, text='Тип эксперимента')
        self.choose_experiment_label.grid(row=1, column=0)

        self.choose_experiment_combobox = CTkComboBox(self.run_frame, values=['Запоминание картинки',
                                                                              'Экстраполяция движения',
                                                                              'Новая картинка'])
        self.choose_experiment_combobox.grid(row=2, column=0)

        self.btn_settings = CTkButton(self.run_frame, text='Настроить эксперимент',
                                      command=self.experiment_settings)
        self.btn_settings.grid(row=2, column=1)

        self.timer_ask_label = CTkLabel(self.run_frame, text='Обнулить глобальный таймер эксперимента')
        self.timer_ask_label.grid(row=3, column=0)

        self.timer_radio_buttons = IntVar()
        self.timer_radio_buttons.set(0)
        self.radio_button_yes = CTkRadioButton(self.run_frame, text="Да", variable=self.timer_radio_buttons, value=1)
        self.radio_button_no = CTkRadioButton(self.run_frame, text="Нет", variable=self.timer_radio_buttons, value=0)
        self.radio_button_yes.grid(row=3, column=1)
        self.radio_button_no.grid(row=3, column=2)

        self.output_file_label = CTkLabel(self.run_frame, text='Файл записи результатов эксперимента')
        self.output_file_label.grid(row=4, column=0)

        self.output_file_entry = CTkEntry(self.run_frame)
        self.output_file_entry.grid(row=4, column=1)

        self.btn = CTkButton(self.run_frame, text="Запустить тестирование", command=self.open_about)
        self.btn.grid(row=5, column=0)

        self.close_experiment_window_label = CTkLabel(master=self.run_frame,
                                                      text='Для завершения эксперимента можно нажать клавишу t')

        self.run_error_label = CTkLabel(self.run_frame_top, text='', text_color='red')
        self.run_error_label.grid(row=1, column=0)

    def generate_canvases(self):
        self.graph_panel = GraphPanel(self.root, row=1, column=0)

    def update_graph_data(self, log):
        self.graph_panel.update(log)

    def open_about(self):
        if self.started:
            self.close_experiment_window()
        else:
            if hasattr(self, "frame_log_top"):
                self.frame_log_top.destroy()
            match self.choose_experiment_combobox.get():
                case 'Запоминание картинки':
                    self.window = MonkeyWindow1()
                case 'Экстраполяция движения':
                    self.window = MonkeyWindow2()
                case 'Новая картинка':
                    self.window = MonkeyWindow3()

            if self.choose_experiment_combobox.get():
                self.run_error_label.configure(text='')
                if self.timer_radio_buttons or not settings['experiment_start']:
                    settings['experiment_start'] = perf_counter()

                self.btn.configure(text="Завершить тестирование")
                self.started = True

                print('start_experiment_sound')
                utils.experiment_start()

                self.update_thread = threading.Thread(target=self.update_log)
                self.update_thread.start()
                self.update_second_screen_thread = threading.Thread(target=self.check_second_screen)
                self.update_second_screen_thread.start()

                if settings['move_cursor']:
                    self.move_cursor_thread = threading.Thread(target=self.move_cursor)
                    self.move_cursor_thread.start()

                self.close_experiment_window_label.grid(row=6, column=0)

                self.window.mainloop()
            else:
                self.run_error_label.configure(text='Тип эксперимента не выбран')

    def update_log(self):
        self.frame_log_top = CTkFrame(self.run_frame_top)
        self.frame_log_top.grid(row=0, column=1)

        self.log_header_label = CTkLabel(self.frame_log_top, text='Результаты последних 10 тестов')
        self.log_header_label.pack(fill=X)

        while not self.window.log:
            sleep(1)

        experiment_type = self.window.experiment_type
        log_header = settings[f'current_log_header{experiment_type}']

        if log_header is None:
            log_header = ['Номер', 'Время с начала эксперимента', 'Время реакции', 'Ответ', 'Правильный ответ']

        frame1 = CTkFrame(self.frame_log_top)
        frame1.pack(fill=X)

        self.log_label = [[CTkLabel(frame1, text='') for _ in range(len(log_header))] for _ in
                          range(11)]

        for i, row in enumerate(self.log_label):
            for j, label in enumerate(row):
                label.grid(row=i, column=j, sticky="ew", padx=1)

        # setting the text in the first row of the table
        for label, text in zip(self.log_label[0], log_header):
            label.configure(text=text)

        self.generate_canvases()

        # Chaning colors and text in the table
        while APPLICATION_RUNNING:
            for i, line in enumerate(self.window.log[max(len(self.window.log) - 10, 0):]):
                if line['Ответ'] is None:
                    color = '#fbf'
                elif line['Ответ'] == line['Правильный ответ']:
                    color = '#bfb'
                else:
                    color = '#fbb'

                for j, key in enumerate(log_header):
                    self.log_label[i + 1][j].configure(text=str(line[key]), fg_color=color, text_color="#333")

            self.update_graph_data(self.window.log)
            sleep(1)

    def experiment_settings(self):
        match self.choose_experiment_combobox.get():
            case 'Запоминание картинки':
                self.experiment_settings_window = ExperimentSettingsWindow1()
            case 'Экстраполяция движения':
                self.experiment_settings_window = ExperimentSettingsWindow2()
            case 'Новая картинка':
                self.experiment_settings_window = ExperimentSettingsWindow3()
        if self.choose_experiment_combobox.get():
            self.experiment_settings_window.mainloop()
        else:
            self.run_error_label.configure(text='Перед тем как настроить эксперимент выберите его тип')

    def save_experiment_data(self, path, autosave=False):
        df = pd.DataFrame(self.window.log)
        print('autosave...')
        filename = f'{str(datetime.datetime.now()).split(".")[0].replace(":", "_")} {self.window.experiment_type}.xlsx'
        print(f'filename: {filename}')
        print(f'path: data/{filename}')
        df.to_excel(f'data/{filename}')
        if not autosave:
            print('saving...')
            df.to_excel(path)

    def check_second_screen(self):
        self.second_screen_copy = SecondScreenCopy(self.run_frame_top, 2, 0)

    def move_cursor(self):
        while self.started:
            sleep(0.1)
            win32api.SetCursorPos((-100, 100))

    def close_experiment_window(self):
        self.close_experiment_window_label.grid_forget()
        self.window.destroy()
        self.btn.configure(text="Запустить тестирование")
        self.started = False
        try:
            self.save_experiment_data(self.output_file_entry.get())
        except Exception as err:
            print(f'При сохранении данных произошла ошибка: {err}')
            self.try_again_window = TryAgainWindow(self)
            self.try_again_window.mainloop()
        else:
            print('Данные эксперимента сохранены успешно')
