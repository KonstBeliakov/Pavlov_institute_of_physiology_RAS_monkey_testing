import threading
import tkinter as tk
from tkinter import ttk

from tkinter import *
import tkinter.messagebox as mb

import utils
from frames import *
from settings import settings
from screeninfo import get_monitors


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Основное окно')

        utils.move_to_first_screen(self)

        self.protocol("WM_DELETE_WINDOW", self.confirm_delete)

        utils.load_settings()
        utils.start_auto_saving()

        if settings['fullscreen_mode'] and len(get_monitors()) >= 2:
            t = threading.Thread(target=utils.paint_second_monitor)
            t.start()

        self.notebook = ttk.Notebook()
        self.notebook.pack(expand=True, fill=BOTH)
        frame_text = ['Общие настройки', 'Запуск эксперимента', 'Проверка устройств', 'Экспорт данных',
                      'Информация о приложении']
        self.frame = [ttk.Frame(self.notebook) for _ in range(len(frame_text))]

        for frame in self.frame:
            frame.pack(fill=BOTH, expand=True)

        self.test_image = [PhotoImage(file="pictograms/settings.png"),
                           PhotoImage(file="pictograms/run.png"),
                           PhotoImage(file='pictograms/yes.png') if utils.serial_available else PhotoImage(file="pictograms/no.png"),
                           PhotoImage(file="pictograms/data.png"),
                           PhotoImage(file="pictograms/info.png")]

        for i in range(len(self.frame)):
            self.notebook.add(self.frame[i], text=frame_text[i], image=self.test_image[i], compound=LEFT)

        self.settings_frame = SettingsFrame(self.frame[0], self)
        self.run_frame = RunFrame(self.frame[1], self)
        self.devise_check_frame = DeviseCheckFrame(self.frame[2], self)
        self.dataframe = DataFrame(root=self.frame[3])
        self.info_frame = InfoFrame(self.frame[4])

    def confirm_delete(self):
        message = "Вы уверены, что хотите закрыть это окно?"
        if mb.askyesno(message=message, parent=self):
            utils.save_settings()
            self.destroy()


if __name__ == '__main__':
    print('start...')
    app = App()
    app.mainloop()
