from tkinter import *
from tkinter import ttk
from settings_windows.settings_window import SettingsWindow
#from settings_windows.temp import a
import settings


class ExperimentSettingsWindow2(SettingsWindow):
    def __init__(self):
        super().__init__(experiment_type=2)
        self.title('Настройки эксперимента')


        self.settingsFrame = Frame(self)
        self.settingsFrame.grid(column=0, row=0)

        label_names = ['Минимальная скорость изображения', 'Максимальная скорость изображения', 'Ширина барьера',
                       'Цвет барьера', 'Количество изображений', 'Расстояние до барьера', 'Прямое движение',
                       'Задержка между экспериментами', 'Число повторений']

        self.labels = [Label(self.settingsFrame, text=text) for text in label_names]

        self.min_speed_entry = Entry(self.settingsFrame)
        self.min_speed_entry.grid(column=1, row=0)

        self.max_speed_entry = Entry(self.settingsFrame)
        self.max_speed_entry.grid(column=1, row=1)

        self.barrier_width_entry = Entry(self.settingsFrame)
        self.barrier_width_entry.grid(column=1, row=2)

        self.barrier_color_combobox = ttk.Combobox(self.settingsFrame, values=sorted(['red', 'green', 'blue', 'black',
                                                                                      'white', 'yellow', 'magenta', 'cyan']))
        self.barrier_color_combobox.grid(column=1, row=3)

        self.image_number_entry = Entry(self.settingsFrame)
        self.image_number_entry.grid(column=1, row=4)

        self.barrier_dist_entry = Entry(self.settingsFrame)
        self.barrier_dist_entry.grid(column=1, row=5)

        self.straight_movement = StringVar(value="Да")

        self.btn_yes = ttk.Radiobutton(self.settingsFrame, text='Да', value='Да', variable=self.straight_movement)
        self.btn_yes.grid(column=1, row=6)

        self.btn_no = ttk.Radiobutton(self.settingsFrame, text='Нет', value='Нет', variable=self.straight_movement)
        self.btn_no.grid(column=2, row=6)

        self.session_delay_entry = Entry(self.settingsFrame)
        self.session_delay_entry.grid(column=1, row=7)

        self.repeat_entry = Entry(self.settingsFrame)
        self.repeat_entry.grid(column=1, row=8)

        for i, label in enumerate(self.labels):
            label.grid(column=0, row=i)

    def int_value_check(self, value, name, declension=1, min_value=None, max_value=None):
        if not value:
            return f'{name} не указан{["", "о", "а"][declension]}'
        try:
            int(value)
        except:
            return f'{name} долж{["ен", "но", "на"][declension]} быть целым числом'
        if min_value is not None and min_value > int(value):
            return f'{name} не может быть меньше {min_value}'
        if max_value is not None and max_value < int(value):
            return f'{name} не может быть больше {max_value}'

    def save_settings(self):
        error_text = self.int_value_check(self.min_speed_entry.get(),
                                          'Минимальное значение скорости', declension=1, min_value=0)
        if not error_text:
            error_text = self.int_value_check(self.max_speed_entry.get(),
                                              'Максимальное значение скорости', declension=1, min_value=0)

        if not error_text and int(self.min_speed_entry.get()) > int(self.max_speed_entry.get()):
            error_text = 'Максимальное значение скорости должно быть больше минимального'

        if not error_text:
            error_text = self.int_value_check(self.barrier_width_entry.get(),
                                              'Ширина барьера', declension=2, min_value=0)
        if not error_text:
            error_text = self.int_value_check(self.image_number_entry.get(),
                                              'Количество изображений', declension=1, min_value=1, max_value=10)
        if not error_text:
            error_text = self.int_value_check(self.barrier_dist_entry.get(),
                                              'Расстояние до барьера', declension=1, min_value=0)
        if not error_text:
            error_text = self.int_value_check(self.session_delay_entry.get(),
                                              'Задержка между экспериментами', declension=2, min_value=0)
        if not error_text:
            error_text = self.int_value_check(self.repeat_entry.get(),
                                              'Количество повторений', declension=1, min_value=0)

        if error_text:
            self.error_label.configure(text=error_text)
            self.error_label.pack()
        else:
            settings.image_min_speed = int(self.min_speed_entry.get())
            settings.image_max_speed = int(self.max_speed_entry.get())
            settings.barrier_color = self.barrier_color_combobox.get()
            settings.barrier_width = int(self.barrier_width_entry.get())
            settings.image_number = int(self.image_number_entry.get())
            settings.barrier_dist = int(self.barrier_dist_entry.get())
            settings.straight_movement = self.straight_movement == 'Да'
            settings.session_delay2 = float(self.session_delay_entry.get())
            settings.repeat_number2 = int(self.repeat_entry.get())
            self.destroy()


if __name__ == '__main__':
    #print(a)
    window = Tk()
    settings_window = ExperimentSettingsWindow2()
    settings_window.mainloop()
