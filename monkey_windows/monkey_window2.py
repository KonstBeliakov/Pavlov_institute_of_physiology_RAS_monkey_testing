from datetime import datetime
import threading
from time import sleep, perf_counter
from tkinter import *
from settings import settings

from random import randint, randrange
import utils
from monkey_windows.monkey_window import MonkeyWindow
from widgets.canvas_object import CanvasObject


class MonkeyWindow2(MonkeyWindow):
    def __init__(self):
        super().__init__()
        self.experiment_number = 0
        self.experiment_type = 2

        self.log = []

        self.title('Experiment window')

        self.image_speed = randint(settings['image_min_speed'], settings['image_max_speed'])

        self.image_size = settings['image_size2']
        t = (self.canvas_size[1] - settings['image_number'] * self.image_size) // (settings['image_number'] + 1)
        x_pos = (self.canvas_size[0] - settings['barrier_width']) // 2 - self.image_size - settings['barrier_dist']
        self.image_position = [[x_pos, t * (i + 1) + self.image_size * i] for i in range(settings['image_number'])]

        try:
            self.filename = settings['exp2_filename']
            self.python_image = utils.open_image(self.filename, settings['image_size2'])
        except FileNotFoundError:
            self.filename = 'pictograms/no.png'
            self.python_image = utils.open_image(self.filename, settings['image_size2'])

        if settings['movement_direction'] == 'Справа налево':
            self.objects = [CanvasObject(self.canvas, self.canvas_size[0] - self.image_position[i][0],
                                         self.canvas_size[1] - self.image_position[i][1], self.image_size, self.filename,
                                         speedX=-self.image_speed) for i in range(settings['image_number'])]
        else:
            self.objects = [CanvasObject(self.canvas, *self.image_position[i], self.image_size, self.filename,
                                         speedX=self.image_speed) for i in range(settings['image_number'])]

        self.right_image = randrange(settings['image_number'])

        for obj in self.objects:
            obj.hide()
        self.objects[self.right_image].show()

        self.test_start = perf_counter()
        self.pressed = False

        self.bind()

        self.barrier = self.canvas.create_rectangle((self.canvas_size[0] - settings['barrier_width']) // 2, 0,
                                                    settings['barrier_width'] + (
                                                            self.canvas_size[0] - settings['barrier_width']) // 2,
                                                    self.canvas_size[1], fill=settings['barrier_color'])

        self.t1 = threading.Thread(target=self.update)
        self.t1.start()

    def write_log(self, answer):
        self.log.append({
            'Номер': self.experiment_number,
            'Время с начала эксперимента': round(perf_counter() - settings['experiment_start'], 3),
            'Время реакции': None if answer is None else round(perf_counter() - self.test_start, 3),
            'Ответ': answer,
            'Правильный ответ': self.right_image,
            'Файл': self.filename,
            'Дата': datetime.now().date(),
            'Время': datetime.now().time(),
            'Отказ от ответа': int(answer is None),
            'Файл настроек эксперимента': settings['settings_file_name'][2]
        })

    def object_click_event(self, answer: int):
        self.write_log(answer)

        if answer == self.right_image:
            utils.right_answer()
        else:
            utils.wrong_answer()
        self.pressed = True

    def update(self):
        for i in range(settings['repeat_number2']):
            self.experiment_number += 1
            next_experiment = False
            while not next_experiment:
                next_experiment = True
                for j, obj in enumerate(self.objects):
                    obj.update()

                    # if image is behind the barrier
                    if settings['movement_direction'] == 'Справа налево':
                        if self.objects[j].x + self.image_size // 2 < (self.canvas_size[0] + settings['barrier_width']) // 2:
                            obj.show()
                    else:  # moving from left to right
                        if self.objects[j].x - self.image_size // 2 > (self.canvas_size[0] - settings['barrier_width']) // 2:
                            obj.show()

                    # check that the image goes beyond the screen
                    if not (obj.x + (self.image_size // 2) < 0 or obj.x - (self.image_size // 2) > self.canvas_size[0]):
                        next_experiment = False

                sleep(0.05)

            sleep(settings['session_delay2'])
            self.right_image = randrange(settings['image_number'])

            for i, obj in enumerate(self.objects):
                obj.set_pos(*self.image_position[i])
                obj.hide()

            self.objects[self.right_image].show()
            self.test_start = perf_counter()
            if not self.pressed:
                self.write_log(None)

            self.experiment_number += 1
            self.pressed = False
        self.destroy()

    def bind_image(self, x):
        self.objects[x].bind('<Button-1>', lambda event: self.object_click_event(x))

    def bind(self):
        for i in range(settings['image_number']):
            self.bind_image(i)


if __name__ == '__main__':
    root = Tk()
    root.title('main window')
    window = MonkeyWindow2()
    window.mainloop()
