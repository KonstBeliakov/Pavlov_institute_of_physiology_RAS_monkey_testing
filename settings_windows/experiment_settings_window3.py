import tkinter as tk
from improved_entry import ImprovedEntry
import settings
from settings_windows.settings_window import SettingsWindow


class ExperimentSettingsWindow3(SettingsWindow):
    def __init__(self):
        super().__init__(experiment_type=3)

        self.settingsFrame = tk.Frame(self)
        self.settingsFrame.grid(column=0, row=0)

        self.entries = [
            ImprovedEntry(self.settingsFrame, 0, 0, 'Время запоминания изображений',      str(settings.delay3[0]),        value_type=float, min_value=0),
            ImprovedEntry(self.settingsFrame, 0, 1, 'Задержка перед ответом',             str(settings.delay3[1]),        value_type=float, min_value=0),
            ImprovedEntry(self.settingsFrame, 0, 2, 'Время на ответ',                     str(settings.delay3[2]),        value_type=float, min_value=0),
            ImprovedEntry(self.settingsFrame, 0, 3, 'Задержка между экспериментами',      str(settings.delay3[3]),        value_type=float, min_value=0),
            ImprovedEntry(self.settingsFrame, 0, 4, 'Минимальное количество изображений', str(settings.min_image_number), value_type=int, min_value=0),
            ImprovedEntry(self.settingsFrame, 0, 5, 'Максимальное количество изображений',str(settings.max_image_number), value_type=int, min_value=0),
            ImprovedEntry(self.settingsFrame, 0, 6, 'Перемешивать изображения (y/n)',     str(settings.shuffle_images),   value_type=str),
            ImprovedEntry(self.settingsFrame, 0, 7, 'Начинать заново после ошибки (y/n)', str(settings.stop_after_error), value_type=str),
            ImprovedEntry(self.settingsFrame, 0, 8, 'Размер изображения',                 str(settings.image_size3),      value_type=int),
            ImprovedEntry(self.settingsFrame, 0, 9, 'Количество изображений в сетке (AxB)',
                          str(f'{settings.grid_size[0]}x{settings.grid_size[1]}'), value_type=str)
        ]

    def save_settings(self):
        error_text = ''

        for entry in self.entries:
            error_text = entry.check_value()
            if error_text:
                break

        if not error_text:
            try:
                l = self.entries[9].get().split('x')
                if len(l) != 2:
                    error_text = 'Размерность сетки должна быть равна 2'
                elif int(l[0]) < 1 or int(l[1]) < 1:
                    error_text = 'Размер сетки не может быть меньше 1'
            except:
                error_text = 'Не получилось обработать параметр "Количество изображений в сетке (AxB)"'

        if error_text:
            self.show_error(error_text)
        else:
            for i in range(len(settings.delay3)):
                settings.delay3[i] = float(self.entries[i].get())
            settings.min_image_number = int(self.entries[4].get())
            settings.max_image_number = int(self.entries[5].get())
            settings.shuffle_images = self.entries[6].get() in ['Да', 'y', 'yes', 'Yes', 'True', 'true', 't', '1', 'YES']
            settings.stop_after_error = self.entries[7].get() in ['Да', 'y', 'yes', 'Yes', 'True', 'true', 't', '1', 'YES']
            settings.image_size3 = int(self.entries[8].get())
            settings.grid_size = [int(i) for i in self.entries[9].get().split('x')]
            self.destroy()


if __name__ == '__main__':
    window = ExperimentSettingsWindow3()
    window.mainloop()
