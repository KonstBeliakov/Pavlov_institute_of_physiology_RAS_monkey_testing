from customtkinter import *
import settings
from utils import entry_value_check
from dateutil import parser


class ImprovedEntry(CTkEntry):
    def __init__(self, screen, x: int, y: int, text: str, value=None, value_type=int, min_value=None, max_value=None,
                 save_value=None, may_be_empty=False):
        super().__init__(screen)

        self.may_be_empty = may_be_empty

        if value is None:
            save_value = save_value.strip()
            if '[' in save_value:
                index = save_value.find('[')
                num = int(save_value[index + 1: -1])
                value = settings.settings[save_value[:index]][num]
            else:
                value = settings.settings[save_value]
        self.set_value(value)

        self.grid(row=y, column=x + 1, padx=5, pady=2)

        self.text = text
        self.label = CTkLabel(screen, text=self.text)
        self.label.grid(row=y, column=x, padx=5, pady=2)

        self.value_type = value_type
        self.min_value = min_value
        self.max_value = max_value

        self.save_to = save_value

    def check_value(self):
        return entry_value_check(self.get(), self.text, min_value=self.min_value, max_value=self.max_value,
                                 value_type=self.value_type, may_be_empty=self.may_be_empty)

    def save_value(self):
        if self.value_type == bool:
            value = self.get().strip() in ['Да', 'y', 'yes', 'Yes', 'True', 'true', 't', '1', 'YES']
        elif self.value_type == 'date':
            if self.may_be_empty and not self.get().strip():
                value = ''
            else:
                value = parser.parse(self.get().strip()).date()
        elif self.value_type == 'list float':
            value = [float(i) for i in self.get().split()]
        else:
            value = self.value_type(self.get())

        if self.save_to is not None:
            self.save_to = self.save_to.strip()
            if '[' in self.save_to:
                index = self.save_to.find('[')
                num = int(self.save_to[index + 1: -1])
                settings.settings[self.save_to[:index]][num] = value
            else:
                settings.settings[self.save_to] = value

    def set_value(self, value):
        self.delete(0, END)
        if isinstance(value, list):
            self.insert(0, ' '.join([str(i) for i in value]))
        else:
            self.insert(0, str(value))
