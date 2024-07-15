from customtkinter import *
import tkinter as tk
from tkinter import ttk

from settings import settings
from settings_windows import *
from widgets import WidgetList


class SettingsFrame:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.basic_settings_radio_button_frame = CTkFrame(root)
        self.basic_settings_radio_button_frame.grid(column=0, row=0)

        self.sounds_in_experiments_label = CTkLabel(self.basic_settings_radio_button_frame,
                                                 text='Использовать звуковое подкрепление')
        self.sounds_in_experiments_label.grid(column=0, row=0)
        self.sounds_in_experiments = tk.StringVar(value='Да')
        self.sound_btn_yes = ttk.Radiobutton(self.basic_settings_radio_button_frame, text='Да', value='Да',
                                             variable=self.sounds_in_experiments)
        self.sound_btn_yes.grid(column=1, row=0)
        self.btn_no = ttk.Radiobutton(self.basic_settings_radio_button_frame, text='Нет', value='Нет',
                                      variable=self.sounds_in_experiments)
        self.btn_no.grid(column=2, row=0)

        self.basic_settings_label_frame = CTkFrame(root)
        self.basic_settings_label_frame.grid(column=0, row=1)

        self.widgets_list = WidgetList(self.basic_settings_label_frame, 0, 0, [
            {'text': 'Путь до файла звука начала эксперимента (оставить пустым если не используется)',          'value_type': str, 'save_value': 'experiment_start_sound', 'may_be_empty': True},
            {'text': 'Путь до файла позитивного звукового подкрепления (оставить пустым если не используется)', 'value_type': str, 'save_value': 'right_answer_sound', 'may_be_empty': True},
            {'text': 'Путь до файла негативного звукового подкрепления (оставить пустым если не используется)', 'value_type': str, 'save_value': 'wrong_answer_sound', 'may_be_empty': True},
            {'text': 'Радиус круга отображающегося после нажатия',       'value_type': int,   'min_value': 0, 'save_value': 'mouse_click_circle_radius'},
            {'text': 'Цвет круга',                                       'value_type': str, 'save_value': 'click_circle_color'},
            {'text': 'Толщина линии круга',                              'value_type': int,   'min_value': 0, 'save_value': 'click_circle_width'},
            {'text': 'Время отображения круга',                          'value_type': float, 'min_value': 0, 'save_value': 'click_circle_time'},
            {'text': 'Размер копии второго монитора',                    'value_type': float, 'min_value': 0, 'max_value': 0.5, 'save_value': 'monitor_copy_size'},
            {'text': 'Цвет фона экспериментального окна',                'value_type': str, 'save_value': 'bg_color'},
            {'widget_type': 'radiobutton', 'text': 'Полноэкранный режим экспериментального окна', 'value_type': bool, 'save_value': 'fullscreen_mode'},
            {'text': 'Частота автосохранений (в минутах)', 'value_type': int, 'save_value': 'autosave_period'},
            {'text': 'Номер захватываемого монитора', 'value_type': int, 'save_value': 'captured_monitor'},
            {'text': 'Размер экспериментального монитора', 'value_type': str, 'save_value': 'screen_size', 'may_be_empty': True},
        ])

        self.button_frame = CTkFrame(root)
        self.button_frame.grid(row=2, column=0)

        self.button_apply = CTkButton(self.button_frame, text='Применить', command=self.apply_basic_settings)
        self.button_apply.grid(row=0, column=0)

        self.error_label = tk.Label(root, text='Настройки не применены', fg='#f00')
        self.error_label.grid(row=3, column=0)

        self.button_export = CTkButton(self.button_frame, text='Экспортировать', command=self.export_settings)
        self.button_export.grid(row=0, column=1)

        self.button_import = CTkButton(self.button_frame, text='Импортировать', command=self.import_settings)
        self.button_import.grid(row=0, column=2)

    def apply_basic_settings(self):
        if (error_text := self.widgets_list.save_values(check_validity=True)) is None:
            settings['using_sound'] = (self.sounds_in_experiments.get() == 'Да')
            self.error_label.configure(text='')
        else:
            self.error_label.configure(text=error_text)

    def import_settings(self):
        self.import_settings_window = ImportSettingsWindow(0, self)
        self.import_settings_window.mainloop()

    def export_settings(self):
        self.export_settings_window = ExportSettingsWindow(0, self)
        self.export_settings_window.mainloop()
