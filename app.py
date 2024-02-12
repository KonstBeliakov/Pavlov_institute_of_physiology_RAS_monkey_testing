import tkinter as tk
from tkinter import ttk
from tkinter import *
from monkey_window import Monkey_window


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.window = None
        self.started = False
        notebook = ttk.Notebook()
        notebook.pack(expand=True, fill=BOTH)
        frame_text = ['Информация о приложении', 'Настройки тестирования А', 'Настройки тестирования B',
                      'Настройки тестирования C', 'Запуск']
        frame = [ttk.Frame(notebook) for _ in range(5)]

        for i in range(len(frame)):
            frame[i].pack(fill=BOTH, expand=True)

        self.test_image = [PhotoImage(file="info.png"), PhotoImage(file="settings.png"),
                           PhotoImage(file="settings.png"), PhotoImage(file="settings.png"),
                           PhotoImage(file="run.png")]

        for i in range(len(frame)):
            notebook.add(frame[i], text=frame_text[i], image=self.test_image[i], compound=LEFT)

        self.btn = tk.Button(frame[-1], text="Запустить тестирование", command=self.open_about)
        self.btn.pack(padx=50, pady=20)

    def open_about(self):
        if not self.started:
            self.btn.configure(text="Завершить тестирование")
            self.started = True
            self.window = Monkey_window()
            self.window.mainloop()
        else:
            self.btn.configure(text="Запустить тестирование")
            self.started = False
