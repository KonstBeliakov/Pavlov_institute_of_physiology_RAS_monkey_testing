from customtkinter import *
import tkinter as tk

from settings import settings
from settings_windows import *
from widgets import WidgetList
from style import *


class SettingsFrame:
    def __init__(self, root, app):
        self.root = root
        self.app = app

        self.basic_settings_label_frame = CTkFrame(root, fg_color=frame_fg_color)
        self.basic_settings_label_frame.grid(column=0, row=1)

        self.widget_list_header = CTkLabel(self.basic_settings_label_frame, text='Общие настройки для всех экспериментов')
        self.widget_list_header.pack()

        self.widget_list_frame = CTkFrame(self.basic_settings_label_frame, fg_color=frame_fg_color2)
        self.widget_list_frame.pack()

        self.widgets_list = WidgetList(self.widget_list_frame, 0, 0, [
            {'text': 'Использовать звуковое подкрепление', 'widget_type': 'radiobutton','value_type': bool,
             'save_value': 'using_sound'},
            {'text': 'Путь до файла звука начала эксперимента\n(оставить пустым если не используется)',
             'value_type': str, 'save_value': 'experiment_start_sound', 'may_be_empty': True},
            {'text': 'Путь до файла звука начала теста\n(оставить пустым если не используется)',
             'value_type': str, 'save_value': 'test_start_sound', 'may_be_empty': True},
            {'text': 'Путь до файла позитивного звукового подкрепления\n(оставить пустым если не используется)',
             'value_type': str, 'save_value': 'right_answer_sound', 'may_be_empty': True},
            {'text': 'Путь до файла негативного звукового подкрепления\n(оставить пустым если не используется)',
             'value_type': str, 'save_value': 'wrong_answer_sound', 'may_be_empty': True},
            {'text': 'Радиус круга отображающегося после нажатия', 'value_type': int, 'min_value': 0,
             'save_value': 'mouse_click_circle_radius'},
            {'text': 'Цвет круга', 'value_type': str, 'save_value': 'click_circle_color'},
            {'text': 'Толщина линии круга', 'value_type': int, 'min_value': 0, 'save_value': 'click_circle_width'},
            {'text': 'Время отображения круга', 'value_type': float, 'min_value': 0, 'save_value': 'click_circle_time'},
            {'text': 'Размер копии второго монитора', 'value_type': float, 'min_value': 0, 'max_value': 0.5,
             'save_value': 'monitor_copy_size'},
            {'text': 'Цвет фона экспериментального окна', 'value_type': str, 'save_value': 'bg_color'},
            {'widget_type': 'radiobutton', 'text': 'Полноэкранный режим экспериментального окна', 'value_type': bool,
             'save_value': 'fullscreen_mode'},
            {'text': 'Частота автосохранений (в минутах)', 'value_type': int, 'save_value': 'autosave_period'},
            {'text': 'Номер захватываемого монитора', 'value_type': int, 'save_value': 'captured_monitor'},
            {'text': 'Размер экспериментального монитора', 'value_type': str, 'save_value': 'screen_size',
             'may_be_empty': True},
            {'widget_type': 'radiobutton', 'text': 'Автоматически перемещать курсор на\nоператорский монитор',
             'value_type': bool, 'save_value': 'move_cursor'},
            {'text': 'Длительность положительного подкрепления', 'value_type': float, 'save_value': 'drink_delay'},
            {'widget_type': 'radiobutton', 'text': 'Используемый скрипт arduino', 'values': ['18-10-03.ino', '24-07-18.ino'],
             'value_type': str, 'save_value': 'arduino_script'},
            {'text': 'Время работы заслонки для подъема/опускания', 'value_type': float,
             'save_value': 'barrier_working_time'},
        ])

        self.button_frame = CTkFrame(root, fg_color='transparent')
        self.button_frame.grid(row=2, column=0)

        self.button_apply = CTkButton(self.button_frame, text='Применить', command=self.apply_basic_settings)
        self.button_apply.grid(row=0, column=0, padx=1, pady=5)

        self.button_export = CTkButton(self.button_frame, text='Экспортировать', command=self.export_settings)
        self.button_export.grid(row=0, column=1, padx=1, pady=5)

        self.button_import = CTkButton(self.button_frame, text='Импортировать', command=self.import_settings)
        self.button_import.grid(row=0, column=2, padx=1, pady=5)

        self.error_label = CTkLabel(root, text='Настройки не применены', text_color='#f00')
        self.error_label.grid(row=3, column=0)

    def apply_basic_settings(self):
        if (error_text := self.widgets_list.save_values(check_validity=True)) is None:
            self.error_label.configure(text='')
        else:
            self.error_label.configure(text=error_text)

    def import_settings(self):
        self.import_settings_window = ImportSettingsWindow(0, self)
        self.import_settings_window.mainloop()

    def export_settings(self):
        self.export_settings_window = ExportSettingsWindow(0, self)
        self.export_settings_window.mainloop()
