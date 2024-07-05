settings = {
    'test': None,

    'bg_color': '#fff',
    'monitor_copy_size': 0.05,

    # saving experiment data params
    'experiment_data_filename': '',
    'selected_period_start': '',
    'selected_period_end': '',

    # arduino params
    'port': 'COM3',
    'baudrate': 9600,

    # sounds
    'using_sound': True,
    'experiment_start_sound': 'sounds/start.mp3',
    'right_answer_sound': 'sounds/right_answer_sound.mp3',
    'wrong_answer_sound': 'sounds/wrong_answer_sound.wav',

    # click parametres
    'mouse_click_circle_radius': 20,
    'click_circle_color': '#f00',
    'click_circle_width': 5,
    'click_circle_time': 1.0,

    # First type experiment settings
    'delay': [1.0, [1.0], 1.0, 0.0, 5.0],
    'session_number': 1,
    'repeat_number': 5,
    'experiment_start': None,
    'restart_after_answer': False,
    'image_size': 100,
    'distance_between_images': 100,
    'same_images': False,
    'display_target_image_twice': False,
    'mix_delays': False,
    'correct_answers_percentage': 50,
    'image_selection_method': 'Случайный',
    'equalize_correct_answers_by_delays': False,
    'right_image': 'Старое изображение',
    'log_header1': ['Номер', 'Время с начала эксперимента', 'Время реакции', 'Ответ', 'Правильный ответ', 'Файл 1',
                    'Файл 2', 'Дата', 'Время', 'Ответ справа', 'Ответ слева', 'Текущая отсрочка', 'Предыдущая отсрочка',
                    'Правильным считается', 'Отказ от ответа', 'Файл настроек эксперимента'],
    'current_log_header1': None,

    # Second type experiment settings
    'image_min_speed': 50,
    'image_max_speed': 75,
    'barrier_width': 100,
    'barrier_color': 'red',
    'barrier_dist': 150,
    'image_number': 5,
    'session_delay2': 1.0,
    'straight_movement': True,
    'repeat_number2': 3,
    'image_size2': 100,
    'exp2_filename': 'pictograms/no.png',
    'movement_direction': None,
    'log_header2': ['Номер', 'Время с начала эксперимента', 'Время реакции', 'Ответ', 'Правильный ответ', 'Файл',
                    'Дата', 'Время', 'Отказ от ответа', 'Файл настроек эксперимента'],
    'current_log_header2': None,

    # Experiment 3 settings
    'min_image_number': 2,
    'max_image_number': 4,
    'shuffle_images': True,
    'image_size3': 128,
    'delay3': [1.0, 1.0, 1.0, 0.5],
    'stop_after_error': True,
    'grid_size': [5, 5],
    'log_header3': ['Номер', 'Время с начала эксперимента', 'Время реакции', 'Ответ', 'Правильный ответ', 'Файлы',
                    'Дата', 'Время', 'Текущая отсрочка', 'Предыдущая отсрочка', 'Отказ от ответа',
                    'Файл настроек эксперимента'],
    'current_log_header3': None,

    # Settings
    'settings_file_name': [None, None, None, None],
}
