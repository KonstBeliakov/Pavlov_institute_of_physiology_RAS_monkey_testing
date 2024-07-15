from customtkinter import *
from settings import settings


class ImprovedRadiobuttons:
    def __init__(self, screen, x: int, y: int, text, values=('Да', 'Нет'), value_type=int, save_value=None):
        self.label = CTkLabel(screen, text=text)
        self.label.grid(row=y, column=x)

        self.values = values

        self.variable = StringVar(screen, '')
        self.variable.set(values[0])
        self.radio_button_values = [CTkRadioButton(screen, text=values[i], variable=self.variable, value=values[i])
                                    for i in range(len(values))]

        for i in range(len(values)):
            self.radio_button_values[i].grid(row=y, column=x + i + 1)

        self.value_type = value_type
        self.save_to = save_value

        if save_value is not None:
            print(save_value, settings[save_value], self.values)
            self.set_value(settings[save_value])

    def check_value(self):
        pass

    def save_value(self):
        if self.save_to is not None:
            if self.value_type == bool:
                settings[self.save_to] = self.variable.get().strip() in ['Да', 'да', 'y', 'yes', 'Yes', 'True', 'true', 't', '1', 'YES']
            else:
                settings[self.save_to] = self.value_type(self.variable.get())

    def get(self):
        return self.variable.get()

    def set_value(self, value):
        if self.value_type == bool:
            if value:
                self.variable.set('Да')
            else:
                self.variable.set('Нет')
        else:
            if str(value) in self.values:
                self.variable.set(str(value))
            else:
                raise ValueError
