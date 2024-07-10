from tkinter import *
from settings import settings


class ImprovedCheckbuttons:
    def __init__(self, screen, x: int, y: int, text: str, values: list, value_type=int, save_value=None, values_in_row=None):
        self.label = Label(screen, text=text)
        self.label.grid(row=y, column=x)

        self.values = values

        self.variables = [IntVar() for _ in range(len(values))]
        self.checkbuttons = [Checkbutton(screen, text=values[i], variable=self.variables[i], command=self.selected)
                             for i in range(len(values))]

        if values_in_row is None:
            values_in_row = len(values)

        for i in range(len(values)):
            self.checkbuttons[i].grid(row=y + i // values_in_row, column=x + i % values_in_row + 1)

        self.value_type = value_type
        self.save_to = save_value

        if save_value is not None and isinstance(settings[save_value], list):
            self.set_value(settings[save_value])

    def check_value(self):
        pass

    def save_value(self):
        if self.save_to is not None:
            settings[self.save_to] = self.get()
            print(settings[self.save_to])

    def get(self):
        s = []
        for i, var in enumerate(self.variables):
            if var.get():
                s.append(self.value_type(self.values[i]))
        return s

    def set_value(self, values):
        for var in self.variables:
            var.set(0)

        for value in values:
            if str(value) in self.values:
                index = self.values.index(str(value))
                self.variables[index].set(1)
            else:
                raise ValueError

    def selected(self):
        pass


if __name__ == '__main__':
    root = Tk()
    checkbutton = ImprovedCheckbuttons(root, 0, 0, 'checkbutton', values=['1', '2', '3'], value_type=int, save_value='test')

    checkbutton.set_value([1, 3])
    print(checkbutton.get())  # [1, 3]

    button = Button(root, text='save_value', command=checkbutton.save_value)
    button.grid(row=1, column=0)

    root.mainloop()
