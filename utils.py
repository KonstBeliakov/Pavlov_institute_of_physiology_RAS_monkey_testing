import time

from PIL import Image
from PIL.ImageTk import PhotoImage

import pygame
import serial
import threading

from settings import settings

pygame.init()
serial_available = False
ser = None


def check_serial():
    global ser, serial_available
    try:
        if ser is not None:
            ser.close()
        ser = serial.Serial(settings['port'], settings['baudrate'])
        serial_available = True
    except Exception as e:
        print(e)
        serial_available = False
    print(f'serial_available: {serial_available}')
    return serial_available


def open_image(filename: str, image_size: int):
    return PhotoImage(Image.open(filename).resize((image_size, image_size)))


def entry_value_check(value, name, declension=1, min_value=None, max_value=None, value_type=int, may_be_empty=False):
    if not value:
        if may_be_empty:
            return None
        return f'{name} не указан{["", "о", "а"][declension]}'
    try:
        if value_type == int:
            int(value)
        elif value_type == float:
            float(value)
    except:
        d = {int: 'целым', float: 'вещественным'}
        return f'{name} долж{["ен", "но", "на"][declension]} быть {d[value_type]} числом'
    if min_value is not None and min_value > value_type(value):
        return f'{name} не может быть меньше {min_value}'
    if max_value is not None and max_value < value_type(value):
        return f'{name} не может быть больше {max_value}'


def right_answer():
    if settings['using_sound'] and settings['right_answer_sound']:
        play_sound(settings['right_answer_sound'])
    positive_reinforcement()


def wrong_answer():
    if settings['using_sound'] and settings['wrong_answer_sound']:
        play_sound(settings['wrong_answer_sound'])


def experiment_start():
    if settings['using_sound'] and settings['experiment_start_sound']:
        play_sound(settings['experiment_start_sound'])


def play_sound(sound):
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play(0)


def positive_reinforcement():
    if serial_available:
        ser.write(bytes([1]))


def disable_anser_entry():
    if serial_available:
        ser.write(bytes([2]))


def anable_answer_entry():
    if serial_available:
        ser.write(bytes([4]))


def read_usb():
    while True:
        if serial_available:
            print(f'received usb message: {ser.readline()}')
        else:
            print('serial is not available')
        time.sleep(.1)


check_serial()

if __name__ == '__main__':
    t1 = threading.Thread(target=read_usb, daemon=True)
    t1.start()

    time.sleep(1)
    disable_anser_entry()
    time.sleep(1)
    anable_answer_entry()
    time.sleep(1)
    disable_anser_entry()
    time.sleep(1)
    anable_answer_entry()
    time.sleep(1)

    print('end')
    ser.close()
