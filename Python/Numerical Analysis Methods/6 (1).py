#!/usr/bin/env python3
import numpy as np
import sympy as sp
import math
import matplotlib.pyplot as plt
plt.style.use('ggplot')


def main():
	with open('file', 'r') as f:
		matrix = [float(num) for num in f.read().split()]
	x = matrix[:len(matrix) // 2]
	y = matrix[len(matrix) // 2:]
	print('x =',x)
	print('y =',y)
	print('\n    Многочлен Лагранжа:')
	f_L = Lagranzh(x,y)
	print('\n    Многочлен Ньютона:')
	f_N = newton_polinomial(table_divided_difference(x,y), x, y)
	print('\n    Кусочно-линейный и кусочно-квадратичный сплайны:')
	linear_coef = linear_spline(x, y)
	quadratic_coef = quadratic_spline(x, y)
	print('\n    Кубический интерполяционный сплайн:')
	cubic_coef = cubic_spline(x, y)
	
	range_X = np.linspace(0, 3)
	plt.plot(range_X, f_L(range_X), label='Лагранжа')
	plt.plot(range_X, f_N(range_X), label='Ньютона')
	plt.plot(range_X, [linear_spline_function(x_value, x, *linear_coef) for x_value in range_X], label='линейный сплайн')
	plt.plot(range_X, [quadratic_spline_function(x_value, x, *quadratic_coef) for x_value in range_X], label='квадратичный сплайн')
	plt.plot(range_X, [cubic_spline_function(x_value, x, *cubic_coef) for x_value in range_X], label='кубический сплайн')
	plt.scatter(x, y)
	plt.legend()
	plt.grid(True)
	plt.title('Все графики')
	plt.show()

def Lagranzh(X,Y):
    x = sp.symbols('x')
    expr = 1
    for xi in X:
        expr = expr * (x - xi)	
    L = 0
    for xi, yi in zip(X, Y):
        L = L + yi * (expr / (x - xi)) / (expr / (x - xi)).subs(x, xi)
    print(' Интерполяционный многочлен Лагранжа:\n',L.expand())
    func = sp.lambdify(x, L, "numpy")
    print('L(x1+x2) =', func(X[0]+X[1]))
    Lagranzh_chedule(func,0, 3)
    return func

def Lagranzh_chedule(func, x1:float,x2:float):
	fig, ax = plt.subplots()
	x = np.linspace(x1, x2)
	ax.plot(x, func(x), 'r')
	ax.set(xlabel = 'Ось X', ylabel = 'Ось Y', title = 'Интерполяционный многочлена Лагранжа')
	plt.show()

def table_finite_difference(x, y):
    n = len(y)
    diff = []
    diff.append(x)
    diff.append(y)
    for diff_num in range(n - 1):
        diff.append(['' for _ in range(n)])
        for i in range(1, n - diff_num):
            diff[diff_num + 2][i - 1] = diff[diff_num + 1][i] - diff[diff_num + 1][i - 1]
    print(' Таблица конечных разностей:')
    print('|  x  |   y  |        dy(k)      |      d2y(k)      |d3y(k)|      d4y(k)       |')
    for i in range(len(x)):
        print('|{0}|{1}|{2}|{3}|{4}|{5}|'.format(x[i],y[i], diff[2][i], diff[3][i], diff[4][i], diff[5][i]))

def divided_difference(X : np.array, Y : np.array):
    x = sp.symbols('x')
    expr = 1
    for xi in X:
        expr = expr * (x - xi)
    diff = 0
    for xi, yi in zip(X, Y):
        diff += yi / (expr / (x - xi)).subs(x, xi)  
    return diff        

def table_divided_difference(x, y):
    n = len(y)
    diff = []
    diff.append(x)
    diff.append(y)
    for order in range(1, n):
        diff.append(['' for _ in range(n)]) 
        for i in range(n - order):
            diff[order + 1][i] = divided_difference(x[i:i + order + 1], y[i:i + order + 1]) 
    return diff

def newton_polinomial(div_diffs,X,Y):
    table_finite_difference(X,Y)
    diff=table_divided_difference(X,Y)
    print(' Таблица разделенных разностей:')
    print('|    x|     y|      1         |        2       |        3        |         4        |')
    for i in range(len(X)):
        print('|{0}|{1}|{2}|{3}|{4}|{5}|'.format(X[i],Y[i], diff[2][i], diff[3][i], diff[4][i], diff[5][i]))
    x = sp.symbols('x')
    expr = 1
    n = len(div_diffs) 
    N = 0
    for i in range(1, n): 
        N += div_diffs[i][0] * expr
        expr = expr * (x - div_diffs[0][i - 1])
    print(' Интерполяционный многочлен Ньютона:\n',N.expand())
    func = sp.lambdify(x, N, "numpy")
    print('N(x1+x2) =', func(X[0]+X[1]))
    return sp.lambdify(x, N, "numpy")

def linear_spline_function(x_value, x_points, a, b):
    interval_index = len(x_points) - 2
    for i in range(1, len(x_points)):
        if x_value < x_points[i]:
            interval_index = i - 1
            break           
    return a[interval_index] * x_value + b[interval_index]

def linear_spline(x, y):
    n = len(x)
    fig, ax = plt.subplots() 
    a, b = np.empty(n - 1), np.empty(n - 1)
    for i in range(n - 1):
        A = np.array([[x[i], 1], [x[i  + 1], 1]])
        B = np.array(y[i:i+2])
        a[i], b[i] = np.linalg.solve(A, B) 

        range_X = np.linspace(x[i], x[i+1])
        ax.plot(range_X, a[i] * range_X + b[i])
    print('		Таблица Кусочно-линейных сплайнов:')
    print('|    a|     b|')
    for i in range(len(x)-1):
        print('|{0}|{1}|'.format("{0:0.3f}".format(a[i]), "{0:0.3f}".format(b[i])))
    plt.grid(True)
    plt.scatter(x, y)  
    plt.title('Кусочно-линейный сплайн')
    plt.show()
    return a, b

def quadratic_spline_function(x_value, x_points, a, b, c):
    interval_index = len(x_points) - 3
    for i in range(1, len(x_points) - 1):
        if x_value < x_points[i]:
            interval_index = i - 1
            break           
    return c[interval_index] + (b[interval_index] + a[interval_index] * x_value) * x_value

def quadratic_spline(x, y):
    n = len(x)
    fig, ax = plt.subplots() 
    a, b, c = np.empty(n - 2), np.empty(n - 2), np.empty(n - 2)
    for i in range(n - 2):
        A = []
        for j in range(3):
            A.append([x[i+j] ** 2, x[i+j], 1])
        a[i], b[i], c[i] = np.linalg.solve(np.array(A), np.array(y[i:i+3]))
        
        range_X = np.linspace(x[i], x[i+1] if i < len(x) - 3 else x[i+2])
        ax.plot(range_X, a[i] * range_X ** 2 + b[i] * range_X + c[i])
    for j in range(len(x)-3):
    	for i in range(0,len(x)-2,2):
    		a1[j] = a[i]
    		b1[j] = b[i]
    		c1[j] = c[i]
    print('Таблица Кусочно-квадратичных сплайнов:')
    print('|    a|     b|     с|')
    for i in range(len(x)-3):
        print('|{0}|{1}|{2}|'.format("{0:0.3f}".format(a[i]),"{0:0.3f}".format(b[i]), "{0:0.3f}".format(c[i])))
        
    plt.grid(True)
    plt.scatter(x, y)  
    plt.title('Кусочно-квадратичный сплайн')
    plt.show()
    return a, b, c

def cubic_spline_function(x_value, x_points, a, b, c, d):
    ii = len(x_points) - 2 # ii == interval_index
    for i in range(1, len(x_points)):
        if x_value < x_points[i]:
            ii = i - 1
            break
            
    return a[ii] + (b[ii] + (c[ii] + d[ii] * (x_value - x_points[ii + 1])) * (x_value - x_points[ii + 1])) * (x_value - x_points[ii + 1])

def cubic_spline(x, y):
    n  = len(x)
    
    h_i = np.array([x[i] - x[i - 1] for i in range (1, n)])
    l_i = np.array([(y[i] - y[i - 1]) / h_i[i - 1] for i in range(1, n)])
    delta_i = np.empty(n - 2, float)
    lambda_i = np.empty(n - 2, float)
    
    delta_i[0] =  -0.5 * h_i[1] / (h_i[0] + h_i[1])
    lambda_i[0] = 1.5 * (l_i[1] - l_i[0]) / (h_i[0] + h_i[1])
    
    for i in range(1, n - 2):
        delta_i[i] = - h_i[i + 1] / (2 * h_i[i] + 2 * h_i[i + 1] + h_i[i] * delta_i[i - 1])
        lambda_i[i] = (2 * l_i[i + 1] - 3 * l_i[i] - h_i[i] * lambda_i[i - 1]) / \
                      (2 * h_i[i] + 2 * h_i[i + 1] + h_i[i] * delta_i[i - 1])
    
    print('delta:\n{}'.format(delta_i))
    print('lambda:\n{}'.format(lambda_i))
    
    a = np.array(y.copy()[1:])
    b = np.empty(n - 1)
    c = np.empty(n - 1)
    d = np.empty(n - 1)

    c[n - 2] = 0    
    for i in range(n - 3, -1, -1):
        c[i] = delta_i[i] * c[i + 1] + lambda_i[i]
    # for i = 0, because c[-1] = c[n] = 0
    for i in range(n - 2, -1, -1):
        b[i] = l_i[i] + 2 / 3 * c[i] * h_i[i] + 1 / 3 * h_i[i] * c[i - 1]
        d[i] = (c[i] - c[i - 1]) / (3 * h_i[i])
    fig, ax = plt.subplots()
    for i in range(n - 1):
        range_X = np.linspace(x[i], x[i + 1])
        ax.plot(range_X, a[i] + (b[i] + (c[i] + d[i] * (range_X - x[i + 1])) * (range_X - x[i + 1])) * (range_X - x[i + 1]))
    
    print(' Таблица Кубических сплайнов:')
    print('|    a|     b|    с|    d|')
    for i in range(len(x)-1):
        print('|{0}|{1}|{2}|{3}|'.format("{0:0.3f}".format(a[i]), "{0:0.3f}".format(b[i]), "{0:0.3f}".format(c[i]), "{0:0.3f}".format(d[i])))

    plt.grid(True)
    plt.scatter(x, y)  
    plt.title('Кубический сплайн')
    plt.show()
    return a, b, c, d

if __name__ == "__main__":
	try:
		main()
	except ValueError as ve:
		print(ve)
	except Error as er:
		print(er)