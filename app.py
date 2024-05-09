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
import settings
import utils
from try_again_window import TryAgainWindow

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

        self.started = False
        self.log_label = []
        self.delay_entry = [Entry(), Entry(), Entry()]

        self.protocol("WM_DELETE_WINDOW", self.confirm_delete)

        notebook = ttk.Notebook()
        notebook.pack(expand=True, fill=BOTH)
        frame_text = ['Общие настройки', 'Запуск эксперимента', 'Информация о приложении']
        self.frame = [ttk.Frame(notebook) for _ in range(len(frame_text))]

        for i in range(len(self.frame)):
            self.frame[i].pack(fill=BOTH, expand=True)

        self.test_image = [PhotoImage(file="settings.png"), PhotoImage(file="run.png"), PhotoImage(file="info.png")]

        for i in range(len(self.frame)):
            notebook.add(self.frame[i], text=frame_text[i], image=self.test_image[i], compound=LEFT)

        self.info_frame_init()
        self.settings_frame_init()
        self.run_frame_init()

    def confirm_delete(self):
        message = "Вы уверены, что хотите закрыть это окно?"
        if mb.askyesno(message=message, parent=self):
            self.destroy()

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


        self.basic_settings_labels = ['Путь до файла звука воспроизводящегося в начале эксперимента',
                                      'Путь до файла позитивного звукового подкрепления',
                                      'Путь до файла негативного звукового подкрепления',
                                      '', 'Радиус круга отображающегося после нажатия', 'Цвет круга',
                                      'Толщина линии круга', 'Время отображения круга', '',
                                      'Размер копии второго монитора', 'Цвет фона экспериментального окна']
        self.settings_frame_labels = [Label(self.basic_settings_label_frame, text=t) for t in self.basic_settings_labels]
        for i, label in enumerate(self.settings_frame_labels):
            label.grid(row=i, column=0)


        self.sound_entry = [Entry(self.basic_settings_label_frame) for _ in range(3)]
        self.sound_entry[0].insert(0, settings.experiment_start_sound)
        self.sound_entry[1].insert(0, settings.right_answer_sound)
        self.sound_entry[2].insert(0, settings.wrong_answer_sound)
        for i in range(3):
            self.sound_entry[i].grid(row=i, column=1)


        self.click_settings_entry = [Entry(self.basic_settings_label_frame) for _ in range(4)]
        for i, value in  enumerate([settings.mouse_click_circle_radius, settings.click_circle_color,
                                    settings.click_circle_width, settings.click_circle_time]):
            self.click_settings_entry[i].insert(0, value)
            self.click_settings_entry[i].grid(row=i + 4, column=1)

        self.monitor_copy_size_entry = Entry(self.basic_settings_label_frame)
        self.monitor_copy_size_entry.insert(0, str(settings.monitor_copy_size))
        self.monitor_copy_size_entry.grid(row=9, column=1)

        self.bg_color_entry = Entry(self.basic_settings_label_frame)
        self.bg_color_entry.insert(0, str(settings.bg_color))
        self.bg_color_entry.grid(row=10, column=1)

        self.button_apply = Button(self.frame[frame_number], text='Применить', command=self.apply_basic_settings)
        self.button_apply.grid(row=2, column=0)

        self.error_label = tk.Label(self.frame[frame_number], text='Настройки не применены', fg='#f00')
        self.error_label.grid(row=3, column=0)

    def apply_basic_settings(self):
        error_text = utils.entry_value_check(self.click_settings_entry[0].get(),
                                             self.basic_settings_labels[4], declension=0, min_value=0)
        if not error_text:
            error_text = utils.entry_value_check(self.click_settings_entry[2].get(),
                                                 self.basic_settings_labels[6], declension=2, min_value=0)
        if not error_text:
            error_text = utils.entry_value_check(self.click_settings_entry[3].get(), self.basic_settings_labels[7],
                                                 declension=1, min_value=0, value_type=float)
        if not error_text:
            error_text = utils.entry_value_check(self.monitor_copy_size_entry.get(), self.basic_settings_labels[9],
                                                 declension=0, min_value=0, value_type=float)

        if error_text:
            self.show_error(error_text)
        else:
            self.show_error('')
            settings.using_sound = (self.sounds_in_experiments.get() == 'Да')

            settings.experiment_start_sound = self.sound_entry[0].get()
            settings.right_answer_sound = self.sound_entry[1].get()
            settings.wrong_answer_sound = self.sound_entry[2].get()

            settings.mouse_click_circle_radius = float(self.click_settings_entry[0].get())
            settings.click_circle_color = self.click_settings_entry[1].get()
            settings.click_circle_width = float(self.click_settings_entry[2].get())
            settings.click_circle_time = float(self.click_settings_entry[3].get())
            settings.monitor_copy_size = float(self.monitor_copy_size_entry.get())
            settings.bg_color = self.bg_color_entry.get()

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

        self.second_screen_canvas = Canvas(self.frame[frame_number])
        self.second_screen_canvas.grid(row=0, column=2)

        self.figure = plt.Figure(figsize=(5, 5))  # , facecolor='yellow')
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
            if self.timer_radio_buttons or not settings.experiment_start:
                settings.experiment_start = time.perf_counter()
            self.btn.configure(text="Завершить тестирование")
            self.started = True
            match self.choose_experiment_combobox.get():
                case 'Запоминание картинки':
                    self.window = MonkeyWindow1()
                case 'Экстраполяция движения':
                    self.window = MonkeyWindow2()
                case 'Новая картинка':
                    self.window = MonkeyWindow3()
            if self.choose_experiment_combobox.get():
                utils.experiment_start()

            self.update_thread = threading.Thread(target=self.update_log)
            self.update_thread.start()
            self.update_second_screen_thread = threading.Thread(target=self.second_screen_update)
            self.update_second_screen_thread.start()

            self.window.mainloop()
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

    def second_screen_update(self):
        python_image = tk.PhotoImage(file="settings.png")
        monitor_number = 2
        with mss.mss() as sct:
            mon = sct.monitors[monitor_number]
            self.canvas_image = self.second_screen_canvas.create_image(int(mon['width'] * settings.monitor_copy_size),
                                                                       int(mon['height'] * settings.monitor_copy_size),
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
                img2 = img.resize((int(img.size[0] * 2 * settings.monitor_copy_size),
                                   int(img.size[1] * 2 * settings.monitor_copy_size)))
                img3 = ImageTk.PhotoImage(img2)

                self.second_screen_canvas.itemconfigure(self.canvas_image, image=img3)

    def experiment_settings(self):
        match self.choose_experiment_combobox.get():
            case 'Запоминание картинки':
                self.experiment_settings_window = ExperimentSettingsWindow()
            case 'Экстраполяция движения':
                self.experiment_settings_window = ExperimentSettingsWindow2()
            case 'Новая картинка':
                self.experiment_settings_window = ExperimentSettingsWindow3()
        self.experiment_settings_window.mainloop()

    def save_experiment_data(self, path):
        df = pd.DataFrame(
            {name: [str(line[i]) for line in self.window.log[1:]] for i, name in enumerate(self.window.log[0])})
        df.to_excel(path)


if __name__ == '__main__':
    print('start...')
    app = App()
    app.mainloop()
