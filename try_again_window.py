from customtkinter import *

import utils


class TryAgainWindow(CTkToplevel):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.title('Ошибка')
        self.geometry('600x120')
        utils.move_to_first_screen(self)

        self.label = CTkLabel(self, text='При сохранении данных эксперимента произошла ошибка.\n'
                                         'Скоре всего название файла было написано не правильно (или не было указано).\n'
                                         'Для того чтобы сохранение прошло успешно, файл должен иметь расширение .xlsx')
        self.label.pack()
        self.frame = CTkFrame(self)
        self.frame.pack()

        self.label2 = CTkLabel(self.frame, text='Введите название файла записи данных эксперимента')
        self.entry = CTkEntry(self.frame)

        self.frame2 = CTkFrame(self)
        self.frame2.pack()

        self.button_confirm = CTkButton(self.frame2, text='Сохранить в указанный файл', command=self.save)
        self.button_authosave = CTkButton(self.frame2, text='Автосохранение', command=lambda: self.save(autosave=True))
        self.button_cansel = CTkButton(self.frame2, text='Не сохранять данные эксперимента', command=self.cansel)

        self.failed_label = CTkLabel(self, text='Не удалось сохранить: попробуйте еще раз', fg_color='#f00')

        self.label2.grid(row=0, column=0)
        self.entry.grid(row=0, column=1)
        self.button_confirm.grid(row=0, column=0)
        self.button_authosave.grid(row=0, column=1)
        self.button_cansel.grid(row=0, column=2)

    def save(self, autosave=False):
        try:
            self.parent.save_experiment_data(self.entry.get(), autosave=autosave)
        except Exception as e:
            print(e)
            self.failed_label.pack()
        else:
            self.destroy()

    def cansel(self):
        self.destroy()
