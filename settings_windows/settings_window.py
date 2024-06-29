import tkinter as tk
from tkinter import *

from settings_windows.export_settings_window import ExportSettingsWindow
from settings_windows.import_settings_window import ImportSettingsWindow


class SettingsWindow(Toplevel):
    def __init__(self, experiment_type=None):
        self.experiment_type = experiment_type
        self.widgets_list = None

        super().__init__()

        self.geometry(f'+{-1000}+{50}')

        self.buttonFrame = tk.Frame(self)
        self.buttonFrame.grid(row=1, column=0)

        self.btn_confirm = tk.Button(self.buttonFrame, text='Применить', command=self.save_settings)
        self.btn_confirm.grid(row=0, column=0)
        self.btn_confirm = tk.Button(self.buttonFrame, text='Отмена', command=self.cansel)
        self.btn_confirm.grid(row=0, column=1)
        self.btn_import_settings = tk.Button(self.buttonFrame, text='Импортировать настройки',
                                             command=self.open_import_settings_window)
        self.btn_import_settings.grid(row=0, column=2)
        self.btn_export_settings = tk.Button(self.buttonFrame, text='Экспортировать настройки',
                                             command=self.open_export_settings_window)
        self.errorFrame = Frame(self)
        self.errorFrame.grid(row=2, column=0)

        self.btn_export_settings.grid(row=0, column=3)
        self.error_label = tk.Label(self.errorFrame, text='Ошибка!', fg='#f00')

    def save_settings(self):
        pass

    def cansel(self):
        self.destroy()

    def open_export_settings_window(self):
        self.export_settings_window = ExportSettingsWindow(self.experiment_type, self)
        self.export_settings_window.mainloop()

    def open_import_settings_window(self):
        self.import_settings_window = ImportSettingsWindow(self.experiment_type, self)
        self.import_settings_window.mainloop()

    def show_error(self, error_text):
        self.error_label.configure(text=error_text)
        self.error_label.pack()


if __name__ == '__main__':
    window = Tk()
    settings_window = SettingsWindow()
    settings_window.mainloop()