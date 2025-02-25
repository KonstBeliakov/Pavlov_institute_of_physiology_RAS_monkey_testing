from customtkinter import *

import utils
from settings_windows.export_settings_window import ExportSettingsWindow
from settings_windows.import_settings_window import ImportSettingsWindow


class SettingsWindow(CTkToplevel):
    def __init__(self, experiment_type=None):
        self.experiment_type = experiment_type
        self.widgets_list = None

        super().__init__()
        utils.move_to_first_screen(self)

        self.buttonFrame = CTkFrame(self)
        self.buttonFrame.grid(row=1, column=0)

        self.btn_confirm = CTkButton(self.buttonFrame, text='Применить', command=self.save_settings)
        self.btn_confirm.grid(row=0, column=0, padx=1, pady=5)
        self.btn_confirm = CTkButton(self.buttonFrame, text='Отмена', command=self.cansel)
        self.btn_confirm.grid(row=0, column=1, padx=1, pady=5)
        self.btn_import_settings = CTkButton(self.buttonFrame, text='Импортировать настройки',
                                             command=self.open_import_settings_window)
        self.btn_import_settings.grid(row=0, column=2, padx=1, pady=5)
        self.btn_export_settings = CTkButton(self.buttonFrame, text='Экспортировать настройки',
                                             command=self.open_export_settings_window)
        self.btn_export_settings.grid(row=0, column=3, padx=1, pady=5)

        self.errorFrame = CTkFrame(self)
        self.errorFrame.grid(row=2, column=0)

        self.error_label = CTkLabel(self.errorFrame, text='Ошибка!', text_color='#f00')

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
    window = CTk()
    settings_window = SettingsWindow()
    settings_window.mainloop()