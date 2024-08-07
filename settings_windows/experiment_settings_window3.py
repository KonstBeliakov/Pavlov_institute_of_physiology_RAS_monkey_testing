from customtkinter import *

from widgets import WidgetList
from settings import settings
from settings_windows.settings_window import SettingsWindow


class ExperimentSettingsWindow3(SettingsWindow):
    def __init__(self):
        super().__init__(experiment_type=3)
        self.title('Настройки эксперимента 3')

        self.settingsFrame = CTkFrame(self)
        self.settingsFrame.grid(column=0, row=0)

        self.widgets_list = WidgetList(self.settingsFrame, 0, 0, [
            {'text': 'Время запоминания изображений',      'value_type': float, 'min_value': 0, 'save_value': 'delay3[0]'},
            {'text': 'Задержка перед ответом',             'value_type': float, 'min_value': 0, 'save_value': 'delay3[1]'},
            {'text': 'Время на ответ',                     'value_type': float, 'min_value': 0, 'save_value': 'delay3[2]'},
            {'text': 'Задержка между экспериментами',      'value_type': float, 'min_value': 0, 'save_value': 'delay3[3]'},
            {'text': 'Минимальное количество изображений', 'value_type': int,   'min_value': 0, 'save_value': 'min_image_number'},
            {'text': 'Максимальное количество изображений','value_type': int,   'min_value': 0, 'save_value': 'max_image_number'},
            {'widget_type': 'radiobutton', 'text': 'Перемешивать изображения',     'value_type': bool, 'save_value': 'shuffle_images'},
            {'widget_type': 'radiobutton', 'text': 'Начинать заново после ошибки', 'value_type': bool, 'save_value': 'stop_after_error'},
            {'text': 'Размер изображения',                 'value_type': int,                   'save_value': 'image_size3'},
            {'text': 'Количество изображений в сетке (AxB)', 'value': str(f'{settings["grid_size"][0]}x{settings["grid_size"][1]}'), 'value_type': str},
            {'widget_type': 'checkbutton', 'text': 'Отображаемые параметры', 'values': settings['log_header3'],
             'value_type': str, 'save_value': 'current_log_header3', 'values_in_row': 3}
        ])

    def save_settings(self):
        error_text = self.widgets_list.check_values()

        if error_text is None:
            try:
                l = self.widgets_list.widgets[9].get().split('x')
                if len(l) != 2:
                    error_text = 'Размерность сетки должна быть равна 2'
                elif int(l[0]) < 1 or int(l[1]) < 1:
                    error_text = 'Размер сетки не может быть меньше 1'
            except:
                error_text = 'Не получилось обработать параметр "Количество изображений в сетке (AxB)"'

        if error_text:
            self.show_error(error_text)
        else:
            self.widgets_list.save_values(check_validity=False)
            settings['grid_size'] = [int(i) for i in self.widgets_list.widgets[9].get().split('x')]
            self.destroy()


if __name__ == '__main__':
    window = ExperimentSettingsWindow3()
    window.mainloop()
