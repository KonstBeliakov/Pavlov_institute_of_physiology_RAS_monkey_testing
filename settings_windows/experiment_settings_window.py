import tkinter as tk

from settings import settings
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
            ImprovedEntry(self.settingsFrame, 0, 0, 'Количество сессий',                              value_type=int,     min_value=1, save_value='session_number'),
            ImprovedEntry(self.settingsFrame, 0, 1, 'Количество тестов в сессии',                     value_type=int,     min_value=1, save_value='repeat_number'),
            ImprovedEntry(self.settingsFrame, 0, 2, 'Время отображения целевого изображения',         value_type=float,   min_value=0, save_value='delay[0]'),
            ImprovedEntry(self.settingsFrame, 0, 3, 'Задержка перед появлением тестовых изображений', value_type=float,   min_value=0, save_value='delay[1]'),
            ImprovedEntry(self.settingsFrame, 0, 4, 'Время для ответа',                               value_type=float,   min_value=0, save_value='delay[2]'),
            ImprovedEntry(self.settingsFrame, 0, 5, 'Задержка между тестами',                         value_type=float,   min_value=0, save_value='delay[3]'),
            ImprovedEntry(self.settingsFrame, 0, 6, 'Задержка между сессиями',                        value_type=float,   min_value=0, save_value='delay[4]'),
            ImprovedEntry(self.settingsFrame, 0, 7, 'Размер изображения',                             value_type=int,     min_value=1, save_value='image_size'),
            ImprovedEntry(self.settingsFrame, 0, 8, 'Расстояние между изображениями',                 value_type=int,  min_value=1, save_value='distance_between_images')
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
        print(f'error_text: {error_text}')
        if error_text:
            self.error_label.configure(text=error_text)
        else:
            for entry in self.entries:
                entry.save_value()
            self.destroy()


if __name__ == '__main__':
    window = ExperimentSettingsWindow()
    window.mainloop()
