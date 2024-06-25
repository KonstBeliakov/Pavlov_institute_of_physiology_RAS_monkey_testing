from tkhtmlview import HTMLLabel
from tkinter import Button
from os import startfile


class InfoFrame:
    def __init__(self, root):
        self.button = Button(root, text='Открыть документацию в браузере', command=self.open_documentation)
        self.button.pack()

        with open('info_frame_text.html', 'r', encoding='utf-8') as file:
            self.info_label = HTMLLabel(root, html=file.read())
        self.info_label.pack(fill="both", expand=True)

    def open_documentation(self):
        startfile('info_frame_text.html')
