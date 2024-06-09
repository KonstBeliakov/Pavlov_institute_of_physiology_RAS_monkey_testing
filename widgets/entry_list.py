from widgets.improved_entry import ImprovedEntry
from tkinter import Frame


class EntryList:
    def __init__(self, screen, x, y, entries_params):
        self.frame = Frame(screen)
        self.frame.grid(row=y, column=x)
        self.entries = [ImprovedEntry(screen=self.frame, x=0, y=i, **params) for i, params in enumerate(entries_params)]

    def check_values(self, show_error=False):
        error_text = ''
        for entry in self.entries:
            if (t := entry.check_value()) is not None:
                if show_error:
                    entry.configure(fg='red')
                error_text += f'{t}\n'
            else:
                entry.configure(fg='black')
        return None if not error_text else error_text

    def save_values(self, check_validity=True):
        if check_validity and (t := self.check_values(show_error=True)) is not None:
            return t

        for entry in self.entries:
            entry.save_value()
