import tkinter as tk
from tkinter import ttk

import settings
from settings_windows.settings_window import SettingsWindow


class ExperimentSettingsWindow3(SettingsWindow):
    def __init__(self):
        super().__init__(experiment_type=3)

        self.settingsFrame = tk.Frame(self)
        self.settingsFrame.grid(column=0, row=0)
        self.shuffle = 'Да'

        text = ['Время запоминания изображений', 'Задержка перед ответом', 'Время на ответ',
                'Задержка между экспериментами', 'Минимальное количество изображений',
                'Максимальное количество изображений', 'Перемешивать изображения']
        self.labels = [tk.Label(self.settingsFrame, text=t) for t in text]
        for i, label in enumerate(self.labels):
            label.grid(column=0, row=i)

        self.entries = [tk.Entry(self.settingsFrame) for _ in range(6)]
        for i, entry in enumerate(self.entries):
            entry.grid(column=1, row=i)

        self.btn_yes = ttk.Radiobutton(self.settingsFrame, text='Да', value='Да', variable=self.shuffle)
        self.btn_yes.grid(column=1, row=6)

        self.btn_no = ttk.Radiobutton(self.settingsFrame, text='Нет', value='Нет', variable=self.shuffle)
        self.btn_no.grid(column=2, row=6)

    def save_settings(self):
        pass


if __name__ == '__main__':
    window = ExperimentSettingsWindow3()
    window.mainloop()