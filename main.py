import tkinter as tk
import tkinter.messagebox as mb


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
        self.label = tk.Label(self, text='Это окно для настройки параметров тестирования')
        self.btn = tk.Button(self, text="Запустить тестирование",
                             command=self.open_about)
        self.label.pack()
        self.btn.pack(padx=50, pady=20)

    def open_about(self):
        window = Window()
        window.grab_set()


if __name__ == "__main__":
    app = App()
    app.mainloop()
