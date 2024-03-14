import tkinter as tk
from tkinter import ttk

import settings
from settings_windows.settings_window import SettingsWindow
from utils import entry_value_check


class ExperimentSettingsWindow3(SettingsWindow):
    def __init__(self):
        super().__init__(experiment_type=3)

        self.settingsFrame = tk.Frame(self)
        self.settingsFrame.grid(column=0, row=0)
        self.shuffle = tk.StringVar(value='Да')
        self.stop_after_error = tk.StringVar(value='Да')

        self.label_text = ['Время запоминания изображений', 'Задержка перед ответом', 'Время на ответ',
                'Задержка между экспериментами', 'Минимальное количество изображений',
                'Максимальное количество изображений', 'Перемешивать изображения', 'Начинать заново после ошибки']
        self.labels = [tk.Label(self.settingsFrame, text=t) for t in self.label_text]
        for i, label in enumerate(self.labels):
            label.grid(column=0, row=i)

        self.entries = [tk.Entry(self.settingsFrame) for _ in range(6)]
        for i, entry in enumerate(self.entries):
            entry.grid(column=1, row=i)

        self.btn_yes = ttk.Radiobutton(self.settingsFrame, text='Да', value='Да', variable=self.shuffle)
        self.btn_yes.grid(column=1, row=6)
        self.btn_no = ttk.Radiobutton(self.settingsFrame, text='Нет', value='Нет', variable=self.shuffle)
        self.btn_no.grid(column=2, row=6)

        self.btn_yes2 = ttk.Radiobutton(self.settingsFrame, text='Да', value='Да', variable=self.stop_after_error)
        self.btn_yes2.grid(column=1, row=7)
        self.btn_no2 = ttk.Radiobutton(self.settingsFrame, text='Нет', value='Нет', variable=self.stop_after_error)
        self.btn_no2.grid(column=2, row=7)

    def save_settings(self):
        error_text = ''
        for i in range(4):
            if not error_text:
                error_text = entry_value_check(self.entries[i].get(), self.label_text[i], declension=1,
                                               min_value=0, value_type=float)
        for i in range(4, 6):
            if not error_text:
                error_text = entry_value_check(self.entries[i].get(), self.label_text[i], declension=1, min_value=1)
        if not error_text and int(self.entries[4].get()) > int(self.entries[5].get()):
            error_text = 'Минимальное количество изображений не может быть больше максимального количества изображений'

        if error_text:
            self.show_error(error_text)
        else:
            for i in range(4):
                settings.delay3[i] = float(self.entries[i].get())
            settings.min_image_number = int(self.entries[4].get())
            settings.max_image_number = int(self.entries[5].get())
            settings.shuffle_images = (self.shuffle == 'Да')
            settings.stop_after_error = (self.stop_after_error == 'Да')
            self.destroy()


if __name__ == '__main__':
    window = ExperimentSettingsWindow3()
    window.mainloop()