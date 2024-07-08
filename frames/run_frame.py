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

    def generate_canvases(self):
        self.figure1 = plt.Figure(figsize=(5, 5))
        self.figure1.suptitle(f'Кривые ответов по задержкам')
        self.graph_canvas1 = FigureCanvasTkAgg(self.figure1, self.root)
        self.graph_canvas1.get_tk_widget().grid(row=1, column=0)
        self.figure_subplot1 = self.figure1.add_subplot()
        self.figure_subplot1.legend([f'Задержка {delay} секунд' for delay in settings['delay'][1]])

        self.figure2 = plt.Figure(figsize=(5, 5))
        self.figure2.suptitle(f'Среднее время ответа по задержкам')
        self.graph_canvas2 = FigureCanvasTkAgg(self.figure2, self.root)
        self.graph_canvas2.get_tk_widget().grid(row=1, column=1)
        self.figure_subplot2 = self.figure2.add_subplot()

        self.figure3 = plt.Figure(figsize=(5, 5))
        self.figure3.suptitle(f'Процент правильных ответов по задержкам')
        self.graph_canvas3 = FigureCanvasTkAgg(self.figure3, self.root)
        self.graph_canvas3.get_tk_widget().grid(row=1, column=2)
        self.figure_subplot3 = self.figure3.add_subplot()

        self.figure4 = plt.Figure(figsize=(5, 5))
        self.figure4.suptitle(f'Процент отказов по задержкам')
        self.graph_canvas4 = FigureCanvasTkAgg(self.figure4, self.root)
        self.graph_canvas4.get_tk_widget().grid(row=1, column=3)
        self.figure_subplot4 = self.figure4.add_subplot()

        self.graph_canvas1.draw()
        self.graph_canvas2.draw()
        self.graph_canvas3.draw()
        self.graph_canvas4.draw()

    def update_graph_data(self, log):
        delays = sorted(settings['delay'][1])

        graph_data = [[0] for _ in range(len(delays))]
        for i, line in enumerate(log):
            index = delays.index(line['Текущая отсрочка'])
            if line['Ответ'] is None:
                graph_data[index].append(graph_data[index][-1])
            elif line['Ответ'] == line['Правильный ответ']:
                graph_data[index].append(graph_data[index][-1] + 1)
            else:
                graph_data[index].append(graph_data[index][-1] - 1)

        graph_number = len(settings['delay'][1])
        self.figure_subplot1.clear()
        for i in range(graph_number):
            self.figure_subplot1.plot(list(range(len(graph_data[i]))), graph_data[i])

        delays = sorted(settings['delay'][1])
        time_sum = {delay: 0 for delay in delays}
        time_num = {delay: 0 for delay in delays}

        for line in log:
            if line['Время реакции'] is not None:
                time_sum[line['Текущая отсрочка']] += line['Время реакции']
                time_num[line['Текущая отсрочка']] += 1

        avg_time = []
        for delay in delays:
            if time_num[delay]:
                avg_time.append(time_sum[delay] / time_num[delay])
            else:
                avg_time.append(0)

        self.figure_subplot2.clear()
        self.figure_subplot2.plot(delays, avg_time)

        correct_answer_count = {delay: 0 for delay in delays}
        total_answer_count = {delay: 0 for delay in delays}
        refusals_count = {delay: 0 for delay in delays}
        total_presentation_count = {delay: 0 for delay in delays}

        for line in log:
            total_presentation_count[line['Текущая отсрочка']] += 1
            if line['Отказ от ответа']:
                refusals_count[line['Текущая отсрочка']] += 1
            else:
                total_answer_count[line['Текущая отсрочка']] += 1
                if line['Ответ'] == line['Правильный ответ']:
                    correct_answer_count[line['Текущая отсрочка']] += 1

        right_answer_percentage = []
        for delay in delays:
            if total_answer_count[delay]:
                right_answer_percentage.append(correct_answer_count[delay] / total_answer_count[delay] * 100)
            else:
                right_answer_percentage.append(0)

        self.figure_subplot3.clear()
        self.figure_subplot3.plot(delays, right_answer_percentage)

        refusals_persentage = []
        for delay in delays:
            if total_presentation_count[delay]:
                refusals_persentage.append(refusals_count[delay] / total_presentation_count[delay] * 100)
            else:
                refusals_persentage.append(0)

        self.figure_subplot4.clear()
        self.figure_subplot4.plot(delays, refusals_persentage)

        self.graph_canvas1.draw()
        self.graph_canvas2.draw()
        self.graph_canvas3.draw()
        self.graph_canvas4.draw()

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

        while not self.window.log:
            sleep(1)

        experiment_type = self.window.experiment_type
        log_header = settings[f'current_log_header{experiment_type}']
        print(f'log_header: {log_header}')
        if log_header is None:
            log_header = ['Номер', 'Время с начала эксперимента', 'Время реакции', 'Ответ', 'Правильный ответ']

        self.log_label = [[tk.Label(self.frame_log_top, text='') for _ in range(len(log_header))] for _ in
                          range(11)]

        for i in range(len(self.log_label)):
            for j in range(len(self.log_label[i])):
                self.log_label[i][j].grid(row=i, column=j)

        for j, text in enumerate(log_header):
            self.log_label[0][j].configure(text=text)

        self.generate_canvases()

        while True:
            for i, line in enumerate(self.window.log[max(len(self.window.log) - 10, 0):]):
                if line['Ответ'] is None:
                    color = '#f0f'
                elif line['Ответ'] == line['Правильный ответ']:
                    color = '#0f0'
                else:
                    color = '#f00'

                for j, key in enumerate(log_header):
                    self.log_label[i + 1][j].configure(text=str(line[key]), fg=color)

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
        self.second_screen_copy = SecondScreenCopy(self.root, 1, 1)
