from customtkinter import *

from settings import settings
from widgets import WidgetList
from settings_windows.settings_window import SettingsWindow


class ExperimentSettingsWindow1(SettingsWindow):
    def __init__(self):
        super().__init__(experiment_type=1)
        self.title('Настройки эксперимента 1')

        self.settingsFrame = CTkFrame(self)
        self.settingsFrame.grid(row=0, column=0)

        self.widgets_list = WidgetList(self.settingsFrame, 0, 0, [
            {'text': 'Количество сессий',                              'value_type': int,     'min_value': 1, 'save_value': 'session_number'},
            {'text': 'Количество тестов в сессии',                     'value_type': int,     'min_value': 1, 'save_value': 'repeat_number'},
            {'text': 'Время отображения целевого изображения',         'value_type': float,   'min_value': 0, 'save_value': 'delay[0]'},
            {'text': 'Задержки перед появлением тестовых изображений \n(несколько чисел через пробел)', 'value_type': 'list float',    'min_value': 0, 'save_value': 'delay[1]'},
            {'text': 'Время для ответа',                               'value_type': float,   'min_value': 0, 'save_value': 'delay[2]'},
            {'text': 'Задержка между тестами',                         'value_type': float,   'min_value': 0, 'save_value': 'delay[3]'},
            {'text': 'Задержка между сессиями',                        'value_type': float,   'min_value': 0, 'save_value': 'delay[4]'},
            {'text': 'Размер изображения',                             'value_type': int,     'min_value': 1, 'save_value': 'image_size'},
            {'text': 'Расстояние между изображениями',                 'value_type': int,     'min_value': 1, 'save_value': 'distance_between_images'},
            {'widget_type': 'radiobutton', 'text': 'Отображать целевое изображение дважды',    'value_type': bool, 'save_value': 'display_target_image_twice'},
            {'widget_type': 'radiobutton', 'text': 'Перемешивать задержки',                    'value_type': bool, 'save_value': 'mix_delays'},
            {'text': 'Процент правильных ответов в первом окне',       'value_type': int,     'min_value': 0, 'save_value': 'correct_answers_percentage'},
            {'widget_type': 'radiobutton', 'text': 'Уравнять правильные ответы по задержкам', 'value_type': bool, 'save_value': 'equalize_correct_answers_by_delays'},
            {'widget_type': 'radiobutton', 'text': 'Переходить к следующему заданию после ответа\n(досрочное завершение времени на ответ)', 'value_type': bool, 'save_value': 'restart_after_answer'},
            {'widget_type': 'radiobutton', 'text': 'Способ выбора изображений', 'values': ['Случайный', 'Парами'], 'value_type': str, 'save_value': 'image_selection_method'},
            {'widget_type': 'radiobutton', 'text': 'Правильный ответ', 'values': ['Новое изображение', 'Старое изображение'], 'value_type': str, 'save_value': 'right_image'},
            {'text': 'Брать изображения из папки', 'value_type': str, 'save_value': 'experiment1_directory', 'may_be_empty': True},
            {'widget_type': 'radiobutton', 'text': 'Использованные изображения', 'values': ['Игнорировать', 'Переносить', 'Удалять'], 'value_type': str, 'save_value': 'used_images'},
            {'text': 'Папка для переноса использованных изображений', 'value_type': str, 'save_value': 'used_images_directory'},
            {'widget_type': 'checkbutton', 'text': 'Отображаемые параметры', 'values': settings['log_header1'],
             'value_type': str, 'save_value': 'current_log_header1', 'values_in_row': 3},
        ])

    def save_settings(self):
        if (error_text := self.widgets_list.save_values(check_validity=True)) is None:
            self.destroy()
        else:
            self.show_error(error_text)


if __name__ == '__main__':
    window = ExperimentSettingsWindow1()
    window.mainloop()
