import customtkinter as ctk


from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from settings import settings


class GraphPanel:
    def __init__(self, root, row, column):
        self.root = root

        self.frame = ctk.CTkFrame(root)
        self.frame.grid(row=row, column=column)

        self.figsizes = [(8, 4), (3.5, 4), (3.5, 4), (3.5, 4)]

        self.figures = [plt.Figure(figsize=figsize) for figsize in self.figsizes]
        self.graph_canvases = [FigureCanvasTkAgg(figure, self.frame) for figure in self.figures]

        for i, canvas in enumerate(self.graph_canvases):
            canvas.get_tk_widget().grid(row=0, column=i)

        fontsize = 12

        self.figures[0].suptitle('Кривые ответов', fontsize=fontsize)
        self.figures[1].suptitle('Среднее время ответа', fontsize=fontsize)
        self.figures[2].suptitle('Процент правильных ответов', fontsize=fontsize)
        self.figures[3].suptitle('Процент отказов', fontsize=fontsize)

        self.figure_subplots = [figure.add_subplot() for figure in self.figures]

        self.draw()

    def draw(self):
        for canvas in self.graph_canvases:
            canvas.draw()

    def update(self, data):
        for subplot in self.figure_subplots:
            subplot.clear()

        delays = sorted(settings['delay'][1])

        graph_data = [[0] for _ in range(len(delays))]
        for i, line in enumerate(data):
            index = delays.index(line['Текущая отсрочка'])
            if line['Ответ'] is None:
                graph_data[index].append(graph_data[index][-1])
            elif line['Ответ'] == line['Правильный ответ']:
                graph_data[index].append(graph_data[index][-1] + 1)
            else:
                graph_data[index].append(graph_data[index][-1] - 1)

        graph_number = len(settings['delay'][1])
        for i in range(graph_number):
            self.figure_subplots[0].plot(list(range(len(graph_data[i]))), graph_data[i])
        self.figure_subplots[0].legend([f'Задержка {delay} секунд' for delay in settings['delay'][1]])

        delays = sorted(settings['delay'][1])
        time_sum = {delay: 0 for delay in delays}
        time_num = {delay: 0 for delay in delays}

        for line in data:
            if line['Время реакции'] is not None:
                time_sum[line['Текущая отсрочка']] += line['Время реакции']
                time_num[line['Текущая отсрочка']] += 1

        avg_time = []
        for delay in delays:
            if time_num[delay]:
                avg_time.append(time_sum[delay] / time_num[delay])
            else:
                avg_time.append(0)

        self.figure_subplots[1].plot(delays, avg_time)

        correct_answer_count = {delay: 0 for delay in delays}
        total_answer_count = {delay: 0 for delay in delays}
        refusals_count = {delay: 0 for delay in delays}
        total_presentation_count = {delay: 0 for delay in delays}

        for line in data:
            total_presentation_count[line['Текущая отсрочка']] += 1
            if line['Отказ от ответа']:
                refusals_count[line['Текущая отсрочка']] += 1
            else:
                total_answer_count[line['Текущая отсрочка']] += 1
                if line['Ответ'] == line['Правильный ответ']:
                    correct_answer_count[line['Текущая отсрочка']] += 1

        right_answer_percentage = []
        for delay in delays:
            if total_answer_count[delay]:
                right_answer_percentage.append(correct_answer_count[delay] / total_answer_count[delay] * 100)
            else:
                right_answer_percentage.append(0)

        self.figure_subplots[2].plot(delays, right_answer_percentage)

        refusals_persentage = []
        for delay in delays:
            if total_presentation_count[delay]:
                refusals_persentage.append(refusals_count[delay] / total_presentation_count[delay] * 100)
            else:
                refusals_persentage.append(0)

        self.figure_subplots[3].plot(delays, refusals_persentage)

        self.draw()
