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


if __name__ == '__main__':
    window = Tk()
    settings_window = ExperimentSettingsWindow()
    settings_window.mainloop()