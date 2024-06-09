import time
import tkinter.messagebox as mb

import threading
from random import sample, randrange
import os
from monkey_windows.monkey_window import MonkeyWindow
from settings import settings
import utils
from widgets.canvas_object import CanvasObject


class MonkeyWindow1(MonkeyWindow):
    def __init__(self):
        super().__init__()
        self.pressed = False
        self.log = [['Номер', 'Абсолютное время', 'Время на ответ', 'Ответ', 'Правильный ответ']]
        self.experiment_number = 1

        self.protocol("WM_DELETE_WINDOW", self.confirm_delete)

        self.t1 = threading.Thread(target=self.update)
        self.t1.start()

    def confirm_delete(self):
        message = "Вы уверены, что хотите закрыть это окно?"
        if mb.askyesno(message=message, parent=self):
            self.destroy()

    def image_pressed(self, number):
        if not self.pressed:
            self.log.append([self.experiment_number, round(time.perf_counter() - settings['experiment_start'], 3),
                             round(time.perf_counter() - self.test_start, 3),
                             number, self.right_number])
            if number == self.right_number:
                utils.right_answer()
            else:
                utils.wrong_answer()
        self.pressed = True

    def update(self):
        for i in range(settings['session_number']):
            for j in range(settings['repeat_number']):
                image_numbers = sample(files, 2)
                start_position = [self.canvas_size[0] // 2, self.canvas_size[1] // 2]
                self.objects = [CanvasObject(self.canvas, 100 + 100 * i, 100, settings['image_size'],
                                             f'{directory}/{image_numbers[i]}') for i in range(2)]
                self.right_number, self.wrong_number = [(t := randrange(2)), int(not t)]

                self.objects[self.right_number].set_pos(*start_position)
                self.objects[self.right_number].show()
                self.objects[self.wrong_number].hide()

                time.sleep(settings['delay'][0])

                # both images are hidden
                self.objects[self.right_number].hide()

                time.sleep(settings['delay'][1][(self.experiment_number - 1) % len(settings['delay'][1])])

                # both images shows up and it's time for answering
                dx = (self.canvas_size[0] - settings['image_size'] * 2 - settings['distance_between_images']) // 2
                pos = [[dx + settings['image_size'] // 2, self.canvas_size[1] // 2],
                       [dx + settings['image_size'] * 1.5 + settings['distance_between_images'], self.canvas_size[1] // 2]
                       ]

                self.objects[0].set_pos(*pos[0])
                self.objects[1].set_pos(*pos[1])

                self.objects[0].show()
                self.objects[1].show()

                self.objects[0].bind('<Button-1>', lambda event: self.image_pressed(0))
                self.objects[1].bind('<Button-1>', lambda event: self.image_pressed(1))

                self.test_start = time.perf_counter()

                while time.perf_counter() - self.test_start < settings['delay'][2]:
                    if self.pressed and settings['restart_after_answer']:
                        break
                    time.sleep(0.05)

                if not self.pressed:
                    self.log.append([self.experiment_number, round(time.perf_counter() - settings['experiment_start'], 3),
                                     None, None, self.right_number])
                self.pressed = False

                self.objects[0].hide()
                self.objects[1].hide()

                time.sleep(settings['delay'][3])
                # both images are hidden again

                self.experiment_number += 1
        time.sleep(settings['delay'][4])


if __name__ == '__main__':
    directory = '../images'
    temp_image_file = '../pictograms/settings.png'
    settings['experiment_start'] = time.perf_counter()
    files = os.listdir(directory)
    window = MonkeyWindow1()
    window.mainloop()
else:
    directory = "images"
    temp_image_file = 'pictograms/settings.png'
    files = os.listdir(directory)
