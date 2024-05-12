import tkinter as tk

import settings
import utils
from settings_windows.settings_window import SettingsWindow
from improved_entry import ImprovedEntry


class ExperimentSettingsWindow(SettingsWindow):
    def __init__(self):
        super().__init__(experiment_type=1)
        self.title('Настройки эксперимента')
        self.export_settings_window = None
        self.import_settings_window = None

        self.settingsFrame = tk.Frame(self)
        self.settingsFrame.grid(row=0, column=0)

        self.entries = [
            ImprovedEntry(self.settingsFrame, 0, 0, 'Количество сессий',                              str(settings.session_number),       value_type=int,     min_value=1),
            ImprovedEntry(self.settingsFrame, 0, 1, 'Количество тестов в сессии',                     str(settings.repeat_number),        value_type=int,     min_value=1),
            ImprovedEntry(self.settingsFrame, 0, 2, 'Время отображения целевого изображения',         str(settings.delay[0]),             value_type=float,   min_value=0),
            ImprovedEntry(self.settingsFrame, 0, 3, 'Задержка перед появлением тестовых изображений', str(settings.delay[1]),             value_type=float,   min_value=0),
            ImprovedEntry(self.settingsFrame, 0, 4, 'Время для ответа',                               str(settings.delay[2]),             value_type=float,   min_value=0),
            ImprovedEntry(self.settingsFrame, 0, 5, 'Задержка между тестами',                         str(settings.delay[3]),             value_type=float,   min_value=0),
            ImprovedEntry(self.settingsFrame, 0, 6, 'Задержка между сессиями',                        str(settings.delay[4]),             value_type=float,   min_value=0),
            ImprovedEntry(self.settingsFrame, 0, 7, 'Размер изображения',                             str(settings.image_size),           value_type=int,     min_value=1),
            ImprovedEntry(self.settingsFrame, 0, 8, 'Расстояние между изображениями',                 str(settings.distance_between_images), value_type=int,  min_value=1)
        ]

        self.restart_radiobuttons = tk.IntVar()
        self.restart_radiobuttons.set(0)
        self.radio_button_yes = tk.Radiobutton(self.settingsFrame, text="Да", variable=self.restart_radiobuttons,
                                               value=1)
        self.radio_button_no = tk.Radiobutton(self.settingsFrame, text="Нет", variable=self.restart_radiobuttons,
                                              value=0)
        self.radio_button_yes.grid(row=9, column=1)
        self.radio_button_no.grid(row=9, column=2)

        self.same_images = tk.IntVar()
        self.same_images.set(0)
        self.same_images_yes = tk.Radiobutton(self.settingsFrame, text="Да", variable=self.same_images, value=1)
        self.same_images_no = tk.Radiobutton(self.settingsFrame, text="Нет", variable=self.same_images, value=0)
        self.same_images_yes.grid(row=10, column=1)
        self.same_images_no.grid(row=10, column=2)

    def save_settings(self):
        self.error_label.grid_forget()
        error_text = ''

        for entry in self.entries:
            error_text = entry.check_value()
            if error_text:
                break

        if error_text:
            self.error_label.configure(text=error_text)
            self.error_label.pack()
        else:
            settings.delay = [float(i.get()) for i in self.entries[2:7]]
            settings.session_number = int(self.entries[0].get())
            settings.repeat_number = int(self.entries[1].get())
            settings.image_size = int(self.entries[-2].get())
            settings.distance_between_images = int(self.entries[-1].get())
            settings.restart_after_answer = bool(self.restart_radiobuttons.get())
            settings.same_images = bool(self.same_images.get())
            self.destroy()


if __name__ == '__main__':
    window = ExperimentSettingsWindow()
    window.mainloop()
