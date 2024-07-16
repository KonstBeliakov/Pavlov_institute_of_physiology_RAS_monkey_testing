import datetime
import threading
from tkinter import LabelFrame
from try_again_window import TryAgainWindow
from time import perf_counter, sleep
import pandas as pd

from customtkinter import *

import utils
from monkey_windows import *
from settings_windows import *
from widgets import *
from settings import settings


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
        self.run_frame.grid(row=0, column=0)

        self.choose_experiment_label = CTkLabel(self.run_frame, text='Тип эксперимента')
        self.choose_experiment_label.grid(row=0, column=0)

        self.choose_experiment_combobox = CTkComboBox(self.run_frame, values=['Запоминание картинки',
                                                                               'Экстраполяция движения',
                                                                               'Новая картинка'])
        self.choose_experiment_combobox.grid(row=1, column=0)

        self.btn_settings = CTkButton(self.run_frame, text='Настроить эксперимент',
                                      command=self.experiment_settings)
        self.btn_settings.grid(row=1, column=1)

        self.timer_ask_label = CTkLabel(self.run_frame, text='Обнулить глобальный таймер эксперимента')
        self.timer_ask_label.grid(row=2, column=0)

        self.timer_radio_buttons = IntVar()
        self.timer_radio_buttons.set(0)
        self.radio_button_yes = CTkRadioButton(self.run_frame, text="Да", variable=self.timer_radio_buttons, value=1)
        self.radio_button_no = CTkRadioButton(self.run_frame, text="Нет", variable=self.timer_radio_buttons, value=0)
        self.radio_button_yes.grid(row=3, column=0)
        self.radio_button_no.grid(row=3, column=1)

        self.output_file_label = CTkLabel(self.run_frame, text='Файл записи результатов эксперимента')
        self.output_file_label.grid(row=4, column=0)

        self.output_file_entry = CTkEntry(self.run_frame)
        self.output_file_entry.grid(row=4, column=1)

        self.btn = CTkButton(self.run_frame, text="Запустить тестирование", command=self.open_about)
        self.btn.grid(row=5, column=0)

        self.run_error_label = CTkLabel(self.run_frame_top, text='', text_color='red')
        self.run_error_label.grid(row=1, column=0)

    def generate_canvases(self):
        self.graph_panel = GraphPanel(self.root, row=1, column=0)

    def update_graph_data(self, log):
        self.graph_panel.update(log)

    def open_about(self):
        if not self.started:
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

                utils.experiment_start()

                self.update_thread = threading.Thread(target=self.update_log)
                self.update_thread.start()
                self.update_second_screen_thread = threading.Thread(target=self.check_second_screen)
                self.update_second_screen_thread.start()

                self.window.mainloop()
            else:
                self.run_error_label.configure(text='Тип эксперимента не выбран')
        else:
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

    def update_log(self):
        self.frame_log_top = CTkFrame(self.run_frame_top)
        self.frame_log_top.grid(row=0, column=1)

        self.log_header_label = CTkLabel(self.frame_log_top, text='Результаты последних 10 тестов')
        self.log_header_label.pack(fill=X)

        while not self.window.log:
            sleep(1)

        experiment_type = self.window.experiment_type
        log_header = settings[f'current_log_header{experiment_type}']
        print(f'log_header: {log_header}')
        if log_header is None:
            log_header = ['Номер', 'Время с начала эксперимента', 'Время реакции', 'Ответ', 'Правильный ответ']

        self.log_frames = [CTkFrame(self.frame_log_top) for _ in range(11)]
        for log_frame in self.log_frames:
            log_frame.pack(fill=X, pady=2)

        for i in range(11):
            for j in range(len(log_header)):
                self.log_frames[i].grid_columnconfigure(j, weight=1)

        self.log_label = [[CTkLabel(self.log_frames[i], text='') for _ in range(len(log_header))] for i in
                          range(11)]

        for i in range(len(self.log_label)):
            for j in range(len(self.log_label[i])):
                self.log_label[i][j].grid(row=0, column=j, sticky="ew", padx=5)

        for j, text in enumerate(log_header):
            self.log_label[0][j].configure(text=text)

        self.generate_canvases()

        while True:
            for i, line in enumerate(self.window.log[max(len(self.window.log) - 10, 0):]):
                if line['Ответ'] is None:
                    color = '#fbf'
                elif line['Ответ'] == line['Правильный ответ']:
                    color = '#bfb'
                else:
                    color = '#fbb'

                self.log_frames[i + 1].configure(fg_color=color)

                for j, key in enumerate(log_header):
                    self.log_label[i + 1][j].configure(text=str(line[key]))

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
