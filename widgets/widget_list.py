from widgets.improved_entry import ImprovedEntry
from widgets.improved_radiobuttons import ImprovedRadiobuttons
from widgets.improved_checkbuttons import ImprovedCheckbuttons
from tkinter import Frame


class WidgetList:
    def __init__(self, screen, x, y, widget_params, vertical=False):
        self.frame = Frame(screen)
        self.frame.grid(row=y, column=x)
        self.widgets = []
        for i, params in enumerate(widget_params):
            if 'widget_type' in params:
                widget_type = params['widget_type']
                del params['widget_type']
            else:
                widget_type = 'entry'

            if vertical:
                x = 2 * i
                y = 0
            else:
                x = 0
                y = i

            if widget_type == 'radiobutton':
                self.widgets.append(ImprovedRadiobuttons(screen=self.frame, x=x, y=y, **params))
            elif widget_type == 'checkbutton':
                self.widgets.append(ImprovedCheckbuttons(screen=self.frame, x=x, y=y, **params))
            else:
                self.widgets.append(ImprovedEntry(screen=self.frame, x=x, y=y, **params))

    def check_values(self, show_error=False):
        error_text = ''
        for widget in self.widgets:
            if isinstance(widget, ImprovedEntry):
                if (t := widget.check_value()) is not None:
                    if show_error:
                        widget.configure(fg='red')
                    error_text += f'{t}\n'
                else:
                    widget.configure(fg='black')
        return None if not error_text else error_text

    def save_values(self, check_validity=True):
        if check_validity and (t := self.check_values(show_error=True)) is not None:
            return t

        for widget in self.widgets:
            widget.save_value()
