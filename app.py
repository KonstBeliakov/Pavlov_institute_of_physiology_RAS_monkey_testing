import time
import tkinter as tk
from tkinter import ttk
from tkinter import *
from monkey_window import Monkey_window
import threading
import tkinter.messagebox as mb

import settings
from import_settings_window import ImportSettingsWindow
from export_settings_window import ExportSettingsWindow


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.import_settings_window = None
        self.export_settings_window = None
        self.intVar_repeat_number = None
        self.intVar_session_number = None
        self.entry_repeat_number = None
        self.label_repeat_number = None
        self.entry_session_number = None
        self.label_session_number = None
        self.choose_yes_sound = None
        self.label_choose_no_sound = None
        self.label_choose_yes_sound = None
        self.choose_no_sound = None
        self.btn_import_settings = None
        self.btn_export_settings = None
        self.timer_ask_label = None
        self.choose_experiment_label = None
        self.choose_experiment_combobox = None
        self.radio_button_no = None
        self.radio_button_yes = None
        self.timer_radio_buttons = None
        self.update_thread = None
        self.log_label = []
        self.btn_confirm = None
        self.error_label = None
        self.delay_entry_IntVar = None
        self.delay_label = None
        self.delay_entry = [Entry(), Entry(), Entry()]
        self.info_label = None
        self.btn = None
        self.window = None
        self.started = False

        self.protocol("WM_DELETE_WINDOW", self.confirm_delete)

        notebook = ttk.Notebook()
        notebook.pack(expand=True, fill=BOTH)
        frame_text = ['Общие настройки', 'Запуск эксперимента', 'Информация о приложении']
        self.frame = [ttk.Frame(notebook) for _ in range(3)]

        for i in range(len(self.frame)):
            self.frame[i].pack(fill=BOTH, expand=True)

        self.test_image = [PhotoImage(file="settings.png"), PhotoImage(file="run.png"), PhotoImage(file="info.png")]

        for i in range(len(self.frame)):
            notebook.add(self.frame[i], text=frame_text[i], image=self.test_image[i], compound=LEFT)

        self.info_frame_init()
        self.settings_frame_init()
        self.run_frame_init()

    def confirm_delete(self):
        message = "Вы уверены, что хотите закрыть это окно?"
        if mb.askyesno(message=message, parent=self):
            self.destroy()

    def info_frame_init(self):
        frame_number = 2
        self.info_label = Label(self.frame[frame_number],
                                text="Настроить параметры запуска можно в одной из вкладок настроек, после чего "
                                     "тестирование запускается кнопкой во вкладке \"Запуск эксперимента\"\nДанные полученные в "
                                     "результате тестирования будут записаны в текстовый файл data.txt")
        self.info_label.pack()

    def settings_frame_init(self):
        frame_number = 0
        delay_text = ['Время отображения целевого изображения', 'Задержка перед появлением тестовых изображений',
                      'Время для ответа (выбора одного из тестовых изображений)', 'Задержка между тестами',
                      'Задержка между сессиями']

        self.delay_label = [Label(self.frame[frame_number], text=i) for i in delay_text]
        self.delay_entry_IntVar = [IntVar() for _ in range(5)]
        for i in range(5):
            self.delay_entry_IntVar[i].set(settings.delay[i])
        self.delay_entry = [Entry(self.frame[frame_number], text=self.delay_entry_IntVar[i]) for i in range(5)]

        self.label_session_number = Label(self.frame[frame_number], text='Количество сессий')
        self.label_session_number.grid(row=0, column=0)

        self.intVar_session_number = StringVar(self.frame[frame_number], '1')
        self.entry_session_number = Entry(self.frame[frame_number], text=self.intVar_session_number)
        self.entry_session_number.grid(row=0, column=1)

        self.label_repeat_number = Label(self.frame[frame_number], text='Количество тестов в сессии')
        self.label_repeat_number.grid(row=1, column=0)

        self.intVar_repeat_number = StringVar(self.frame[frame_number], '5')
        self.entry_repeat_number = Entry(self.frame[frame_number], text=self.intVar_repeat_number)
        self.entry_repeat_number.grid(row=1, column=1)

        for i in range(5):
            self.delay_label[i].grid(row=i + 2, column=0)
            self.delay_entry[i].grid(row=i + 2, column=1)
        self.label_choose_yes_sound = Label(self.frame[frame_number],
                                            text='Путь до файла позитивного звукового подкрепления')
        self.label_choose_yes_sound.grid(row=7, column=0)
        self.choose_yes_sound = Entry(self.frame[frame_number])
        self.choose_yes_sound.grid(row=7, column=1)

        self.label_choose_no_sound = Label(self.frame[frame_number],
                                           text='Путь до файла негативного звукового подкрепления')
        self.label_choose_no_sound.grid(row=8, column=0)
        self.choose_no_sound = Entry(self.frame[frame_number])
        self.choose_no_sound.grid(row=8, column=1)

        self.btn_confirm = tk.Button(self.frame[frame_number], text='Применить', command=self.save_settings)
        self.btn_confirm.grid(row=9, column=0)
        self.btn_import_settings = tk.Button(self.frame[frame_number], text='Импортировать настройки',
                                             command=self.open_import_settings_window)
        self.btn_import_settings.grid(row=9, column=1)
        self.btn_export_settings = tk.Button(self.frame[frame_number], text='Экспортировать настройки',
                                             command=self.open_export_settings_window)
        self.btn_export_settings.grid(row=9, column=2)
        self.error_label = Label(self.frame[frame_number],
                                 text='Ошибка: в поля времени должны быть введены вещественные числа')

    def run_frame_init(self):
        frame_number = 1
        self.choose_experiment_label = Label(self.frame[frame_number], text='Тип эксперимента')
        self.choose_experiment_label.grid(row=0, column=0)

        self.choose_experiment_combobox = ttk.Combobox(self.frame[frame_number], values=['Запоминание картинки'])
        self.choose_experiment_combobox.grid(row=1, column=0)

        self.timer_ask_label = Label(self.frame[frame_number], text='Обнулить глобальный таймер эксперимента')
        self.timer_ask_label.grid(row=2, column=0)

        self.timer_radio_buttons = IntVar()
        self.timer_radio_buttons.set(0)
        self.radio_button_yes = Radiobutton(self.frame[frame_number], text="Да", variable=self.timer_radio_buttons,
                                            value=1)
        self.radio_button_no = Radiobutton(self.frame[frame_number], text="Нет", variable=self.timer_radio_buttons,
                                           value=0)
        self.radio_button_yes.grid(row=3, column=0)
        self.radio_button_no.grid(row=3, column=1)

        self.btn = tk.Button(self.frame[frame_number], text="Запустить тестирование", command=self.open_about)
        self.btn.grid(row=4, column=0)

    def open_export_settings_window(self):
        self.export_settings_window = ExportSettingsWindow()
        self.export_settings_window.mainloop()

    def open_import_settings_window(self):
        self.import_settings_window = ImportSettingsWindow()
        self.import_settings_window.mainloop()

    def open_about(self):
        if not self.started:
            self.btn.configure(text="Завершить тестирование")
            self.started = True
            self.window = Monkey_window()

            self.update_thread = threading.Thread(target=self.update_log)
            self.update_thread.start()

            self.window.mainloop()
        else:
            self.window.destroy()
            self.btn.configure(text="Запустить тестирование")
            self.started = False

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

    def update_log(self):
        while True:
            self.log_label = [[tk.Label(self.frame[1], text=text, fg='#0f0' if line[-1] == line[-2] else '#f00')
                               for text in line] for line in self.window.log[-10:]]
            for i in range(len(self.log_label)):
                for j in range(len(self.log_label[i])):
                    self.log_label[i][j].grid(row=i, column=1 + j)
            time.sleep(1)
