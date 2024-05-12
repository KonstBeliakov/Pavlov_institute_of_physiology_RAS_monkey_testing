import tkinter as tk

import settings
import utils
from settings_windows.settings_window import SettingsWindow


class ExperimentSettingsWindow(SettingsWindow):
    def __init__(self):
        super().__init__(experiment_type=1)
        self.title('Настройки эксперимента')
        self.export_settings_window = None
        self.import_settings_window = None

        self.settingsFrame = tk.Frame(self)
        self.settingsFrame.grid(row=0, column=0)

        self.label_text = ['Количество сессий', 'Количество тестов в сессии', 'Время отображения целевого изображения',
                           'Задержка перед появлением тестовых изображений',
                           'Время для ответа (выбора одного из тестовых изображений)', 'Задержка между тестами',
                           'Задержка между сессиями', 'Размер изображения', 'Расстояние между изображениями',
                           'Отображать два одинаковых изображения', 'Переходить к следующему тесту после ответа']

        self.labels = [tk.Label(self.settingsFrame, text=i) for i in self.label_text]
        for i, label in enumerate(self.labels):
            label.grid(column=0, row=i)

        self.delay_entry_IntVar = [tk.IntVar() for _ in range(len(self.label_text) - 2)]
        for i, value in enumerate([settings.session_number, settings.repeat_number, settings.delay[0],
                                   settings.delay[1], settings.delay[2], settings.delay[3], settings.delay[4],
                                   settings.image_size, settings.distance_between_images]):
            self.delay_entry_IntVar[i].set(value)

        self.entries = [tk.Entry(self.settingsFrame, text=self.delay_entry_IntVar[i]) for i in
                        range(len(self.label_text) - 2)]
        for i in range(len(self.label_text) - 2):
            self.entries[i].grid(row=i, column=1)

        self.restart_radiobuttons = tk.IntVar()
        self.restart_radiobuttons.set(0)
        self.radio_button_yes = tk.Radiobutton(self.settingsFrame, text="Да", variable=self.restart_radiobuttons,
                                               value=1)
        self.radio_button_no = tk.Radiobutton(self.settingsFrame, text="Нет", variable=self.restart_radiobuttons,
                                              value=0)
        self.radio_button_yes.grid(row=len(self.label_text) - 2, column=1)
        self.radio_button_no.grid(row=len(self.label_text) - 2, column=2)

        self.same_images = tk.IntVar()
        self.same_images.set(0)
        self.same_images_yes = tk.Radiobutton(self.settingsFrame, text="Да", variable=self.same_images, value=1)
        self.same_images_no = tk.Radiobutton(self.settingsFrame, text="Нет", variable=self.same_images, value=0)
        self.same_images_yes.grid(row=len(self.label_text) - 1, column=1)
        self.same_images_no.grid(row=len(self.label_text) - 1, column=2)

    def save_settings(self):
        self.error_label.grid_forget()
        error_text = ''

        for i in range(len(self.label_text) - 2):
            if not error_text:
                error_text = utils.entry_value_check(self.entries[i].get(), self.label_text[i], declension=1,
                                                     min_value=0, max_value=None, value_type=float)
            else:
                break

        if error_text:
            self.error_label.configure(text=error_text)
            self.error_label.pack()
        else:
            settings.delay = [float(i.get()) for i in self.entries[2:7]]
            settings.session_number = int(self.entries[0].get())
            settings.repeat_number = int(self.entries[1].get())
            settings.image_size = int(self.entries[-2].get())
            settings.distance_between_images = int(self.entries[-1].get())
            settings.restart_after_answer = bool(self.restart_radiobuttons.get())
            settings.same_images = bool(self.same_images.get())
            self.destroy()


if __name__ == '__main__':
    window = ExperimentSettingsWindow()
    window.mainloop()
