import datetime
import threading
from tkinter import *
from try_again_window import TryAgainWindow
from time import perf_counter, sleep
import pandas as pd

from tkinter import ttk
import tkinter as tk

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import utils
from monkey_windows import *
from settings_windows import *
from settings import settings
from widgets.second_screen_copy import SecondScreenCopy


class RunFrame:
    def __init__(self, root, app):
        self.log_label = None
        self.try_again_window = None
        self.window = None
        self.experiment_settings_window = None

        self.root = root
        self.app = app
        self.started = False

        self.run_frame_top = LabelFrame(root, text='Настройки запуска')
        self.run_frame_top.grid(row=0, column=0)
        self.run_frame = Frame(self.run_frame_top)
        self.run_frame.pack()

        self.choose_experiment_label = Label(self.run_frame, text='Тип эксперимента')
        self.choose_experiment_label.grid(row=0, column=0)

        self.choose_experiment_combobox = ttk.Combobox(self.run_frame, values=['Запоминание картинки',
                                                                               'Экстраполяция движения',
                                                                               'Новая картинка'])
        self.choose_experiment_combobox.grid(row=1, column=0)

        self.btn_settings = tk.Button(self.run_frame, text='Настроить эксперимент',
                                      command=self.experiment_settings)
        self.btn_settings.grid(row=1, column=1)

        self.timer_ask_label = Label(self.run_frame, text='Обнулить глобальный таймер эксперимента')
        self.timer_ask_label.grid(row=2, column=0)

        self.timer_radio_buttons = IntVar()
        self.timer_radio_buttons.set(0)
        self.radio_button_yes = Radiobutton(self.run_frame, text="Да", variable=self.timer_radio_buttons, value=1)
        self.radio_button_no = Radiobutton(self.run_frame, text="Нет", variable=self.timer_radio_buttons, value=0)
        self.radio_button_yes.grid(row=3, column=0)
        self.radio_button_no.grid(row=3, column=1)

        self.output_file_label = Label(self.run_frame, text='Файл записи результатов эксперимента')
        self.output_file_label.grid(row=4, column=0)

        self.output_file_entry = Entry(self.run_frame)
        self.output_file_entry.grid(row=4, column=1)

        self.btn = tk.Button(self.run_frame, text="Запустить тестирование", command=self.open_about)
        self.btn.grid(row=5, column=0)

        self.run_error_label = Label(self.run_frame_top, text='', fg='red')
        self.run_error_label.pack()

        self.second_screen_canvas = Canvas(root)
        self.second_screen_canvas.grid(row=0, column=2)

        self.figure = plt.Figure(figsize=(5, 5))
        self.graph_canvas = FigureCanvasTkAgg(self.figure, root)
        self.graph_canvas.get_tk_widget().grid(row=1, column=0)
        self.figure_subplot = self.figure.add_subplot(1, 1, 1)

        self.draw_graph([0, 1, 2], [5, 3, 7])

    def draw_graph(self, x, y):
        self.figure_subplot.clear()
        self.figure_subplot.plot(x, y)
        self.graph_canvas.draw()

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
        self.frame_log_top = LabelFrame(self.root, text='Результаты последних 10 тестов')
        self.frame_log_top.grid(row=0, column=1)

        self.log_label = [[tk.Label(self.frame_log_top, text='') for _ in range(len(self.window.log[0]))] for _ in
                          range(11)]

        for i in range(len(self.log_label)):
            for j in range(len(self.log_label[i])):
                self.log_label[i][j].grid(row=i, column=j)

        for j, text in enumerate(self.window.log[0]):
            self.log_label[0][j].configure(text=text)
        sleep(1)
        while True:
            for i, line in enumerate(self.window.log[max(len(self.window.log) - 10, 1):]):
                for j, text in enumerate(line):
                    if line[-1] == line[-2]:
                        color = '#0f0'
                    elif line[-2] == line[-3] is None:
                        color = '#f0f'
                    else:
                        color = '#f00'
                    self.log_label[i + 1][j].configure(text=str(text), fg=color)

            graph_data = [0]
            for i, line in enumerate(self.window.log):
                if line[-1] == line[-2]:
                    graph_data.append(graph_data[-1] + 1)
                else:
                    graph_data.append(graph_data[-1] - 1)
            self.draw_graph(list(range(len(graph_data))), graph_data)
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
        df = pd.DataFrame(
            {name: [str(line[i]) for line in self.window.log[1:]] for i, name in enumerate(self.window.log[0])})
        print('autosave...')
        filename = f'{str(datetime.datetime.now()).split(".")[0].replace(":", "_")} {self.window.experiment_type}.xlsx'
        print(f'filename: {filename}')
        print(f'path: data/{filename}')
        df.to_excel(f'data/{filename}')
        if not autosave:
            print('saving...')
            df.to_excel(path)

    def check_second_screen(self):
        self.second_screen_copy = SecondScreenCopy(self.root, 2, 0)
