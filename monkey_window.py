import tkinter as tk
import tkinter.messagebox as mb

from PIL.ImageTk import PhotoImage


class Monkey_window(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.attributes("-fullscreen", True)
        self.protocol("WM_DELETE_WINDOW", self.confirm_delete)
        self.label = tk.Label(self, text="Это окно для тестирования обезьяны")
        self.button = tk.Button(self, text="Закрыть", command=self.destroy)
        self.label.pack(padx=20, pady=20)
        self.button.pack(pady=5, ipadx=2, ipady=2)
        self.img = PhotoImage(file='settings2.png')
        tk.Label(self, image=self.img).pack()

    def confirm_delete(self):
        message = "Вы уверены, что хотите закрыть это окно?"
        if mb.askyesno(message=message, parent=self):
            self.destroy()