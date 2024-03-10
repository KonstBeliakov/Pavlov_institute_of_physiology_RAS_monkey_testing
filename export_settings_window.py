import tkinter as tk
import json

import settings


class ExportSettingsWindow(tk.Toplevel):
    def __init__(self, experiment_type):
        self.experiment_type = experiment_type

        super().__init__()

        self.title('Экспортировать натройки')
        self.geometry('300x100')

        self.label = tk.Label(self, text='Сохранить файл настроек')
        self.label.pack()

        self.entry = tk.Entry(self)
        self.entry.pack()

        self.button = tk.Button(self, text='Сохранить', command=self.write_file)
        self.button.pack()

        self.error_label = tk.Label(self, text='Не удалось сохранить настройки, попробуйте еще раз', fg='#f00')

    def write_file(self):
        try:
            data = {'delay': settings.delay, 'session_number': settings.session_number,
                    'repeat_number': settings.repeat_number, 'experiment_start': settings.experiment_start,
                    'restart_after_answer': settings.restart_after_answer}
            with open(self.entry.get(), 'w') as file:
                json.dump(data, file)
        except:
            self.error_label.pack()
        else:
            self.destroy()
