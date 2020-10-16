import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random


k = 15
s = 80


def square_analysis():
    while True:
        n_val = int(input('Увядзіце лік n: '))
        square_list = []
        cur_val = 123456789

        for i in range(n_val):
            cur_val = square(cur_val)
            square_list.append(cur_val / 10 ** 8)

        # print(square_list)

        create_plot(square_list, n_val, k)
        hit_rate(square_list, n_val)

        print(f'R(xy) = {correlation(square_list, n_val)}')
        if input('\nПрацягнуць?(1/0): ') != '1':
            break


def congruent_analysis():
    while True:
        Ai = random.uniform(10 ** 7, 10 ** 10)
        m = random.uniform(10 ** 7, 10 ** 10)
        k = random.uniform(10 ** 7, 10 ** 10)

        n_val = int(input('Увядзіце лік n: '))

        congruent_list = []
        for i in range(n_val):
            Ai = congruent(Ai, m, k)
            congruent_list.append(Ai / m)
        # print(congruent_list)
        create_plot(congruent_list, n_val, k)
        hit_rate(congruent_list, n_val)

        print(f'R(xy) = {correlation(congruent_list, n_val)}')
        if input('\nПрацягнуць?(1/0): ') != '1':
            break


def create_plot(data_list, n, k_v):
    hist_data = pd.Series(data_list)
    hist_data.plot.hist(grid=True, bins=k_v, rwidth=0.9, color='#607c8e')
    plt.title(f'Гістаграма частасцяў пры n={n}')
    plt.xlabel('Шкала магчымых выпадковых лікаў')
    plt.ylabel('Колькасць значэнняў')
    plt.grid(axis='y', alpha=0.75)
    plt.xticks(np.linspace(0.0, 1.0, k_v + 1))
    plt.show()


def hit_rate(data_list, n):
    print('Трапленні ў інтэрвалы:')
    for i in range(k):
        curr_num = 0
        for j in range(len(data_list)):
            if (i + 1) / k > data_list[j] >= i / k:
                curr_num += 1
        print(f'[{i / k} - {(i + 1) / k}]: {curr_num}; адносная частасць траплення ў інтэрвал: {curr_num / n * 100}%;')
    print(f'M(x) = {expected_value(data_list, n)}')
    print(f'D(x) = {dispersion(data_list, n)}')


def expected_value(data_list, n):  # M(x)
    value = 0
    for i in range(len(data_list)):
        value += data_list[i]
    return value / n


def dispersion(data_list, n):
    value = 0
    for i in range(len(data_list)):
        value += data_list[i] ** 2
    return (value / n) - (expected_value(data_list, n) ** 2)


def correlation(data_list, n):
    xList = []
    yList = []
    Mxy = 0
    for i in range(n - s):
        xList.append(data_list[i])
        yList.append(data_list[i + s])
    for i in range(n - s):
        Mxy += xList[i] * yList[i]
    Mxy /= (n - s)
    return (Mxy - (expected_value(xList, n - s) * expected_value(yList, n - s))) \
           / ((dispersion(xList, n - s) * dispersion(yList, n - s)) ** 0.5)


def square(num):
    num_square = num ** 2
    str_num_square = str(num_square)

    # print(len(str_num_square))
    if len(str_num_square) < 8:
        i = len(str_num_square)
        count = ''
        while i < 8:
            count += '0'
            i += 1
        str_num_square = count + str_num_square

    # print(f'Квадрат ліку: {str_num_square}')
    middle = int(len(str_num_square) / 2)
    # return int(f'{str_num_square[middle - 2]}{str_num_square[middle - 1]}'f'{str_num_square[middle]}{
    # str_num_square[middle + 1]}')
    return int(f'{str_num_square[middle - 4]}{str_num_square[middle - 3]}'
               f'{str_num_square[middle - 2]}{str_num_square[middle - 1]}'
               f'{str_num_square[middle]}{str_num_square[middle + 1]}'
               f'{str_num_square[middle + 2]}{str_num_square[middle + 3]}')


def congruent(Ai, m, k):
    return (k * Ai) % m


if __name__ == '__main__':
    print('## Метад квадратаў ##')
    number = 0
    while number < 10 ** 7:
        number = int(input('Увядзіце дастаткова вялікі лік: '))
    answer_square = square(number)
    print(f'Адказ: {answer_square / 10 ** 8}')  # / 10000 ??
    while input('Працягнуць?(1/0): ') == '1':
        answer_square = square(answer_square)
        print(f'Адказ: {answer_square / 10 ** 8}')
        if answer_square == 0:
            print('Паўнамоцтвы метаду скончыліся')
            break

    print('\n## Мультыплікатыўны кангруэнтны метад ##')
    A_val = 0
    m_val = 0
    k_val = 0
    while A_val < 10 ** 7:
        A_val = int(input('Увядзіце дастаткова вялікі A0: '))
    while m_val < 10 ** 7:
        m_val = int(input('Увядзіце дастаткова вялікі m: '))
    while k_val < 10 ** 7:
        k_val = int(input('Увядзіце дастаткова вялікі k: '))
    A_val = congruent(A_val, m_val, k_val)
    print(f'Адказ: {A_val / m_val}')

    while input('Працягнуць?(1/0): ') == '1':
        A_val = congruent(A_val, m_val, k_val)
        print(f'Адказ: {A_val / m_val}')
        if A_val == 0:
            print('Паўнамоцтвы метаду скончыліся')
            break

    print('\n## Статыстычнае даследаванне ##')
    print('1) Для метаду квадрата:')
    square_analysis()
    print('\n2) Для мультыплікатыўнага кангруэнтнага метаду:')
    congruent_analysis()
