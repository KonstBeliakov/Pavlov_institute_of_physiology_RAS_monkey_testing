from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from settings import settings


class GraphPanel:
    def __init__(self, root):
        self.root = root

        self.figsize = (4, 4)

        self.figure1 = plt.Figure(figsize=self.figsize)
        self.figure1.suptitle(f'Кривые ответов по задержкам')
        self.graph_canvas1 = FigureCanvasTkAgg(self.figure1, self.root)
        self.graph_canvas1.get_tk_widget().grid(row=1, column=0)
        self.figure_subplot1 = self.figure1.add_subplot()

        self.figure2 = plt.Figure(figsize=self.figsize)
        self.figure2.suptitle(f'Среднее время ответа по задержкам')
        self.graph_canvas2 = FigureCanvasTkAgg(self.figure2, self.root)
        self.graph_canvas2.get_tk_widget().grid(row=1, column=1)
        self.figure_subplot2 = self.figure2.add_subplot()

        self.figure3 = plt.Figure(figsize=self.figsize)
        self.figure3.suptitle(f'Процент правильных ответов по задержкам')
        self.graph_canvas3 = FigureCanvasTkAgg(self.figure3, self.root)
        self.graph_canvas3.get_tk_widget().grid(row=1, column=2)
        self.figure_subplot3 = self.figure3.add_subplot()

        self.figure4 = plt.Figure(figsize=self.figsize)
        self.figure4.suptitle(f'Процент отказов по задержкам')
        self.graph_canvas4 = FigureCanvasTkAgg(self.figure4, self.root)
        self.graph_canvas4.get_tk_widget().grid(row=1, column=3)
        self.figure_subplot4 = self.figure4.add_subplot()

        self.draw()

    def draw(self):
        self.graph_canvas1.draw()
        self.graph_canvas2.draw()
        self.graph_canvas3.draw()
        self.graph_canvas4.draw()

    def update(self, data):
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
        self.figure_subplot1.clear()
        for i in range(graph_number):
            self.figure_subplot1.plot(list(range(len(graph_data[i]))), graph_data[i])
        self.figure_subplot1.legend([f'Задержка {delay} секунд' for delay in settings['delay'][1]])

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

        self.figure_subplot2.clear()
        self.figure_subplot2.plot(delays, avg_time)

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

        self.figure_subplot3.clear()
        self.figure_subplot3.plot(delays, right_answer_percentage)

        refusals_persentage = []
        for delay in delays:
            if total_presentation_count[delay]:
                refusals_persentage.append(refusals_count[delay] / total_presentation_count[delay] * 100)
            else:
                refusals_persentage.append(0)

        self.figure_subplot4.clear()
        self.figure_subplot4.plot(delays, refusals_persentage)

        self.draw()
