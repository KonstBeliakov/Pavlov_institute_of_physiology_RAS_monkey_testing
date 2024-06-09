import utils
from monkey_windows.monkey_window import MonkeyWindow


class CanvasObject:
    def __init__(self, canvas, x, y, size, texture_file_name):
        self.x = x
        self.y = y
        self.canvas = canvas
        self.texture = utils.open_image(texture_file_name, size)
        self.object = self.canvas.create_image(x, y, image=self.texture)

    def move(self, dx, dy):
        self.x += dx
        self.x += dy
        self.canvas.move(self.object, dx, dy)

    def set_pos(self, x, y):
        self.canvas.move(self.object, x - self.x, y - self.y)
        self.x = x
        self.y = y

    def hide(self):
        self.canvas.itemconfig(self.object, state='hidden')

    def show(self):
        self.canvas.itemconfig(self.object, state='normal')

    def bind(self, event, function):
        self.canvas.tag_bind(self.object, event, function)

    def pos(self):
        return self.x, self.y  # self.canvas.coords(object)


if __name__ == '__main__':
    window = MonkeyWindow()
    window.mainloop()
