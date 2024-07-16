from customtkinter import CTkLabel


class InfoFrame:
    def __init__(self, root):
        CTkLabel(master=root, text='Документация открылась в браузере').pack()
