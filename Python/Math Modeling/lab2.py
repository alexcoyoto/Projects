from lab1 import congruent
from lab1 import create_plot
from lab1 import expected_value
from lab1 import dispersion
import random
import sympy
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as ss
from scipy.stats import binom
import seaborn as sns

import statsmodels.stats.api as sms


n_val = 10000
scale = 100


def neuman():
    #   a = 0, b = 1
    x1_k = []
    x2_k = []
    y1_k = []
    y2_k = []
    X = []
    Y = []
    fx_max = 3

    Ai = random.uniform(10 ** 7, 10 ** 10)
    m = random.uniform(10 ** 7, 10 ** 10)
    k = random.uniform(10 ** 7, 10 ** 10)

    for i in range(n_val * 6):
        Ai = congruent(Ai, m, k)
        x1_k.append(Ai / m)
        Ai = congruent(Ai, m, k)
        y1_k.append(Ai / m)
    for i in range(n_val * 6):
        Ai = congruent(Ai, m, k)
        x2_k.append((Ai / m) * fx_max)
        Ai = congruent(Ai, m, k)
        y2_k.append((Ai / m))
        #   x2_k.append(x1_k[i] * fx_max)

    i = 0
    while len(X) < n_val:
        if (8 * (x1_k[i] ** 3) + 1) / 3 >= x2_k[i]:     # f(x)
            X.append(x1_k[i])
        i += 1

    create_plot(X, n_val, 15)
    #   print(f'M(X) = {expected_value(X, n_val)}')

    i = 0
    j = 0
    while len(Y) < n_val:
        if (8 * (X[j] ** 3) + 2 * y1_k[i]) / (8 * (X[j] ** 3) + 1) \
                >= y2_k[i] * ((8 * X[j] ** 3 + 2) / (8 * X[j] ** 3 + 1)):  # f(x | y), fx|y_max
            Y.append(y1_k[i])
            j += 1
        i += 1

    create_plot(Y, n_val, 15)
    #   print(f'M(Y) = {expected_value(Y, n_val)}')

    return X, Y


def bernoulli(p):
    X = []
    for i in range(scale + 1):
        X.append(C_coeff(i, scale) * p ** i * (1-p) ** (scale - i))
    return X


def C_coeff(m, n):
    return np.math.factorial(n) / (np.math.factorial(m) * np.math.factorial(n - m))


def fac(n):
    if n == 0:
        return 1
    return fac(n-1) * n


def create_matrix(X, pre_Y):
    XY = []
    for i in range(scale + 1):
        row = []
        for j in range(scale + 1):
            row.append((X[i] * pre_Y[j]))
        XY.append(row)
    iter = scale
    while iter < scale * 2:     # sum of hits
        for i in range(len(XY)):
            XY[i].append(0)
        iter += 1
    for i in range(len(XY)):
        XY[i] = shift_matrix(XY[i], i)
    return XY


def shift_matrix(data_list, steps):
    if steps < 0:
        steps = abs(steps)
        for i in range(steps):
            data_list.append(data_list.pop(0))
    else:
        for i in range(steps):
            data_list.insert(0, data_list.pop())
    return data_list


def display_matrix(matrix):
    if scale > 10:
        print('Вельмі дробязныя значэнні. Няма сэнсу выводзіць матрыцу')
        return
    for i in range(len(matrix)):
        final_str = ''
        for j in range(len(matrix[i])):
            final_str = final_str + '%.10f' % matrix[i][j] + ' '
        print(final_str)


def get_Y(matrix):
    Y = []
    matrix = np.transpose(matrix)
    for i in range(len(matrix)):
        column_sum = 0
        for j in range(len(matrix[i])):
            column_sum = column_sum + matrix[i][j]
        Y.append(column_sum)
    return Y


def empirical_stuff(X, Y):
    print(f'M(X) = {expected_value(X, n_val)}')
    print(f'M(Y) = {expected_value(Y, n_val)}')
    Mxy = 0
    for i in range(n_val):
        Mxy += X[i] * Y[i]
    Mxy /= n_val
    print(f'M(X,Y) = {Mxy}\n')

    print(f'D(X) = {dispersion(X, n_val)}')
    print(f'D(Y) = {dispersion(Y, n_val)}')

    Mxy_square = 0
    for i in range(n_val):
        Mxy_square += (X[i] ** 2) * (Y[i] ** 2)
    Mxy_square /= n_val
    print(f'D(X,Y) = {Mxy_square - Mxy ** 2}\n')

    cov_xy = Mxy - expected_value(X, n_val) * expected_value(Y, n_val)
    print(f'K(X,Y) = {cov_xy}')
    rxy = cov_xy / (dispersion(X, n_val) ** 0.5 * dispersion(Y, n_val) ** 0.5)
    print(f'r(X,Y) = {rxy}')


def M_for_DSV(X):
    result = 0
    for i in range(len(X)):
        result = result + X[i] * i
    return result


def D_for_DSV(X):
    result = 0
    for i in range(len(X)):
        result = result + X[i] * i ** 2
    return result - M_for_DSV(X) ** 2


def theory_stuff():
    x = sympy.symbols('x')
    y = sympy.symbols('y')
    f_xy = 8/3 * (x ** 3 + y / 4)
    f_x = (8 * x ** 3 + 1) / 3
    f_x_after_y = (8 * x ** 3 + 2 * y) / (8 * x ** 3 + 1)
    #   aa = sympy.integrate(f_xy, (y, 0,  1))
    #   print(sympy.integrate(sympy.integrate(f_xy, (y, 0, 1)), (x, 0, 1)))
    Mx = sympy.integrate(sympy.integrate(f_xy * x, (y, 0, 1)), (x, 0, 1))
    My = sympy.integrate(sympy.integrate(f_xy * y, (y, 0, 1)), (x, 0, 1))
    Mxy = sympy.integrate(sympy.integrate(f_xy * x * y, (y, 0, 1)), (x, 0, 1))
    print(f'M(X) = {Mx}')
    print(f'M(Y) = {My}')
    print(f'M(X,Y) = {Mxy}\n')

    print(f'D(X) = {sympy.integrate(sympy.integrate(f_xy * x ** 2, (y, 0, 1)), (x, 0, 1)) - Mx ** 2}')
    print(f'D(Y) = {sympy.integrate(sympy.integrate(f_xy * y ** 2, (y, 0, 1)), (x, 0, 1)) - My ** 2}')
    print(f'D(X,Y) = {sympy.integrate(sympy.integrate(f_xy * (x ** 2) * (y ** 2), (y, 0, 1)), (x, 0, 1)) - Mxy ** 2}\n')

    print(f'K(X,Y) = {Mxy - Mx * My}')


def conf_intervals(data_list, symbol):
    confidence = 0.95
    se = ss.sem(data_list)
    h = se * ss.t._ppf((1 + confidence) / 2., n_val - 1)
    print(f'{expected_value(data_list, n_val) - h} <= M({symbol})={expected_value(data_list, n_val)}'
          f' <= {expected_value(data_list, n_val) + h}')

    h_min = ss.chi2.isf(confidence / 2, n_val - 1)
    h_plus = ss.chi2.isf(1 - confidence / 2, n_val - 1)
    print(f'{dispersion(data_list, n_val) * n_val / h_min}'
          f' <= D({symbol})={dispersion(data_list, n_val)} <= {dispersion(data_list, n_val) * n_val / h_plus}\n')


def c_i_DSV(X, symbol):
    confidence = 0.95
    se = ss.sem(X)
    n = 10 ** 5
    h = se * ss.t._ppf((1 + confidence) / 2., n - 1)
    print(f'{M_for_DSV(X) - h} <= M({symbol})={M_for_DSV(X)}'
          f' <= {M_for_DSV(X) + h}')

    h_min = ss.chi2.isf(confidence / 2, n - 1)
    h_plus = ss.chi2.isf(1 - confidence / 2, n - 1)
    print(f'{D_for_DSV(X) * n / h_min}'
          f' <= D({symbol})={D_for_DSV(X)} <= {D_for_DSV(X) * n / h_plus}\n')


def empirical_stuff_for_DSV(X, Y, XY):
    print(f'M(X) = {M_for_DSV(X)}')
    print(f'M(Y) = {M_for_DSV(Y)}')
    Mxy = 0
    for i in range(len(XY)):
        yj_pij = 0
        for j in range(len(XY[i])):
            yj_pij = yj_pij + XY[i][j] * j
        Mxy = Mxy + yj_pij * i

    print(f'M(X,Y) = {Mxy}\n')

    print(f'D(X) = {D_for_DSV(X)}')
    print(f'D(Y) = {D_for_DSV(Y)}')

    cov_xy = Mxy - M_for_DSV(X) * M_for_DSV(Y)
    print(f'\nK(X,Y) = {cov_xy}')
    rxy = cov_xy / (D_for_DSV(X) ** 0.5 * D_for_DSV(Y) ** 0.5)
    print(f'r(X,Y) = {rxy}')


def create_plot_for_DSV(px):
    #   k = len(X) / scale
    if scale <= 100:
        heads = run_binom((scale + 1) * (scale * 2 + 1), scale, px)
    else:
        min_scale = 100
        heads = run_binom((min_scale + 1) * (min_scale * 2 + 1), min_scale, px)
    ax = sns.histplot(heads, bins=11, label='Шматкутнік размеркавання')
    ax.set_xlabel("Колькасць трапленняў", fontsize=16)
    ax.set_ylabel("Частасць", fontsize=16)
    plt.show()


def run_binom(trials, n, p):
    heads = []
    for i in range(trials):
        tosses = [np.random.random() for i in range(n)]
        heads.append(len([i for i in tosses if i >= 0.50]))
    return heads


if __name__ == '__main__':
    #   print((75350124 - 1) % 9 + 1)  9var
    #   a = 0, b = 1, f_max = 3

    X_list = []
    Y_list = []
    X_list, Y_list = neuman()
    #   print(expected_value(X_list, n_val))
    print('\nЭмпірычныя ацэньванні:\n')
    empirical_stuff(X_list, Y_list)
    print('\nТэарэтычныя ацэньванні:\n')
    theory_stuff()
    print('\nДаверныя інтэрвалы:\n')
    conf_intervals(X_list, 'X')
    conf_intervals(Y_list, 'Y')

    print('###\n')
    print('ДВВ:\n')
    pX = random.uniform(0, 1)
    p_pre_Y = random.uniform(0, 1)
    print(f'p(x) = {pX}')
    print(f'p(pre_y) = {p_pre_Y}')
    Xd = bernoulli(pX)
    pre_Yd = bernoulli(p_pre_Y)
    #   print(Xd)
    #   print(np.sum(Yd))
    XYd = create_matrix(Xd, pre_Yd)
    numbers_D = (scale + 1) * (scale * 2 + 1)
    print('\nМатрыца размеркавання:\n')
    display_matrix(XYd)
    print(f'Колькасць значэнняў: {numbers_D}')
    print(f'Сума значэнняў матрыцы: {np.sum(XYd)}\n')

    print(f'ЗР для X: {Xd}')
    print(f'Сума значэнняў X: {np.sum(Xd)}\n')
    create_plot_for_DSV(pX)

    create_plot(Xd, len(Xd), 10)

    Yd = get_Y(XYd)
    print(f'ЗР для Y: {Yd}')
    print(f'Сума значэнняў Y: {np.sum(Yd)}\n')
    # p_y = M_for_DSV(Yd) / scale
    # create_plot_for_DSV(p_y)

    create_plot(Yd, len(Yd), 10)

    print('Эмпірычныя ацэньванні:\n')
    empirical_stuff_for_DSV(Xd, Yd, XYd)

    print('\nДаверныя інтэрвалы:\n')
    c_i_DSV(Xd, 'X')
    c_i_DSV(Yd, 'Y')


