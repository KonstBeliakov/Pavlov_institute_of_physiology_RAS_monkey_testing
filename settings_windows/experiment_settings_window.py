import tkinter as tk

from widgets.entry_list import EntryList
from settings_windows.settings_window import SettingsWindow


class ExperimentSettingsWindow(SettingsWindow):
    def __init__(self):
        super().__init__(experiment_type=1)
        self.title('Настройки эксперимента')
        self.export_settings_window = None
        self.import_settings_window = None

        self.settingsFrame = tk.Frame(self)
        self.settingsFrame.grid(row=0, column=0)

        self.entries_list = EntryList(self.settingsFrame, 0, 0, [
            {'text': 'Количество сессий',                              'value_type': int,     'min_value': 1, 'save_value': 'session_number'},
            {'text': 'Количество тестов в сессии',                     'value_type': int,     'min_value': 1, 'save_value': 'repeat_number'},
            {'text': 'Время отображения целевого изображения',         'value_type': float,   'min_value': 0, 'save_value': 'delay[0]'},
            {'text': 'Задержки перед появлением тестовых изображений \n(несколько чисел через пробел)', 'value_type': 'list float',    'min_value': 0, 'save_value': 'delay[1]'},
            {'text': 'Время для ответа',                               'value_type': float,   'min_value': 0, 'save_value': 'delay[2]'},
            {'text': 'Задержка между тестами',                         'value_type': float,   'min_value': 0, 'save_value': 'delay[3]'},
            {'text': 'Задержка между сессиями',                        'value_type': float,   'min_value': 0, 'save_value': 'delay[4]'},
            {'text': 'Размер изображения',                             'value_type': int,     'min_value': 1, 'save_value': 'image_size'},
            {'text': 'Расстояние между изображениями',                 'value_type': int,     'min_value': 1, 'save_value': 'distance_between_images'},
            {'text': 'Отображать целевое изображение дважды (y/n)',    'value_type': bool,                    'save_value': 'display_target_image_twice'},
            {'text': 'Перемешивать задержки (y/n)',                    'value_type': bool,                    'save_value': 'mix_delays'},
            {'text': 'Процент правильных ответов в первом окне',       'value_type': int,     'min_value': 0, 'save_value': 'correct_answers_percentage'}
        ])


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
        if (error_text := self.entries_list.save_values(check_validity=True)) is None:
            self.destroy()
        else:
            self.show_error(error_text)


if __name__ == '__main__':
    window = ExperimentSettingsWindow()
    window.mainloop()
