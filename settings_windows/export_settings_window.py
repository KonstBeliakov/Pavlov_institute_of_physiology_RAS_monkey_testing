import tkinter as tk
import json

import utils
from settings import settings


class ExportSettingsWindow(tk.Toplevel):
    def __init__(self, experiment_type, root):
        self.experiment_type = experiment_type
        self.root = root

        super().__init__()
        utils.move_to_first_screen(self)

        self.title('Экспортировать натройки')
        self.geometry('300x100')

        self.label = tk.Label(self, text='Сохранить файл настроек')
        self.label.pack()

        self.entry = tk.Entry(self)
        self.entry.pack()

        self.button = tk.Button(self, text='Сохранить', command=self.write_file)
        self.button.pack()

        self.error_label = tk.Label(self, text='', fg='#f00')
        self.error_label.pack()

    def write_file(self):
        filename = self.entry.get()

        try:
            data = {}
            for i, widget in enumerate(self.root.widgets_list.widgets):
                data[i] = widget.get()

            with open(filename, 'w') as file:
                json.dump(data, file)
        except Exception as err:
            self.error_label.configure(text=f'Не удалось записать файл {filename}')
            print(err)
        else:
            settings['settings_file_name'][self.experiment_type] = filename
            self.destroy()
