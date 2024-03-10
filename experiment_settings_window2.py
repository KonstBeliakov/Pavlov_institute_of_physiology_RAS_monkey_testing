from tkinter import *
from tkinter import ttk
from settings_window import SettingsWindow


class ExperimentSettingsWindow(SettingsWindow):
    def __init__(self):
        super().__init__(experiment_type=2)
        self.title('Настройки эксперимента')

        self.settingsFrame = Frame(self)
        self.settingsFrame.grid(column=0, row=0)

        self.labels = [Label(self.settingsFrame, text=text) for text in ['Минимальная скорость изображения',
                                                          'Максимальная скорость изображения',
                                                          'Ширина барьера', 'Цвет барьера', 'Количество изображений']]

        self.min_speed_entry = Entry(self.settingsFrame)
        self.min_speed_entry.grid(column=1, row=0)

        self.max_speed_entry = Entry(self.settingsFrame)
        self.max_speed_entry.grid(column=1, row=1)

        self.barrier_width_entry = Entry(self.settingsFrame)
        self.barrier_width_entry.grid(column=1, row=2)

        self.barrier_color_combobox = ttk.Combobox(self.settingsFrame, values=sorted(['red', 'green', 'blue', 'black']))
        self.barrier_color_combobox.grid(column=1, row=3)

        self.image_number_entry = Entry(self.settingsFrame)
        self.image_number_entry.grid(column=1, row=4)

        for i, label in enumerate(self.labels):
            label.grid(column=0, row=i)

    def save_settings(self):
        self.error_label.grid_forget()
        error_text = ''

        if not self.min_speed_entry.get():
            error_text = 'Значение минимальной скорости не указано'
        if not error_text and not self.max_speed_entry.get():
            error_text = 'Значение максимальной скорости не указано'

        if not error_text:
            try:
                int(self.min_speed_entry.get())
                int(self.max_speed_entry.get())
            except:
                error_text = 'Значения минимальной и максимальной скоростей изображения должны быть целыми числами'

        if not error_text:
            if int(self.min_speed_entry.get()) < 0 or int(self.max_speed_entry.get()) < 0:
                error_text = 'Значения скоростей не могут быть отрицательными'

        if not error_text:
            if int(self.min_speed_entry.get()) > int(self.max_speed_entry.get()):
                error_text = 'Максимальное значение скорости должно быть больше минимального'

        if not error_text and not self.barrier_width_entry.get():
            error_text = 'Ширина барьера не указана'

        if not error_text:
            try:
                assert int(self.barrier_width_entry.get()) > 0
            except:
                error_text = 'Ширина барьера должна быть положительным числом'

        if not error_text and not self.image_number_entry.get():
            error_text = 'Количество изображений не указано'

        if not error_text:
            try:
                int(self.image_number_entry.get())
            except:
                error_text = 'Количество изображений должно быть целым числом'

        if not error_text:
            if not 10 >= int(self.image_number_entry.get()) > 0:
                error_text = 'Количество изображений не может быть меньше 1 или больше 10'

        if error_text:
            self.error_label.configure(text=error_text)
            self.error_label.pack()
        else:
            # saving settings
            self.destroy()


if __name__ == '__main__':
    window = Tk()
    settings_window = ExperimentSettingsWindow()
    settings_window.mainloop()