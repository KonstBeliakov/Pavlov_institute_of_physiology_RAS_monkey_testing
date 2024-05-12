import tkinter as tk
from utils import entry_value_check


class ImprovedEntry(tk.Entry):
    def __init__(self, screen, x: int, y: int, text: str, value: str, value_type=int, min_value=None, max_value=None):
        super().__init__(screen)
        self.insert(0, value)
        self.grid(row=y, column=x + 1)

        self.label = tk.Label(screen, text=text)
        self.label.grid(row=y, column=x)

        self.value_type = value_type
        self.min_value = min_value
        self.max_value = max_value

    def check_value(self):
        return entry_value_check(self.get(), self.label['text'], min_value=self.min_value, max_value=self.max_value,
                                 value_type=self.value_type)
