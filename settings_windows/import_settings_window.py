import json
import tkinter as tk

import settings


class ImportSettingsWindow(tk.Toplevel):
    def __init__(self, experiment_type):
        self.experiment_type = experiment_type

        super().__init__()

        self.title('Импортировать настройки')
        self.geometry('300x100')
        self.geometry(f'+{-1000}+{50}')

        self.label = tk.Label(self, text='Открыть файл настроек')
        self.label.pack()

        self.entry = tk.Entry(self)
        self.entry.pack()

        self.button = tk.Button(self, text='Открыть', command=self.read_file)
        self.button.pack()

        self.error_label = tk.Label(self, text='Не удалось открыть файл. Убедитесь что он существует', fg='#f00')

    def read_file(self):
        try:
            with open(self.entry.get(), "r") as file:
                data = json.load(file)
                settings.delay = data['delay']
                settings.restart_after_answer = data['restart_after_answer']
                settings.repeat_number = data['repeat_number']
                settings.session_number = data['session_number']
                settings.experiment_start = data['experiment_start']
        except:
            self.error_label.pack()
        else:
            self.destroy()
