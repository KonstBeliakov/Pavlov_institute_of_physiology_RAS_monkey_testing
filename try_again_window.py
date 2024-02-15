
import tkinter as tk


class TryAgainWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.title('Ошибка')
        self.geometry('600x120')

        self.label = tk.Label(self, text='При сохранении данных эксперимента произошла ошибка.\n'
                                         'Скоре всего название файла было написано не правильно (или не было указано).\n'
                                         'Для того чтобы сохранение прошло успешно, файл должен иметь расширение .xlsx')
        self.label.pack()
        self.frame = tk.Frame(self)
        self.frame.pack()

        self.label2 = tk.Label(self.frame, text='Введите название файла записи данных эксперимента')
        self.entry = tk.Entry(self.frame)
        self.button_confirm = tk.Button(self.frame, text='Сохранить', command=self.confirm)
        self.button_cansel = tk.Button(self.frame, text='Не сохранять данные эксперимента', command=self.cansel)

        self.label2.grid(row=0, column=0)
        self.entry.grid(row=0, column=1)
        self.button_confirm.grid(row=1, column=0)
        self.button_cansel.grid(row=1, column=1)

    def confirm(self):
        print('saving...', end='')
        self.parent.save_experiment_data(self.entry.get())
        print('done')
        self.destroy()

    def cansel(self):
        self.destroy()
