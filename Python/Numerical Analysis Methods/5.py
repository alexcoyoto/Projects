#!/usr/bin/env python3
import numpy as np
import sympy as sp
import math
import matplotlib.pyplot as plt
plt.style.use('ggplot')

def main():
	eps = 0.001
	nonliner_equation(eps)
	system_nonliner_equation(eps)

def nonliner_equation(eps):
	print('\tРешение нелинейного уравнения sin(x^2)+cos(x^2)-10x = 0')
	x = sp.symbols('x')
	expr = sp.sin(x**2)+sp.cos(x**2)-10*x
	func = sp.lambdify(x, expr, "numpy")
	x1 = 0
	x2 = 1
	if not check_interval(func, x1, x2):
		return ValueError('Некорректный интервал')
	draw_schedule(func, x1, x2)
	print('\tМетод хорд')
	print('Решение уравнения методом хорд с погрешностью {0}:'.format(eps), \
		method_chord(func, expr, x1, x2, eps))
	print('\tМетод касательных')
	print('Решение уравнения методом касательных с погрешностью {0}:'.format(eps), \
		method_tangent(func, expr, x1, x2, eps))

def draw_schedule(func, x1 : float, x2 : float):
	fig, ax = plt.subplots()
	x = np.linspace(x1, x2)
	ax.plot(x, func(x), 'r')
	ax.set(xlabel = 'Ось X', ylabel = 'Ось Y', \
		title = 'График sin(x^2)+cos(x^2)-10x = 0 на интервале [{0},{1}]'.format(x1,x2))
	plt.show()

def check_interval(func, a, b):
	return func(a) * func(b) < 0

def method_chord(func, expr, x1, x2, eps):
	if not check_interval(func, x1, x2):
		return ValueError('Метод хорд. Некорректный интервал')
	
	x = sp.symbols('x')
	a, b = x1, x2	#выпукла вниз
	if func(x1) * sp.diff(expr, x, x).subs(x, x1):
		a, b = b, a 	#выпукла вверх
		print('Функция выпукла вверх')
	else:
		print('Функция выпукла вниз')

	x_prev = a
	amount_of_iterations = 0
	while True:
		amount_of_iterations += 1
		x_new = x_prev - (b - x_prev) * func(x_prev) / (func(b)-func(x_prev))
		print("Итерация ", amount_of_iterations)
		print('x[{0}] = '.format(amount_of_iterations),x_new)
		if abs(x_new - x_prev) < eps:
			break
		x_prev = x_new 

	return x_new

def method_tangent(func, expr, x1, x2, eps):
	if not check_interval(func, x1, x2):
		return ValueError('Метод касательных. Некорректный интервал')

	x = sp.symbols('x')
	x_prev = x2
	if func(x1) * sp.diff(expr, x, x).subs(x, x1):
		x_prev = x1
		print('Функция выпукла вверх')
	else:
		print('Функция выпукла вниз')

	diff_func = sp.lambdify(x, sp.diff(expr, x), "numpy")
	amount_of_iterations = 0
	while True:
		amount_of_iterations += 1
		x_new = x_prev - func(x_prev) / diff_func(x_prev)
		print("Итерация ", amount_of_iterations)
		print('x[{0}] = '.format(amount_of_iterations),x_new)
		if abs(x_new - x_prev) < eps:
			break
		x_prev = x_new

	return x_new

def system_nonliner_equation(eps):
	print('\n\tРешение системы нелинейных уравнений\ntg(x*y+0.4)=3*x^2\n6*x^2+0.2*y^2=1 x,y>0')
	x, y = sp.symbols('x y')
	expr1 = sp.tan(x*y + 0.4)-3*(x**2)
	expr2 = 6*(x**2)+0.2*(y**2)-1
	func1 = sp.lambdify((x, y), expr1, "numpy")
	func2 = sp.lambdify((x, y), expr2, "numpy")
	x1, x2, y1, y2 = 0, 3, 0, 3
	draw_shedule_system(expr1, expr2, x1, x2, y1, y2)
	x0 = 0.3
	y0 = 0.1
	print('\tМетод Ньютона')
	print('Решение системы методом Ньютона с погрешностью {0}:'.format(eps), \
		newton_method(expr1, expr2, func1, func2, x0, y0, eps ))
	print('\tМодифицированный метод Ньютона')
	print('Решение системы модифицированным методом Ньютона с погрешностью {0}:'.format(eps), \
		newton_modified_method(expr1, expr2, func1, func2, x0, y0, eps ))
	print('\tМетод простых итераций')
	print('Решение системы методом простых итераций {0}:'.format(eps), MSI(x0, y0, eps ))

def draw_shedule_system(expr1, expr2, x1, x2, y1, y2):
	x, y = sp.symbols('x y')
	plot1 = sp.plotting.plot_implicit(sp.Eq(expr1, 0), (x, x1, x2), (y, y1, y2))
	plot2 = sp.plotting.plot_implicit(sp.Eq(expr2, 0), (x, x1, x2), (y, y1, y2))
	plot1.extend(plot2)
	plot1.title='Решение системы'
	plot1.xlabel='Ось X'
	plot1.ylabel='Ось Y'
	plot1.show()

def jacobian(expr1, expr2, x0, y0):
	x, y = sp.symbols('x y')
	J = np.empty((2,2), dtype = float)
	J[0][0] = sp.diff(expr1, x).subs([(x, x0), (y, y0)]).evalf()
	J[0][1] = sp.diff(expr1, y).subs([(x, x0), (y, y0)]).evalf()
	J[1][0] = sp.diff(expr2, x).subs([(x, x0), (y, y0)]).evalf()
	J[1][1] = sp.diff(expr2, y).subs([(x, x0), (y, y0)]).evalf()
	return J

def newton_method(expr1, expr2, func1, func2, x0, y0, eps):
	x_y = np.array([x0, y0])
	amount_of_iterations = 0
	while True:
		amount_of_iterations += 1
		J = jacobian(expr1, expr2, *x_y)
		if not np.linalg.det(J):
			raise ValueError('Якобиан равен 0')
		J = np.linalg.inv(J)
		func_values = np.array([func1(*x_y), func2(*x_y)])
		x_new = x_y[0] - J[0].dot(func_values)
		y_new = x_y[1] - J[1].dot(func_values)
		print('Шаг ', amount_of_iterations)
		print('x[{0}] = {1}\ny[{0}] = {2}'.format(amount_of_iterations, x_new, y_new))
		if np.absolute(np.array([x_new, y_new]) - x_y).max() < eps:
			break
		x_y[0], x_y[1] = x_new, y_new
	print('Количество итераций: ', amount_of_iterations)
	return x_new, y_new

def newton_modified_method(expr1, expr2, func1, func2, x0, y0, eps):
	J = jacobian(expr1, expr2, x0, y0)
	if not np.linalg.det(J):
		raise ValueError('Якобиан равен 0')
	J = np.linalg.inv(J)
	amount_of_iterations = 0
	x_y = np.array([x0, y0])
	while True:
		amount_of_iterations += 1
		func_values = np.array([func1(*x_y), func2(*x_y)])
		x_new = x_y[0] - J[0].dot(func_values)
		y_new = x_y[1] - J[1].dot(func_values)
		print('Шаг ', amount_of_iterations)
		print('x[{0}] = {1}\ny[{0}] = {2}'.format(amount_of_iterations, x_new, y_new))
		if np.absolute(np.array([x_new, y_new]) - x_y).max() < eps:
			break
		'''if amount_of_iterations > 50:
			break'''
		x_y[0], x_y[1] = x_new, y_new
	print('Количество итераций: ', amount_of_iterations)
	return x_new, y_new

def MSI(x0, y0, eps):
	x, y = sp.symbols('x y')
	#phi1 = (sp.atan(3*(x**2)) - 0.4)/y
	phi1 = sp.sqrt(sp.tan(x*y + 0.4)/3)
	phi2 = sp.sqrt(5-30*(x**2))
	if x0>1/(6**0.5):	#проверка для корня
		raise ValueError('МПИ. Значение x>1/sqrt(6)')
	J = jacobian(phi1, phi2, x0, y0)
	if np.linalg.norm(J) >= 1:
		print('Норма матрицы J = {0}'.format(np.linalg.norm(J)))
		raise ValueError('МПИ не сходится')
	f_for_x = sp.lambdify((x, y), phi1, "numpy")
	f_for_y = sp.lambdify((x, y), phi2, "numpy")
	amount_of_iterations = 0
	while True:
		amount_of_iterations +=1
		x_new = f_for_x(x0, y0)
		y_new = f_for_y(x0, y0)
		print('Шаг ', amount_of_iterations)
		print('x[{0}] = {1}\ny[{0}] = {2}'.format(amount_of_iterations, x_new, y_new))
		if max([abs(x0 - x_new), abs(y0 - y_new)]) < eps:
			break
		x0, y0 = x_new, y_new
	print('Количество итераций: ', amount_of_iterations)
	return x_new, y_new

if __name__ == "__main__":
	try:
		main()
	except ValueError as ve:
		print(ve)
	except Error as er:
		print(er)