import datetime
import os
import time
import tkinter as tk
from tkinter import ttk
import mss
import mss.tools

from tkinter import *
import threading
import tkinter.messagebox as mb
import pandas as pd

from PIL import Image
from PIL import ImageTk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkhtmlview import HTMLLabel

from widgets.widget_list import WidgetList
from settings import settings
import utils
from try_again_window import TryAgainWindow

from widgets.improved_entry import ImprovedEntry
from widgets.improved_radiobuttons import ImprovedRadiobuttons

from settings_windows.experiment_settings_window2 import ExperimentSettingsWindow2
from settings_windows.experiment_settings_window import ExperimentSettingsWindow
from settings_windows.experiment_settings_window3 import ExperimentSettingsWindow3

from monkey_windows.monkey_window1 import MonkeyWindow1
from monkey_windows.monkey_window2 import MonkeyWindow2
from monkey_windows.monkey_window3 import MonkeyWindow3


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Основное окно')
        self.geometry(f'+{-1000}+{50}')

        self.started = False
        self.log_label = []
        self.delay_entry = [Entry(), Entry(), Entry()]

        self.protocol("WM_DELETE_WINDOW", self.confirm_delete)

        self.notebook = ttk.Notebook()
        self.notebook.pack(expand=True, fill=BOTH)
        frame_text = ['Общие настройки', 'Запуск эксперимента', 'Информация о приложении', 'Проверка устройств',
                      'Анализ данных']
        self.frame = [ttk.Frame(self.notebook) for _ in range(len(frame_text))]

        for i in range(len(self.frame)):
            self.frame[i].pack(fill=BOTH, expand=True)

        self.test_image = [PhotoImage(file="pictograms/settings.png"), PhotoImage(file="pictograms/run.png"),
                           PhotoImage(file="pictograms/info.png"),
                           PhotoImage(file='pictograms/yes.png') if utils.serial_available else PhotoImage(file="pictograms/no.png"),
                           PhotoImage(file="pictograms/data.png")]

        for i in range(len(self.frame)):
            self.notebook.add(self.frame[i], text=frame_text[i], image=self.test_image[i], compound=LEFT)

        self.info_frame_init()
        self.settings_frame_init()
        self.run_frame_init()
        self.devise_check_frame_init()
        self.data_frame_init()

    def confirm_delete(self):
        message = "Вы уверены, что хотите закрыть это окно?"
        if mb.askyesno(message=message, parent=self):
            self.destroy()

    def load_data(self):
        experiment_type = ['Запоминание картинки', 'Экстраполяция движения', 'Новая картинка'].index(self.experiment_type_radiobutton.get()) + 1
        files = []
        for file in sorted(os.listdir('data/')):
            t1 = (not settings['selected_period_start'] or str(settings['selected_period_start']) < file)
            t2 = (not settings['selected_period_end'] or file < str(settings['selected_period_end']))
            t3 = int(file.split('.')[0][-1]) == experiment_type
            if t1 and t2 and t3:
                files.append(file)

        return files

    def find_experiments(self):
        if (error_text := self.time_interval_entries.check_values(show_error=True)) is not None:
            self.data_frame_error_label.configure(text=error_text)
        else:
            if self.time_interval_entries.widgets[0].get():
                self.time_interval_entries.widgets[0].save_value()
            else:
                settings['selected_period_start'] = ''

            if self.time_interval_entries.widgets[1].get():
                self.time_interval_entries.widgets[1].save_value()
            else:
                settings['selected_period_end'] = ''

            self.experiment_type_radiobutton.save_value()

            self.experiment_data.config(state=NORMAL)
            self.experiment_data.delete(1.0, tk.END)
            self.experiment_data.insert(tk.END, '\n'.join(self.load_data()))
            self.experiment_data.config(state=DISABLED)

    def create_data_file(self):
        pass

    def data_frame_init(self):
        frame_number = 4

        self.data_frame0 = Frame(self.frame[frame_number])
        self.data_frame0.grid(row=0, column=0)

        self.experiment_type_radiobutton = ImprovedRadiobuttons(self.data_frame0, 0, 0, text='Тип эксперимента',
                                                                values=['Запоминание картинки', 'Экстраполяция движения', 'Новая картинка'],
                                                                value_type=str)

        self.data_frame1 = Frame(self.frame[frame_number])
        self.data_frame1.grid(row=1, column=0)

        self.time_interval_entries = WidgetList(self.data_frame1, 0, 1, [
            {'text': 'От', 'value_type': 'date', 'save_value': 'selected_period_start', 'may_be_empty': True},
            {'text': 'До', 'value_type': 'date', 'save_value': 'selected_period_end',   'may_be_empty': True}
        ], vertical=True)

        self.button_search = Button(self.data_frame1, text='Найти эксперименты', command=self.find_experiments)
        self.button_search.grid(row=1, column=1)

        self.data_frame_error_label = Label(self.data_frame1, text='', fg='red')
        self.data_frame_error_label.grid(row=2, column=0)

        self.data_frame2 = Frame(self.frame[frame_number])
        self.data_frame2.grid(row=2, column=0)

        self.experiment_data = tk.Text(self.data_frame2, height=8, width=40)

        t = ' '

        self.experiment_data.insert(tk.END, t)
        self.experiment_data.config(state=DISABLED)
        self.scroll = tk.Scrollbar(self.data_frame2)
        self.experiment_data.configure(yscrollcommand=self.scroll.set)
        self.experiment_data.pack(side=tk.LEFT)

        self.scroll.config(command=self.experiment_data.yview)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.data_frame3 = Frame(self.frame[frame_number])
        self.data_frame3.grid(row=3, column=0)

        self.filename_entry = ImprovedEntry(self.data_frame3, 0, 0, 'Название файла', value_type=str,
                                            save_value='experiment_data_filename')

        self.button_create_file = Button(self.data_frame3, text='Создать файл', command=self.create_data_file)
        self.button_create_file.grid(row=0, column=2)

    def devise_check(self):
        if (error_text := self.devise_check_entries.save_values(check_validity=True)) is not None:
            self.devise_check_error_label.configure(text=error_text)
        else:
            self.devise_check_error_label.configure(text='')
            utils.check_serial()

            if utils.serial_available:
                self.test_image[3].configure(file='pictograms/yes.png')
            else:
                self.test_image[3].configure(file='pictograms/no.png')

    def devise_check_frame_init(self):
        frame_number = 3

        self.devise_check_entries = WidgetList(self.frame[frame_number], 0, 0, [
            {'text': 'Порт', 'value_type': str, 'save_value': 'port'},
            {'text': 'Частота', 'value_type': int, 'min_value': 0, 'save_value': 'baudrate'}
        ])

        self.check_devise_button = Button(self.frame[frame_number], text='Подключиться к управляющей плате', command=self.devise_check)
        self.check_devise_button.grid(row=1, column=0)

        self.check_second_screen_button = Button(self.frame[frame_number], text='Проверить второй монитор', command=self.check_second_screen)
        self.check_second_screen_button.grid(row=2, column=0)

        self.devise_check_error_label = Label(self.frame[frame_number], text='', fg='red')
        self.devise_check_error_label.grid(row=3, column=0)

    def check_second_screen(self):
        self.check_second_screen_canvas = Canvas(self.frame[3])
        self.check_second_screen_canvas.grid(row=4, column=0)
        t1 = threading.Thread(target=lambda: self.second_screen_update(self.check_second_screen_canvas))
        t1.start()

    def info_frame_init(self):
        frame_number = 2
        with open('info_frame_text.html', 'r', encoding='utf-8') as file:
            self.info_label = HTMLLabel(self.frame[frame_number], html=file.read())
        self.info_label.pack(fill="both", expand=True)

    def settings_frame_init(self):
        frame_number = 0
        self.basic_settings_radio_button_frame = Frame(self.frame[frame_number])
        self.basic_settings_radio_button_frame.grid(column=0, row=0)

        self.sounds_in_experiments_label = Label(self.basic_settings_radio_button_frame,
                                                 text='Использовать звуковое подкрепление')
        self.sounds_in_experiments_label.grid(column=0, row=0)
        self.sounds_in_experiments = tk.StringVar(value='Да')
        self.sound_btn_yes = ttk.Radiobutton(self.basic_settings_radio_button_frame, text='Да', value='Да',
                                             variable=self.sounds_in_experiments)
        self.sound_btn_yes.grid(column=1, row=0)
        self.btn_no = ttk.Radiobutton(self.basic_settings_radio_button_frame, text='Нет', value='Нет',
                                      variable=self.sounds_in_experiments)
        self.btn_no.grid(column=2, row=0)

        self.basic_settings_label_frame = Frame(self.frame[frame_number])
        self.basic_settings_label_frame.grid(column=0, row=1)

        self.entries_list = WidgetList(self.basic_settings_label_frame, 0, 0, [
            {'text': 'Путь до файла звука начала эксперимента (оставить пустым если не используется)',          'value_type': str, 'save_value': 'experiment_start_sound', 'may_be_empty': True},
            {'text': 'Путь до файла позитивного звукового подкрепления (оставить пустым если не используется)', 'value_type': str, 'save_value': 'right_answer_sound', 'may_be_empty': True},
            {'text': 'Путь до файла негативного звукового подкрепления (оставить пустым если не используется)', 'value_type': str, 'save_value': 'wrong_answer_sound', 'may_be_empty': True},
            {'text': 'Радиус круга отображающегося после нажатия',       'value_type': int,   'min_value': 0, 'save_value': 'mouse_click_circle_radius'},
            {'text': 'Цвет круга',                                       'value_type': str, 'save_value': 'click_circle_color'},
            {'text': 'Толщина линии круга',                              'value_type': int,   'min_value': 0, 'save_value': 'click_circle_width'},
            {'text': 'Время отображения круга',                          'value_type': float, 'min_value': 0, 'save_value': 'click_circle_time'},
            {'text': 'Размер копии второго монитора',                    'value_type': float, 'min_value': 0, 'max_value': 0.5, 'save_value': 'monitor_copy_size'},
            {'text': 'Цвет фона экспериментального окна',                'value_type': str, 'save_value': 'bg_color'}
        ])

        self.button_apply = Button(self.frame[frame_number], text='Применить', command=self.apply_basic_settings)
        self.button_apply.grid(row=2, column=0)

        self.error_label = tk.Label(self.frame[frame_number], text='Настройки не применены', fg='#f00')
        self.error_label.grid(row=3, column=0)

    def apply_basic_settings(self):
        if (error_text := self.entries_list.save_values(check_validity=True)) is None:
            settings['using_sound'] = (self.sounds_in_experiments.get() == 'Да')
            self.show_error('')
        else:
            self.show_error(error_text)

    def show_error(self, text):
        self.error_label.configure(text=text)

    def run_frame_init(self):
        frame_number = 1

        self.run_frame_top = LabelFrame(self.frame[frame_number], text='Настройки запуска')
        self.run_frame_top.grid(row=0, column=0)
        self.run_frame = Frame(self.run_frame_top)
        self.run_frame.pack()

        self.choose_experiment_label = Label(self.run_frame, text='Тип эксперимента')
        self.choose_experiment_label.grid(row=0, column=0)

        self.choose_experiment_combobox = ttk.Combobox(self.run_frame, values=['Запоминание картинки',
                                                                               'Экстраполяция движения',
                                                                               'Новая картинка'])
        self.choose_experiment_combobox.grid(row=1, column=0)

        self.btn_settings = tk.Button(self.run_frame, text='Настроить эксперимент', command=self.experiment_settings)
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

        self.second_screen_canvas = Canvas(self.frame[frame_number])
        self.second_screen_canvas.grid(row=0, column=2)

        self.figure = plt.Figure(figsize=(5, 5))
        self.graph_canvas = FigureCanvasTkAgg(self.figure, self.frame[frame_number])
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
                    settings['experiment_start'] = time.perf_counter()

                self.btn.configure(text="Завершить тестирование")
                self.started = True

                utils.experiment_start()

                self.update_thread = threading.Thread(target=self.update_log)
                self.update_thread.start()
                self.update_second_screen_thread = threading.Thread(target=lambda: self.second_screen_update(self.second_screen_canvas))
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
        self.frame_log_top = LabelFrame(self.frame[1], text='Результаты последних 10 тестов')
        self.frame_log_top.grid(row=0, column=1)

        self.log_label = [[tk.Label(self.frame_log_top, text='') for _ in range(len(self.window.log[0]))] for _ in
                          range(11)]

        for i in range(len(self.log_label)):
            for j in range(len(self.log_label[i])):
                self.log_label[i][j].grid(row=i, column=j)

        for j, text in enumerate(self.window.log[0]):
            self.log_label[0][j].configure(text=text)
        time.sleep(1)
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
            time.sleep(1)

    def second_screen_update(self, canvas):
        python_image = tk.PhotoImage(file="pictograms/settings.png")
        monitor_number = 2
        with mss.mss() as sct:
            mon = sct.monitors[monitor_number]
            self.canvas_image = canvas.create_image(int(mon['width'] * settings['monitor_copy_size']),
                                                                       int(mon['height'] * settings['monitor_copy_size']),
                                                                       image=python_image)
            monitor = {
                "top": mon["top"],
                "left": mon["left"],
                "width": mon["width"],
                "height": mon["height"],
                "mon": monitor_number,
            }
        while True:
            with mss.mss() as sct:
                sct_img = sct.grab(monitor)
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                img2 = img.resize((int(img.size[0] * 2 * settings['monitor_copy_size']),
                                   int(img.size[1] * 2 * settings['monitor_copy_size'])))
                img3 = ImageTk.PhotoImage(img2)

                canvas.itemconfigure(self.canvas_image, image=img3)

    def experiment_settings(self):
        match self.choose_experiment_combobox.get():
            case 'Запоминание картинки':
                self.experiment_settings_window = ExperimentSettingsWindow()
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


if __name__ == '__main__':
    print('start...')
    app = App()
    app.mainloop()
