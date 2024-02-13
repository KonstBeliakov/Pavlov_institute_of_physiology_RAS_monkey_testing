import time
import tkinter as tk
from tkinter import ttk
from tkinter import *
from monkey_window import Monkey_window
import threading

import settings


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.timer_ask_label = None
        self.choose_experiment_label = None
        self.choose_experiment_combobox = None
        self.radio_button_no = None
        self.radio_button_yes = None
        self.timer_radio_buttons = None
        self.update_thread = None
        self.log_label = []
        self.btn_confirm = None
        self.error_label = None
        self.t = None
        self.delay_label = None
        self.delay_entry = [Entry(), Entry(), Entry()]
        self.label = None
        self.btn = None
        self.window = None
        self.started = False
        notebook = ttk.Notebook()
        notebook.pack(expand=True, fill=BOTH)
        frame_text = ['Общие настройки', 'Запуск эксперимента', 'Информация о приложении']
        self.frame = [ttk.Frame(notebook) for _ in range(3)]

        for i in range(len(self.frame)):
            self.frame[i].pack(fill=BOTH, expand=True)

        self.test_image = [PhotoImage(file="settings.png"), PhotoImage(file="run.png"), PhotoImage(file="info.png")]

        for i in range(len(self.frame)):
            notebook.add(self.frame[i], text=frame_text[i], image=self.test_image[i], compound=LEFT)

        self.info_frame_init()
        self.settings_frame_init()
        self.run_frame_init()

        self.label.pack()

    def info_frame_init(self):
        frame_number = 2
        self.label = Label(self.frame[frame_number],
                           text="Настроить параметры запуска можно в одной из вкладок настроек, после чего "
                                "тестирование запускается кнопкой во вкладке \"Запуск эксперимента\"\nДанные полученные в "
                                "результате тестирования будут записаны в текстовый файл data.txt")

    def settings_frame_init(self):
        frame_number = 0
        delay_text = ['Время отображения целевого изображения', 'Задержка перед появлением тестовых изображений',
                      'Время для ответа (выбора одного из тестовых изображений)', 'Задержка между тестами']

        self.delay_label = [Label(self.frame[frame_number], text=i) for i in delay_text]
        self.t = [IntVar() for i in range(4)]
        for i in range(4):
            self.t[i].set(settings.delay[i])
        self.delay_entry = [Entry(self.frame[frame_number], text=self.t[i]) for i in range(4)]

        for i in range(4):
            self.delay_label[i].grid(row=i, column=0)
            self.delay_entry[i].grid(row=i, column=1)

        self.btn_confirm = tk.Button(self.frame[frame_number], text='Сохранить настройки', command=self.save_settings)
        self.btn_confirm.grid(row=4, column=0)
        self.error_label = Label(self.frame[frame_number], text='Должно быть введено вещественное число')

    def run_frame_init(self):
        frame_number = 1
        self.choose_experiment_label = Label(self.frame[frame_number], text='Выберите тип эксперимента из списка доступных')
        self.choose_experiment_label.grid(row=0, column=0)

        self.choose_experiment_combobox = ttk.Combobox(self.frame[frame_number], values=['Запоминание картинки'])
        self.choose_experiment_combobox.grid(row=1, column=0)

        self.timer_ask_label = Label(self.frame[frame_number], text='Обнулить глобальный таймер эксперимента?')
        self.timer_ask_label.grid(row=2, column=0)

        self.timer_radio_buttons = IntVar()
        self.timer_radio_buttons.set(0)
        self.radio_button_yes = Radiobutton(self.frame[frame_number], text="Да", variable=self.timer_radio_buttons, value=1)
        self.radio_button_no = Radiobutton(self.frame[frame_number], text="Нет", variable=self.timer_radio_buttons, value=0)
        self.radio_button_yes.grid(row=3, column=0)
        self.radio_button_no.grid(row=3, column=1)

        self.btn = tk.Button(self.frame[frame_number], text="Запустить тестирование", command=self.open_about)
        self.btn.grid(row=4, column=0)

    def open_about(self):
        if not self.started:
            self.btn.configure(text="Завершить тестирование")
            self.started = True
            self.window = Monkey_window()

            self.update_thread = threading.Thread(target=self.update_log)
            self.update_thread.start()

            self.window.mainloop()
        else:
            self.window.destroy()
            self.btn.configure(text="Запустить тестирование")
            self.started = False

    def save_settings(self):
        try:
            settings.delay = [float(i.get()) for i in self.delay_entry]
            print(settings.delay)
        except:
            self.error_label.grid(row=4, column=1)
        else:
            self.error_label.grid_forget()

    def update_log(self):
        while True:
            print('updating log...', end='')
            self.log_label = [[tk.Label(self.frame[1], text=text, fg='#0f0' if line[-1] == line[-2] else '#f00')
                               for text in line] for line in self.window.log[-10:]]
            for i in range(len(self.log_label)):
                for j in range(len(self.log_label[i])):
                    self.log_label[i][j].grid(row=i, column=1 + j)
            print('done')
            time.sleep(1)
