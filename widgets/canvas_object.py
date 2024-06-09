import utils
from monkey_windows.monkey_window import MonkeyWindow
from time import perf_counter


class CanvasObject:
    def __init__(self, canvas, x: int, y: int, size: int, texture_file_name: str, speedX=0, speedY=0):
        self.x = x
        self.y = y
        self.canvas = canvas
        self.texture = utils.open_image(texture_file_name, size)
        self.object = self.canvas.create_image(x, y, image=self.texture)
        self.speedX = speedX
        self.speedY = speedY
        self.time = perf_counter()

    def move(self, dx: int, dy: int):
        self.x += dx
        self.x += dy
        self.canvas.move(self.object, dx, dy)

    def set_pos(self, x: int, y: int):
        self.canvas.move(self.object, x - self.x, y - self.y)
        self.x = x
        self.y = y

    def hide(self):
        self.canvas.itemconfig(self.object, state='hidden')

    def show(self):
        self.canvas.itemconfig(self.object, state='normal')

    def bind(self, event: str, function):
        self.canvas.tag_bind(self.object, event, function)

    def pos(self):
        return self.x, self.y  # self.canvas.coords(object)

    def update(self):
        dt = perf_counter() - self.time
        self.move(self.speedX * dt, self.speedY * dt)
        self.time = perf_counter()


if __name__ == '__main__':
    window = MonkeyWindow()
    window.mainloop()
