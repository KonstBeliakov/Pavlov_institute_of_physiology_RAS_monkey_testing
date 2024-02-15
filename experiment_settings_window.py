import tkinter as tk

import settings
from export_settings_window import ExportSettingsWindow
from import_settings_window import ImportSettingsWindow


class ExperimentSettingsWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
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

        self.buttonFrame = tk.Frame(self)
        self.buttonFrame.grid(row=1, column=0)

        self.btn_confirm = tk.Button(self.buttonFrame, text='Применить', command=self.save_settings)
        self.btn_confirm.grid(row=0, column=0)
        self.btn_confirm = tk.Button(self.buttonFrame, text='Отмена', command=self.cansel)
        self.btn_confirm.grid(row=0, column=1)
        self.btn_import_settings = tk.Button(self.buttonFrame, text='Импортировать настройки',
                                             command=self.open_import_settings_window)
        self.btn_import_settings.grid(row=0, column=2)
        self.btn_export_settings = tk.Button(self.buttonFrame, text='Экспортировать настройки',
                                             command=self.open_export_settings_window)
        self.btn_export_settings.grid(row=0, column=3)
        self.error_label = tk.Label(self.buttonFrame, text='Ошибка: в поля времени должны быть введены вещественные числа')

    def save_settings(self):
        self.error_label.grid_forget()
        error_text = ''
        try:
            settings.delay = [float(i.get()) for i in self.delay_entry]
        except:
            error_text = 'Ошибка: в поля для ввода времени задержек должны быть введены вещественные числа'

        try:
            settings.session_number = int(self.entry_session_number.get())
        except:
            error_text = 'Ошибка: количество сессий должно быть целым числом'

        try:
            settings.repeat_number = int(self.entry_repeat_number.get())
        except:
            error_text = 'Ошибка: количество тестов в сессии должно быть целым числом'

        if error_text:
            self.error_label.configure(text=error_text)
            self.error_label.grid(row=9, column=0)

    def cansel(self):
        self.destroy()

    def open_export_settings_window(self):
        self.export_settings_window = ExportSettingsWindow()
        self.export_settings_window.mainloop()

    def open_import_settings_window(self):
        self.import_settings_window = ImportSettingsWindow()
        self.import_settings_window.mainloop()


if __name__ == '__main__':
    window = ExperimentSettingsWindow()
    window.mainloop()
