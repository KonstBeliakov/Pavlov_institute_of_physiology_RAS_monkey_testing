import time
import tkinter as tk
from settings import settings
import threading
from screeninfo import get_monitors


class MonkeyWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.experiment_type = None
        self.canvas_size = [self.winfo_screenwidth() // 1.1, self.winfo_screenheight() // 1.1]
        self.canvas = tk.Canvas(self, bg=settings['bg_color'], width=self.canvas_size[0], height=self.canvas_size[1])
        self.canvas.pack(anchor=tk.CENTER, expand=1)

        monitors = get_monitors()
        if len(monitors) >= 2 and settings['fullscreen_mode']:
            if settings['screen_size']:
                self.geometry(settings['screen_size'])
            else:
                self.geometry(f'{monitors[1].width}x{monitors[1].height}')
        self.overrideredirect(True)

        self.canvas.bind("<Button-1>", self.canvas_pressed)

    def hide(self, click_circle):
        time.sleep(settings['click_circle_time'])
        self.canvas.itemconfig(click_circle, state='hidden')

    def canvas_pressed(self, event):
        center = (event.x, event.y)
        radius = settings['mouse_click_circle_radius']
        click_circle = self.canvas.create_oval(center[0] - radius, center[1] - radius,
                                               center[0] + radius, center[1] + radius,
                                               width=settings['click_circle_width'],
                                               outline=settings['click_circle_color'], fill='')
        self.canvas.itemconfig(click_circle, state='normal')
        t1 = threading.Thread(target=lambda: self.hide(click_circle))
        t1.start()


if __name__ == '__main__':
    window = MonkeyWindow()
    window.mainloop()
