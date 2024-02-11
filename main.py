import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
from tkinter import *


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.attributes("-fullscreen", True)
        self.protocol("WM_DELETE_WINDOW", self.confirm_delete)
        self.label = tk.Label(self, text="Это окно для тестирования обезьяны")
        self.button = tk.Button(self, text="Закрыть", command=self.destroy)
        self.label.pack(padx=20, pady=20)
        self.button.pack(pady=5, ipadx=2, ipady=2)

    def confirm_delete(self):
        message = "Вы уверены, что хотите закрыть это окно?"
        if mb.askyesno(message=message, parent=self):
            self.destroy()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        notebook = ttk.Notebook()
        notebook.pack(expand=True, fill=BOTH)
        frame_text = ['Информация', 'Настройки тестирования А', 'Настройки тестирования B', 'Настройки тестирования C']
        frame = [ttk.Frame(notebook) for _ in range(4)]

        for i in range(len(frame)):
            frame[i].pack(fill=BOTH, expand=True)

        test_image = PhotoImage(file="test.png")

        for i in range(len(frame)):
            notebook.add(frame[i], text=frame_text[i], image=test_image, compound=LEFT)

        self.label = tk.Label(frame[1], text='Это окно для настройки параметров тестирования')
        self.btn = tk.Button(frame[1], text="Запустить тестирование",
                             command=self.open_about)
        self.label.pack()
        self.btn.pack(padx=50, pady=20)

    def open_about(self):
        window = Window()
        window.grab_set()


if __name__ == "__main__":
    app = App()
    app.mainloop()
