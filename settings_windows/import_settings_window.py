import json
from customtkinter import *

import utils
from settings import settings


class ImportSettingsWindow(CTkToplevel):
    def __init__(self, experiment_type, root):
        self.experiment_type = experiment_type
        self.root = root

        super().__init__()
        utils.move_to_first_screen(self)

        self.title('Импортировать настройки')
        self.geometry('300x100')

        self.label = CTkLabel(self, text='Открыть файл настроек')
        self.label.pack()

        self.entry = CTkEntry(self)
        self.entry.pack()

        self.button = CTkButton(self, text='Открыть', command=self.read_file)
        self.button.pack()

        self.error_label = CTkLabel(self, text='', fg='#f00')
        self.error_label.pack()

    def read_file(self):
        filename = self.entry.get()

        try:
            with open(filename, "r") as file:
                data = json.load(file)

            for widget in self.root.widgets_list.widgets:
                widget.set_value(data[widget.text])

            if self.root.experiment_type == 1:
                for widget in self.root.delay_widget_list:
                    widget.set_value(data[widget.text])

        except FileNotFoundError:
            self.error_label.configure(text=f'Файл {filename} не найден')
        except Exception as err:
            self.error_label.configure(text=f'Не удалось извлечь настройки из файла {filename}')
            print(err)
        else:
            settings['settings_file_name'][self.experiment_type] = filename
            self.destroy()
