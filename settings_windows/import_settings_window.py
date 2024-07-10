import json
import tkinter as tk

import utils
from settings import settings


class ImportSettingsWindow(tk.Toplevel):
    def __init__(self, experiment_type, root):
        self.experiment_type = experiment_type
        self.root = root

        super().__init__()
        utils.move_to_first_screen(self)

        self.title('Импортировать настройки')
        self.geometry('300x100')

        self.label = tk.Label(self, text='Открыть файл настроек')
        self.label.pack()

        self.entry = tk.Entry(self)
        self.entry.pack()

        self.button = tk.Button(self, text='Открыть', command=self.read_file)
        self.button.pack()

        self.error_label = tk.Label(self, text='', fg='#f00')
        self.error_label.pack()

    def read_file(self):
        filename = self.entry.get()

        try:
            with open(filename, "r") as file:
                data = json.load(file)

            for i, widget in enumerate(self.root.widgets_list.widgets):
                widget.set_value(data[str(i)])
        except FileNotFoundError:
            self.error_label.configure(text=f'Файл {filename} не найден')
        except Exception as err:
            self.error_label.configure(text=f'Не удалось извлечь настройки из файла {filename}')
            print(err)
        else:
            settings['settings_file_name'][self.experiment_type] = filename
            self.destroy()
