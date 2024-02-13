import tkinter as tk


class ExportSettingsWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.title('Экспортировать натройки')
        self.geometry('300x100')

        self.label = tk.Label(self, text='Сохранить файл настроек')
        self.label.pack()

        self.entry = tk.Entry(self)
        self.entry.pack()

        self.button = tk.Button(self, text='Сохранить', command=self.write_file)
        self.button.pack()

    def write_file(self):
        pass
