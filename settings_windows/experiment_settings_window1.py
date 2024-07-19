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

        self.frame1 = CTkFrame(self.settingsFrame)
        self.frame1.grid(row=0, column=0, padx=5, pady=5, stick='ns')

        self.widget_list_frame_header = CTkLabel(master=self.frame1, text='Настройки эксперимента')
        self.widget_list_frame_header.pack()

        self.widget_list_frame = CTkFrame(master=self.frame1)
        self.widget_list_frame.pack(padx=2, pady=2)

        self.widgets_list = WidgetList(self.widget_list_frame, 0, 0, [
            {'text': 'Количество сессий', 'value_type': int, 'min_value': 1, 'save_value': 'session_number'},
            {'text': 'Количество тестов в сессии', 'value_type': int, 'min_value': 1, 'save_value': 'repeat_number'},
            {'text': 'Размер изображения', 'value_type': int, 'min_value': 1, 'save_value': 'image_size'},
            {'text': 'Расстояние между изображениями', 'value_type': int, 'min_value': 1,
             'save_value': 'distance_between_images'},
            {'widget_type': 'radiobutton', 'text': 'Отображать целевое изображение дважды', 'value_type': bool,
             'save_value': 'display_target_image_twice'},
            {'widget_type': 'radiobutton', 'text': 'Перемешивать задержки', 'value_type': bool,
             'save_value': 'mix_delays'},
            {'text': 'Процент правильных ответов в первом окне', 'value_type': int, 'min_value': 0,
             'save_value': 'correct_answers_percentage'},
            {'widget_type': 'radiobutton', 'text': 'Уравнять правильные ответы по задержкам', 'value_type': bool,
             'save_value': 'equalize_correct_answers_by_delays'},
            {'widget_type': 'radiobutton',
             'text': 'Переходить к следующему заданию после ответа\n(досрочное завершение времени на ответ)',
             'value_type': bool, 'save_value': 'restart_after_answer'},
            {'widget_type': 'radiobutton', 'text': 'Способ выбора изображений', 'values': ['Случайный', 'Парами'],
             'value_type': str, 'save_value': 'image_selection_method'},
            {'widget_type': 'radiobutton', 'text': 'Правильный ответ',
             'values': ['Новое изображение', 'Старое изображение'], 'value_type': str, 'save_value': 'right_image'},
            {'text': 'Брать изображения из папки', 'value_type': str, 'save_value': 'experiment1_directory',
             'may_be_empty': True},
            {'widget_type': 'radiobutton', 'text': 'Использованные изображения',
             'values': ['Игнорировать', 'Переносить', 'Удалять'], 'value_type': str, 'save_value': 'used_images'},
            {'text': 'Папка для переноса использованных изображений', 'value_type': str,
             'save_value': 'used_images_directory'},
            {'widget_type': 'checkbutton', 'text': 'Отображаемые параметры', 'values': settings['log_header1'],
             'value_type': str, 'save_value': 'current_log_header1', 'values_in_row': 3},
        ])

        self.frame2 = CTkFrame(self.settingsFrame)
        self.frame2.grid(row=0, column=1, padx=5, pady=5, stick='ns')

        self.delay_settings_header = CTkLabel(master=self.frame2, text='Настройки задержек в эксперименте')
        self.delay_settings_header.pack()

        self.delay_widget_list_frame = CTkFrame(master=self.frame2)
        self.delay_widget_list_frame.pack(padx=2, pady=2)

        self.delay_widget_list = WidgetList(self.delay_widget_list_frame, 0, 0, [
            {'text': 'Задержка перед появлением целевого изображения', 'value_type': float, 'min_value': 0,
             'save_value': 'delay[5]'},
            {'text': 'Время перед звуковым оповещением после начала эксперимента', 'value_type': float, 'min_value': 0,
             'save_value': 'delay[6]'},
            {'text': 'Время отображения целевого изображения', 'value_type': float, 'min_value': 0,
             'save_value': 'delay[0]'},
            {'text': 'Задержки перед появлением тестовых изображений \n(несколько чисел через пробел)',
             'value_type': 'list float', 'min_value': 0, 'save_value': 'delay[1]'},
            {'text': 'Время для ответа', 'value_type': float, 'min_value': 0, 'save_value': 'delay[2]'},
            {'text': 'Время перед подъемом заслонки\nпосле скрытия тестовых изображений', 'value_type': float,
             'min_value': 0, 'save_value': 'barrier_delay'},
            {'text': 'Задержка между тестами\n(после того как заслонка поднята)', 'value_type': float, 'min_value': 0,
             'save_value': 'delay[3]'},
            {'text': 'Задержка между сессиями', 'value_type': float, 'min_value': 0, 'save_value': 'delay[4]'},
        ])

    def save_settings(self):
        if (error_text := self.delay_widget_list.check_values(show_error=True)) is not None:
            self.show_error(error_text)
        elif (error_text := self.widgets_list.check_values(show_error=True)) is not None:
            self.show_error(error_text)
        else:
            self.widgets_list.save_values(check_validity=False)
            self.delay_widget_list.save_values(check_validity=False)
            self.destroy()


if __name__ == '__main__':
    window = ExperimentSettingsWindow1()
    window.mainloop()
