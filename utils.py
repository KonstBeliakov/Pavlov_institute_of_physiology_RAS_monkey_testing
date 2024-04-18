import pygame
import settings

pygame.init()


def entry_value_check(value, name, declension=1, min_value=None, max_value=None, value_type=int):
    if not value:
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


def play_wrong_answer_sound():
    pygame.mixer.music.load(settings.wrong_answer_sound)
    pygame.mixer.music.play(0)


def play_right_answer_sound():
    pygame.mixer.music.load(settings.right_answer_sound)
    pygame.mixer.music.play(0)


if __name__ == '__main__':
    play_right_answer_sound()
    __import__('time').sleep(1)