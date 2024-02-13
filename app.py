import tkinter as tk
from tkinter import ttk
from tkinter import *
from monkey_window import Monkey_window

import settings


class App(tk.Tk):
    def __init__(self):
        super().__init__()
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
        self.btn = tk.Button(self.frame[frame_number], text="Запустить тестирование", command=self.open_about)
        self.btn.pack(padx=50, pady=20)

    def open_about(self):
        if not self.started:
            self.btn.configure(text="Завершить тестирование")
            self.started = True
            self.window = Monkey_window()
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
