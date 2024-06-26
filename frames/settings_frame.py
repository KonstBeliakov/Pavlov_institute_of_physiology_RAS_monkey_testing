from tkinter import *
import tkinter as tk
from tkinter import ttk

from settings import settings
from widgets.widget_list import WidgetList


class SettingsFrame:
    def __init__(self, root, app):
        self.root = root
        self.app = app
        self.basic_settings_radio_button_frame = Frame(root)
        self.basic_settings_radio_button_frame.grid(column=0, row=0)

        self.sounds_in_experiments_label = Label(self.basic_settings_radio_button_frame,
                                                 text='Использовать звуковое подкрепление')
        self.sounds_in_experiments_label.grid(column=0, row=0)
        self.sounds_in_experiments = tk.StringVar(value='Да')
        self.sound_btn_yes = ttk.Radiobutton(self.basic_settings_radio_button_frame, text='Да', value='Да',
                                             variable=self.sounds_in_experiments)
        self.sound_btn_yes.grid(column=1, row=0)
        self.btn_no = ttk.Radiobutton(self.basic_settings_radio_button_frame, text='Нет', value='Нет',
                                      variable=self.sounds_in_experiments)
        self.btn_no.grid(column=2, row=0)

        self.basic_settings_label_frame = Frame(root)
        self.basic_settings_label_frame.grid(column=0, row=1)

        self.entries_list = WidgetList(self.basic_settings_label_frame, 0, 0, [
            {'text': 'Путь до файла звука начала эксперимента (оставить пустым если не используется)',          'value_type': str, 'save_value': 'experiment_start_sound', 'may_be_empty': True},
            {'text': 'Путь до файла позитивного звукового подкрепления (оставить пустым если не используется)', 'value_type': str, 'save_value': 'right_answer_sound', 'may_be_empty': True},
            {'text': 'Путь до файла негативного звукового подкрепления (оставить пустым если не используется)', 'value_type': str, 'save_value': 'wrong_answer_sound', 'may_be_empty': True},
            {'text': 'Радиус круга отображающегося после нажатия',       'value_type': int,   'min_value': 0, 'save_value': 'mouse_click_circle_radius'},
            {'text': 'Цвет круга',                                       'value_type': str, 'save_value': 'click_circle_color'},
            {'text': 'Толщина линии круга',                              'value_type': int,   'min_value': 0, 'save_value': 'click_circle_width'},
            {'text': 'Время отображения круга',                          'value_type': float, 'min_value': 0, 'save_value': 'click_circle_time'},
            {'text': 'Размер копии второго монитора',                    'value_type': float, 'min_value': 0, 'max_value': 0.5, 'save_value': 'monitor_copy_size'},
            {'text': 'Цвет фона экспериментального окна',                'value_type': str, 'save_value': 'bg_color'}
        ])

        self.button_apply = Button(root, text='Применить', command=self.apply_basic_settings)
        self.button_apply.grid(row=2, column=0)

        self.error_label = tk.Label(root, text='Настройки не применены', fg='#f00')
        self.error_label.grid(row=3, column=0)

    def apply_basic_settings(self):
        if (error_text := self.entries_list.save_values(check_validity=True)) is None:
            settings['using_sound'] = (self.sounds_in_experiments.get() == 'Да')
            self.error_label.configure(text='')
        else:
            self.error_label.configure(text=error_text)
