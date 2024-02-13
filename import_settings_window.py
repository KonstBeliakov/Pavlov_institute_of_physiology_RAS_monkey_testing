import tkinter as tk


class ImportSettingsWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.title('Импортировать настройки')
        self.geometry('300x100')

        self.label = tk.Label(self, text='Открыть файл настроек')
        self.label.pack()

        self.entry = tk.Entry(self)
        self.entry.pack()

        self.button = tk.Button(self, text='Открыть', command=self.read_file)
        self.button.pack()

    def read_file(self):
        pass
