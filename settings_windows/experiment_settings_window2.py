from tkinter import *

from settings import settings
from settings_windows.settings_window import SettingsWindow
from widgets.widget_list import WidgetList


class ExperimentSettingsWindow2(SettingsWindow):
    def __init__(self):
        super().__init__(experiment_type=2)
        self.title('Настройки эксперимента 2')

        self.settingsFrame = Frame(self)
        self.settingsFrame.grid(column=0, row=0)

        self.widgets_list = WidgetList(self.settingsFrame, 0, 0, [
            {'text': 'Минимальная скорость изображения',  'value_type': int,   'min_value': 0, 'save_value': 'image_min_speed'},
            {'text': 'Максимальная скорость изображения', 'value_type': int,   'min_value': 0, 'save_value': 'image_max_speed'},
            {'text': 'Ширина барьера',                    'value_type': int,   'min_value': 0, 'save_value': 'barrier_width'},
            {'text': 'Цвет барьера',                      'value_type': str,                   'save_value': 'barrier_color'},
            {'text': 'Количество изображений',            'value_type': int,   'min_value': 1, 'save_value': 'image_number'},
            {'text': 'Расстояние до барьера',             'value_type': int,   'min_value': 0, 'save_value': 'barrier_dist'},
            {'widget_type': 'radiobutton', 'text': 'Прямое движение',      'value_type': bool, 'save_value': 'straight_movement'},
            {'text': 'Задержка между экспериментами',     'value_type': float, 'min_value': 0, 'save_value': 'session_delay2'},
            {'text': 'Число повторений',                  'value_type': int,   'min_value': 1, 'save_value': 'repeat_number2'},
            {'text': 'Размер изображения',                'value_type': int,   'min_value': 1, 'save_value': 'image_size2'},
            {'text': 'Используемое изображение',          'value_type': str,                   'save_value': 'exp2_filename', 'may_be_empty': True},
            {'widget_type': 'radiobutton', 'text': 'Движение изображений', 'value_type': str,
             'values': ['Слева направо', 'Справа налево'], 'save_value': 'movement_direction'},
            {'widget_type': 'checkbutton', 'text': 'Отображаемые параметры', 'values': settings['log_header2'],
             'value_type': str, 'save_value': 'current_log_header2', 'values_in_row': 3}
        ])

    def save_settings(self):
        if (error_text := self.widgets_list.save_values(check_validity=True)) is None:
            self.destroy()
        else:
            self.show_error(error_text)


if __name__ == '__main__':
    settings_window = ExperimentSettingsWindow2()
    settings_window.mainloop()
