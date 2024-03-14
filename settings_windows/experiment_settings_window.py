import tkinter as tk

import settings
from settings_windows.settings_window import SettingsWindow


class ExperimentSettingsWindow(SettingsWindow):
    def __init__(self):
        super().__init__(experiment_type=1)
        self.title('Настройки эксперимента')
        self.export_settings_window = None
        self.import_settings_window = None
        delay_text = ['Время отображения целевого изображения', 'Задержка перед появлением тестовых изображений',
                      'Время для ответа (выбора одного из тестовых изображений)', 'Задержка между тестами',
                      'Задержка между сессиями']
        self.settingsFrame = tk.Frame(self)
        self.settingsFrame.grid(row=0, column=0)

        self.delay_label = [tk.Label(self.settingsFrame, text=i) for i in delay_text]
        self.delay_entry_IntVar = [tk.IntVar() for _ in range(5)]
        for i in range(5):
            self.delay_entry_IntVar[i].set(settings.delay[i])
        self.delay_entry = [tk.Entry(self.settingsFrame, text=self.delay_entry_IntVar[i]) for i in range(5)]

        self.label_session_number = tk.Label(self.settingsFrame, text='Количество сессий')
        self.label_session_number.grid(row=0, column=0)

        self.intVar_session_number = tk.StringVar(self.settingsFrame, '1')
        self.entry_session_number = tk.Entry(self.settingsFrame, text=self.intVar_session_number)
        self.entry_session_number.grid(row=0, column=1)

        self.label_repeat_number = tk.Label(self.settingsFrame, text='Количество тестов в сессии')
        self.label_repeat_number.grid(row=1, column=0)

        self.intVar_repeat_number = tk.StringVar(self, '5')
        self.entry_repeat_number = tk.Entry(self.settingsFrame, text=self.intVar_repeat_number)
        self.entry_repeat_number.grid(row=1, column=1)

        for i in range(5):
            self.delay_label[i].grid(row=i + 2, column=0)
            self.delay_entry[i].grid(row=i + 2, column=1)

        self.restart_label = tk.Label(self.settingsFrame, text='Переходить к следующему тесту после ответа')
        self.restart_label.grid(row=7, column=0)
        self.restart_radiobuttons = tk.IntVar()
        self.restart_radiobuttons.set(0)
        self.radio_button_yes = tk.Radiobutton(self.settingsFrame, text="Да", variable=self.restart_radiobuttons, value=1)
        self.radio_button_no = tk.Radiobutton(self.settingsFrame, text="Нет", variable=self.restart_radiobuttons, value=0)
        self.radio_button_yes.grid(row=8, column=0)
        self.radio_button_no.grid(row=8, column=1)

    def save_settings(self):
        self.error_label.grid_forget()
        error_text = ''
        try:
            [float(i.get()) for i in self.delay_entry]
        except:
            error_text = 'Ошибка: в поля для ввода времени задержек должны быть введены вещественные числа'

        try:
            int(self.entry_session_number.get())
        except:
            error_text = 'Ошибка: количество сессий должно быть целым числом'

        try:
            int(self.entry_repeat_number.get())
        except:
            error_text = 'Ошибка: количество тестов в сессии должно быть целым числом'

        if error_text:
            self.error_label.configure(text=error_text)
            self.error_label.pack()
        else:
            settings.delay = [float(i.get()) for i in self.delay_entry]
            settings.session_number = int(self.entry_session_number.get())
            settings.repeat_number = int(self.entry_repeat_number.get())
            settings.restart_after_answer = bool(self.restart_radiobuttons.get())
            self.destroy()


if __name__ == '__main__':
    window = ExperimentSettingsWindow()
    window.mainloop()
