import time
import tkinter as tk
import settings
import threading


class MonkeyWindow(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.canvas_size = [500, 500]
        self.canvas = tk.Canvas(self, bg="white", width=self.canvas_size[0], height=self.canvas_size[1])
        self.canvas.pack(anchor=tk.CENTER, expand=1)

        self.canvas.bind("<Button-1>", self.canvas_pressed)

    def hide(self, click_circle):
        time.sleep(settings.click_circle_time)
        self.canvas.itemconfig(click_circle, state='hidden')

    def canvas_pressed(self, event):
        center = (event.x, event.y)
        radius = settings.mouse_click_circle_radius
        click_circle = self.canvas.create_oval(center[0] - radius, center[1] - radius,
                                center[0] + radius, center[1] + radius, width=5, outline='#f00', fill='')
        self.canvas.itemconfig(click_circle, state='normal')
        t1 = threading.Thread(target=lambda: self.hide(click_circle))
        t1.start()


if __name__ == '__main__':
    window = MonkeyWindow()
    window.mainloop()