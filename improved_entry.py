import tkinter as tk

import settings
from utils import entry_value_check


class ImprovedEntry(tk.Entry):
    def __init__(self, screen, x: int, y: int, text: str, value=None, value_type=int, min_value=None, max_value=None,
                 save_value=None):
        super().__init__(screen)

        if value is None:
            save_value = save_value.strip()
            if '[' in save_value:
                index = save_value.find('[')
                num = int(save_value[index + 1: -1])
                value = str(settings.settings[save_value[:index]][num])
            else:
                value = str(settings.settings[save_value])
        self.insert(0, value)

        self.grid(row=y, column=x + 1)

        self.label = tk.Label(screen, text=text)
        self.label.grid(row=y, column=x)

        self.value_type = value_type
        self.min_value = min_value
        self.max_value = max_value

        self.save_to = save_value

    def check_value(self):
        return entry_value_check(self.get(), self.label['text'], min_value=self.min_value, max_value=self.max_value,
                                 value_type=self.value_type)

    def save_value(self):
        value = self.value_type(self.get())
        if self.save_to is not None:
            self.save_to = self.save_to.strip()
            if '[' in self.save_to:
                index = self.save_to.find('[')
                num = int(self.save_to[index + 1: -1])
                settings.settings[self.save_to[:index]][num] = value
            else:
                settings.settings[self.save_to] = value


def f(s):
    i = s.find('[')
    return s[:i], int(s[i:-1])


if __name__ == '__main__':
    print(f('a[0]'))
    print(f('aaa[11]'))