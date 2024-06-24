import utils
from settings import settings
from widgets.improved_entry import ImprovedEntry
from widgets.improved_radiobuttons import ImprovedRadiobuttons
import tkinter as tk
from tkinter import *

from widgets.widget_list import WidgetList

from os import listdir


class DataFrame:
    def __init__(self, root):
        self.root = root

        self.data_frame0 = Frame(root)
        self.data_frame0.grid(row=0, column=0)

        self.experiment_type_radiobutton = ImprovedRadiobuttons(self.data_frame0, 0, 0, text='Тип эксперимента',
                                                                values=['Запоминание картинки',
                                                                        'Экстраполяция движения',
                                                                        'Новая картинка'],
                                                                value_type=str)

        self.data_frame1 = Frame(root)
        self.data_frame1.grid(row=1, column=0)

        self.time_interval_entries = WidgetList(self.data_frame1, 0, 1, [
            {'text': 'От', 'value_type': 'date', 'save_value': 'selected_period_start', 'may_be_empty': True},
            {'text': 'До', 'value_type': 'date', 'save_value': 'selected_period_end',   'may_be_empty': True}
        ], vertical=True)

        self.button_search = Button(self.data_frame1, text='Найти эксперименты', command=self.find_experiments)
        self.button_search.grid(row=1, column=1)

        self.data_frame_error_label = Label(self.data_frame1, text='', fg='red')
        self.data_frame_error_label.grid(row=2, column=0)

        self.data_frame2 = Frame(root)
        self.data_frame2.grid(row=2, column=0)

        self.experiment_data = tk.Text(self.data_frame2, height=8, width=40)

        t = ' '

        self.experiment_data.insert(tk.END, t)
        self.experiment_data.config(state=DISABLED)
        self.scroll = tk.Scrollbar(self.data_frame2)
        self.experiment_data.configure(yscrollcommand=self.scroll.set)
        self.experiment_data.pack(side=tk.LEFT)

        self.scroll.config(command=self.experiment_data.yview)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.data_frame3 = Frame(root)
        self.data_frame3.grid(row=3, column=0)

        self.filename_entry = ImprovedEntry(self.data_frame3, 0, 0, 'Название файла', value_type=str,
                                            save_value='experiment_data_filename')

        self.button_create_file = Button(self.data_frame3, text='Создать файл', command=self.create_data_file)
        self.button_create_file.grid(row=0, column=2)

    def load_data(self):
        experiment_type = ['Запоминание картинки', 'Экстраполяция движения',
                           'Новая картинка'].index(self.experiment_type_radiobutton.get()) + 1
        files = []
        for file in sorted(listdir('data/')):
            t1 = (not settings['selected_period_start'] or str(settings['selected_period_start']) < file)
            t2 = (not settings['selected_period_end'] or file < str(settings['selected_period_end']))
            t3 = int(file.split('.')[0][-1]) == experiment_type
            if t1 and t2 and t3:
                files.append(file)

        return files

    def find_experiments(self):
        if (error_text := self.time_interval_entries.check_values(show_error=True)) is not None:
            self.data_frame_error_label.configure(text=error_text)
        else:
            if self.time_interval_entries.widgets[0].get():
                self.time_interval_entries.widgets[0].save_value()
            else:
                settings['selected_period_start'] = ''

            if self.time_interval_entries.widgets[1].get():
                self.time_interval_entries.widgets[1].save_value()
            else:
                settings['selected_period_end'] = ''

            self.experiment_type_radiobutton.save_value()

            self.experiment_data.config(state=NORMAL)
            self.experiment_data.delete(1.0, tk.END)
            self.experiment_data.insert(tk.END, '\n'.join(self.load_data()))
            self.experiment_data.config(state=DISABLED)

    def create_data_file(self):
        if self.filename_entry.get():
            export_filename = f'datasets/{self.filename_entry.get()}'
            if not export_filename.endswith('.xlsx'):
                export_filename += '.xlsx'
        else:
            export_filename = None

        utils.export_data(export_file=export_filename, files=[f'data/{i}' for i in self.load_data()])
