from tkinter import *
from settings_windows.settings_window import SettingsWindow
from settings import settings
from improved_entry import ImprovedEntry


class ExperimentSettingsWindow2(SettingsWindow):
    def __init__(self):
        super().__init__(experiment_type=2)
        self.title('Настройки эксперимента')

        self.settingsFrame = Frame(self)
        self.settingsFrame.grid(column=0, row=0)

        self.entries = [
            ImprovedEntry(self.settingsFrame, 0, 0, 'Минимальная скорость изображения',  value_type=int,   min_value=0, save_value='image_min_speed'),
            ImprovedEntry(self.settingsFrame, 0, 1, 'Максимальная скорость изображения', value_type=int,   min_value=0, save_value='image_max_speed'),
            ImprovedEntry(self.settingsFrame, 0, 2, 'Ширина барьера',                    value_type=int,   min_value=0, save_value='barrier_width'),
            ImprovedEntry(self.settingsFrame, 0, 3, 'Цвет барьера',                      value_type=str,                save_value='barrier_color'),
            ImprovedEntry(self.settingsFrame, 0, 4, 'Количество изображений',            value_type=int,   min_value=1, save_value='image_number'),
            ImprovedEntry(self.settingsFrame, 0, 5, 'Расстояние до барьера',             value_type=int,   min_value=0, save_value='barrier_dist'),
            ImprovedEntry(self.settingsFrame, 0, 6, 'Прямое движение (true/false)',      value_type=str,               save_value='straight_movement'),
            ImprovedEntry(self.settingsFrame, 0, 7, 'Задержка между экспериментами',     value_type=float, min_value=0, save_value='session_delay2'),
            ImprovedEntry(self.settingsFrame, 0, 8, 'Число повторений',                  value_type=int,   min_value=1, save_value='repeat_number2'),
            ImprovedEntry(self.settingsFrame, 0, 9, 'Размер изображения',                value_type=int,   min_value=1, save_value='image_size2'),
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
            for entry in self.entries:
                entry.save_value()
            settings['straight_movement'] = self.entries[6] in ['Да', 'y', 'yes', 'Yes', 'True', 'true', 't', '1', 'YES']
            self.destroy()


if __name__ == '__main__':
    settings_window = ExperimentSettingsWindow2()
    settings_window.mainloop()
