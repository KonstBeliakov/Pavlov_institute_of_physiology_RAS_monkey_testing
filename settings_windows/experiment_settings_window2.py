from tkinter import *
from settings_windows.settings_window import SettingsWindow
import settings
from improved_entry import ImprovedEntry


class ExperimentSettingsWindow2(SettingsWindow):
    def __init__(self):
        super().__init__(experiment_type=2)
        self.title('Настройки эксперимента')

        self.settingsFrame = Frame(self)
        self.settingsFrame.grid(column=0, row=0)

        self.entries = [
            ImprovedEntry(self.settingsFrame, 0, 0, 'Минимальная скорость изображения',  str(settings.image_min_speed),  value_type=int,   min_value=0),
            ImprovedEntry(self.settingsFrame, 0, 1, 'Максимальная скорость изображения', str(settings.image_max_speed),  value_type=int,   min_value=0),
            ImprovedEntry(self.settingsFrame, 0, 2, 'Ширина барьера',                    str(settings.barrier_width),    value_type=int,   min_value=0),
            ImprovedEntry(self.settingsFrame, 0, 3, 'Цвет барьера',                      str(settings.barrier_color),    value_type=str),
            ImprovedEntry(self.settingsFrame, 0, 4, 'Количество изображений',            str(settings.image_number),     value_type=int,   min_value=1),
            ImprovedEntry(self.settingsFrame, 0, 5, 'Расстояние до барьера',             str(settings.barrier_dist),     value_type=int,   min_value=0),
            ImprovedEntry(self.settingsFrame, 0, 6, 'Прямое движение (true/false)',      str(settings.straight_movement), value_type=str),
            ImprovedEntry(self.settingsFrame, 0, 7, 'Задержка между экспериментами',     str(settings.session_delay2),   value_type=float, min_value=0),
            ImprovedEntry(self.settingsFrame, 0, 7, 'Число повторений',                  str(settings.repeat_number2),   value_type=int,   min_value=1),
        ]

    def save_settings(self):
        error_text = ''

        for entry in self.entries:
            error_text = entry.check_value()
            if error_text:
                break

        if error_text:
            self.show_error(error_text)
        else:
            settings.image_min_speed = int(self.entries[0].get())
            settings.image_max_speed = int(self.entries[1].get())
            settings.barrier_width = int(self.entries[2].get())
            settings.barrier_color = self.entries[3].get()
            settings.image_number = int(self.entries[4].get())
            settings.barrier_dist = int(self.entries[5].get())
            settings.straight_movement = self.entries[6] in ['Да', 'y', 'yes', 'Yes', 'True', 'true', 't', '1', 'YES']
            settings.session_delay2 = float(self.entries[7].get())
            settings.repeat_number2 = int(self.entries[8].get())
            self.destroy()


if __name__ == '__main__':
    settings_window = ExperimentSettingsWindow2()
    settings_window.mainloop()
