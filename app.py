import sys
import threading

from customtkinter import *
from CTkMessagebox import CTkMessagebox
from tkinter import PhotoImage
from os import startfile, path

import utils
from frames import *
from settings import settings, APPLICATION_RUNNING
from screeninfo import get_monitors


class App(CTk):
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

        self.tabview = CTkTabview(master=self, command=self.tab_changed)
        self.tabview.pack(expand=True, fill=BOTH)
        frame_texts = ['Общие настройки', 'Запуск эксперимента', 'Проверка устройств', 'Экспорт данных',
                       'Информация о приложении']
        self.frames = []

        for text in frame_texts:
            self.tabview.add(text)
            self.frames.append(self.tabview.tab(text))

        self.test_image = [PhotoImage(file="pictograms/settings.png"),
                           PhotoImage(file="pictograms/run.png"),
                           PhotoImage(file='pictograms/yes.png') if utils.serial_available else PhotoImage(
                               file="pictograms/no.png"),
                           PhotoImage(file="pictograms/data.png"),
                           PhotoImage(file="pictograms/info.png")]

        self.settings_frame = SettingsFrame(self.frames[0], self)
        self.run_frame = RunFrame(self.frames[1], self)
        self.devise_check_frame = DeviseCheckFrame(self.frames[2], self)
        self.dataframe = DataFrame(root=self.frames[3])
        self.info_frame = InfoFrame(self.frames[4])

        self.bind("<Key>", self.key_handler)

    def key_handler(self, event):
        if (event.char == settings['escape_key']):
            self.run_frame.close_experiment_window()

    def tab_changed(self):
        if self.tabview.get() == 'Информация о приложении':
            doc_path = path.abspath(path.join('docs', 'index.html'))
            startfile(doc_path)

    def confirm_delete(self):
        msg = CTkMessagebox(title="Закрыть",
                            message="Вы уверены, что хотите закрыть это окно?",
                            option_1="Да",
                            option_2="Нет")

        if msg.get() == 'Да':
            utils.save_settings()
            APPLICATION_RUNNING = False
            self.destroy()
            sys.exit()


if __name__ == '__main__':
    print('start...')
    set_appearance_mode('System')
    set_default_color_theme('blue')
    app = App()
    app.mainloop()