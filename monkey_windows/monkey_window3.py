import random
from datetime import datetime
import threading
from time import perf_counter, sleep
import os
from settings import settings, APPLICATION_RUNNING
import utils
from monkey_windows.monkey_window import MonkeyWindow
from widgets.canvas_object import CanvasObject


directory = "images_random"
files = os.listdir(directory)  # images name list


class MonkeyWindow3(MonkeyWindow):
    def __init__(self):
        super().__init__()
        self.experiment_type = 3
        self.experiment_number = 0

        self.test_start = None
        self.title('Experiment window')
        self.log = []
        self.experiment_number = 1

        self.stop = False

        t1 = threading.Thread(target=self.update)
        t1.start()

    def update(self):
        while APPLICATION_RUNNING:
            table_size_x = min(int(self.canvas_size[0] // settings['image_size3']), settings['grid_size'][0])
            table_size_y = min(int(self.canvas_size[1] // settings['image_size3']), settings['grid_size'][1])

            dx = (self.canvas_size[0] - table_size_x * settings['image_size3']) // (table_size_x - 1)
            dy = (self.canvas_size[1] - table_size_y * settings['image_size3']) // (table_size_y - 1)

            self.image_numbers = random.sample(list(range(len(files))), settings['max_image_number'])

            self.stop = False
            self.image_number = settings['min_image_number']

            while self.image_number < settings['max_image_number'] + 1:
                self.image_number += 1
                self.image_position = random.sample(
                    list([(i, j) for i in range(table_size_x) for j in range(table_size_y)]),
                    self.image_number)

                if settings['shuffle_images']:
                    self.image_position2 = random.sample(
                        list([(i, j) for i in range(table_size_x) for j in range(table_size_y)]),
                        self.image_number)
                else:
                    self.image_position2 = self.image_position

                self.objects = [CanvasObject(self.canvas,
                                             settings['image_size3'] // 2 + self.image_position[i][0] * (settings['image_size3'] + dx),
                                             settings['image_size3'] // 2 + self.image_position[i][1] * (settings['image_size3'] + dy),
                                             settings['image_size3'], f'{directory}/{files[self.image_numbers[i]]}')
                                for i in range(self.image_number)]

                self.objects[-1].hide()

                sleep(settings['delay3'][0])

                for obj in self.objects:
                    obj.hide()

                sleep(settings['delay3'][1])

                for obj in self.objects:
                    obj.show()

                self.pressed = False
                self.bind()

                for i, obj in enumerate(self.objects):
                    obj.move((self.image_position2[i][0] - self.image_position[i][0]) * (settings['image_size3'] + dx),
                             (self.image_position2[i][1] - self.image_position[i][1]) * (settings['image_size3'] + dy))

                self.test_start = perf_counter()

                while (perf_counter() - self.test_start) < settings['delay3'][2]:
                    sleep(0.1)
                    if self.stop:
                        break
                if self.stop:
                    break

                if not self.pressed:
                    self.log.append([self.experiment_number, round(perf_counter() - settings['experiment_start'], 3),
                                     None, None, self.image_number])

                for obj in self.objects:
                    obj.hide()

                sleep(settings['delay3'][3])

            self.experiment_number += 1

    def bind_image(self, x):
        self.objects[x].bind('<Button-1>', lambda event: self.image_pressed(x))

    def bind(self):
        for i in range(len(self.objects)):
            self.bind_image(i)

    def write_log(self, answer):
        self.log.append({
            'Номер': self.experiment_number,
            'Время с начала эксперимента': round(perf_counter() - settings['experiment_start'], 3),
            'Время реакции': round(perf_counter() - self.test_start, 3),
            'Ответ': answer,
            'Правильный ответ': len(self.objects) - 1,
            'Файлы': [f'{directory}/{files[self.image_numbers[i]]}' for i in range(self.image_number)],
            'Дата': datetime.now().date(),
            'Время': datetime.now().time(),
            'Текущая отсрочка': settings['delay3'][1],
            'Предыдущая отсрочка': None if self.experiment_number == 1 else settings['delay3'][1],
            'Отказ от ответа': int(answer is None),
            'Файл настроек эксперимента': settings['settings_file_name'][3]
        })

    def image_pressed(self, number):
        self.write_log(number)

        self.pressed = True

        if settings['stop_after_error'] and (number != len(self.objects) - 1):
            self.stop = True
            print(number, len(self.objects) - 1, 'stopped')

        if number == len(self.objects) - 1:
            utils.right_answer()
        else:
            utils.wrong_answer()


if __name__ == '__main__':
    window = MonkeyWindow3()
    window.mainloop()
