import datetime
from datetime import datetime
import time
import tkinter.messagebox as mb

import threading
from random import sample, shuffle, choice
import os
from monkey_windows.monkey_window import MonkeyWindow
from settings import settings
import utils
from widgets.canvas_object import CanvasObject


def generate_experiment_params():
    exp_num = settings['session_number'] * settings['repeat_number']  # number of experiments
    delays = [settings['delay'][1][i % len(settings['delay'][1])] for i in range(exp_num)]

    if settings['mix_delays']:
        shuffle(delays)

    if settings['equalize_correct_answers_by_delays']:
        d = {}
        for delay in delays:
            d[delay] = d.get(delay, 0) + 1

        d2 = {}  # dictionary for counting the number of the current delay of each type
        answers = {}  # dict of lists of answers for each delay
        for delay in delays:
            t = (d[delay] * settings['correct_answers_percentage'] // 100)
            answers[delay] = [False] * t + [True] * (d[delay] - t)
            shuffle(answers[delay])

        exp = []  # list of params of every experiment
        for delay in delays:
            exp.append({'delay': delay, 'answer': answers[delay][d2.get(delay, 0)]})
            d2[delay] = d2.get(delay, 0) + 1
    else:
        # number of responses in the first window
        r1 = settings['correct_answers_percentage'] * exp_num // 100

        answers = [False] * r1 + [True] * (exp_num - r1)
        shuffle(answers)

        exp = [{'delay': delay, 'answer': answer} for delay, answer in zip(delays, answers)]

    return exp


class MonkeyWindow1(MonkeyWindow):
    def __init__(self):
        super().__init__()
        self.test_start = time.perf_counter()
        self.experiment_type = 1
        self.experiment_number = 0

        self.log = []

        self.pressed = False

        self.protocol("WM_DELETE_WINDOW", self.confirm_delete)

        self.t1 = threading.Thread(target=self.update)
        self.t1.start()

    def confirm_delete(self):
        message = "Вы уверены, что хотите закрыть это окно?"
        if mb.askyesno(message=message, parent=self):
            self.destroy()

    def write_log(self, answer):
        self.log.append({
            'Номер': self.experiment_number,
            'Время с начала эксперимента': round(time.perf_counter() - settings['experiment_start'], 3),
            'Время реакции': None if answer is None else round(time.perf_counter() - self.test_start, 3),
            'Ответ': answer,
            'Правильный ответ': self.new_image_number if settings['right_image'] == 'Старое изображение' else self.old_image_number,
            'Файл 1': self.img1_name,
            'Файл 2': self.img2_name,
            'Дата': datetime.now().date(),
            'Время': datetime.now().time(),
            'Ответ справа': int(answer == 1),
            'Ответ слева': int(answer == 0),
            'Текущая отсрочка': self.exp_params[self.experiment_number]['delay'],
            'Предыдущая отсрочка': None if self.experiment_number == 0 else self.exp_params[self.experiment_number - 1]['delay'],
            'Правильным считается': settings['right_image'],
            'Отказ от ответа': int(answer is None),
            'Файл настроек эксперимента': settings['settings_file_name']
        })

    def image_pressed(self, number):
        if not self.pressed:
            self.write_log(number)

            if settings['right_image'] == 'Старое изображение':
                if number == self.new_image_number:
                    utils.right_answer()
                else:
                    utils.wrong_answer()
            else:
                if number == self.old_image_number:
                    utils.right_answer()
                else:
                    utils.wrong_answer()

        self.pressed = True

    def update(self):
        utils.disable_anser_entry()
        self.exp_params = generate_experiment_params()

        for i in range(settings['session_number']):
            for j in range(settings['repeat_number']):
                if settings['image_selection_method'] == 'Случайный':
                    directory = "images_random"
                    files = os.listdir(directory)
                    self.img1_name, self.img2_name = sample(files, 2)
                else:
                    directory = "image_pairs"
                    files = os.listdir(directory)
                    self.img1_name = choice([i for i in files if 'A' in i])
                    self.img2_name = self.img1_name.replace('A', 'B')

                image_numbers = [self.img1_name, self.img2_name]

                screen_center_pos = [self.canvas_size[0] // 2, self.canvas_size[1] // 2]
                dx = (self.canvas_size[0] - settings['image_size'] * 2 - settings['distance_between_images']) // 2
                pos = [[dx + settings['image_size'] // 2, self.canvas_size[1] // 2],
                       [dx + settings['image_size'] * 1.5 + settings['distance_between_images'],
                        self.canvas_size[1] // 2]
                       ]
                self.objects = [CanvasObject(self.canvas, 0, 0, settings['image_size'],
                                             f'{directory}/{image_numbers[i]}') for i in range(2)]

                self.new_image_number = int(self.exp_params[self.experiment_number]['answer'])
                self.old_image_number = int(not self.exp_params[self.experiment_number]['answer'])

                if settings['display_target_image_twice']:
                    self.objects[self.new_image_number].set_pos(*pos[0])
                    self.old_image_copy = CanvasObject(self.canvas, *pos[1], settings['image_size'],
                                                         f'{directory}/{image_numbers[self.new_image_number]}')
                else:
                    self.objects[self.new_image_number].set_pos(*screen_center_pos)
                self.objects[self.new_image_number].show()
                self.objects[self.old_image_number].hide()

                time.sleep(settings['delay'][0])

                # both images are hidden
                if settings['display_target_image_twice']:
                    self.old_image_copy.hide()
                self.objects[self.new_image_number].hide()

                time.sleep(self.exp_params[self.experiment_number - 1]['delay'])

                # both images shows up and it's time for answering
                utils.anable_answer_entry()

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
                    self.write_log(None)

                self.pressed = False

                self.objects[0].hide()
                self.objects[1].hide()

                utils.disable_anser_entry()

                # both images are hidden again
                time.sleep(settings['delay'][3])

                self.experiment_number += 1
        time.sleep(settings['delay'][4])


if __name__ == '__main__':
    directory = '../images_random'
    temp_image_file = '../pictograms/settings.png'
    settings['experiment_start'] = time.perf_counter()
    files = os.listdir(directory)
    window = MonkeyWindow1()
    window.mainloop()
else:
    directory = "images_random"
    temp_image_file = 'pictograms/settings.png'
    files = os.listdir(directory)
