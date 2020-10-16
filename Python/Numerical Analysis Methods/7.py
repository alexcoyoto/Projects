#!/usr/bin/env python3
import numpy as np
import sympy as sp
import math
import matplotlib.pyplot as plt
plt.style.use('ggplot')

def main():
	eps = 0.0001
	x, y = sp.symbols('x y')
	int_expr = (x ** 2 + 1) ** 0.5
	#my_int = np.arcsinh(x) / 2 + (x * (x**2 + 1)**0.5)/2
	int_func = sp.lambdify(x, int_expr)
	int_a = 0
	int_b = 1.8
	print("Численное интегрирование:\nКоличество шагов при грубой оценке =",rough_error_estimation(int_a, int_b, 2, eps))
	int_n = integral_error_estimation(trapezium_integral, int_func, int_a, int_b, 2, eps)
	print('Количество шагов n =', int_n)
	print('Интеграл по формуле трапеций с шагом h =', trapezium_integral(int_func, int_a, int_b, int_n))
	print('Интеграл по формуле трапеций с шагом 2h =',trapezium_integral(int_func, int_a, int_b, int_n // 2))
	
	print('Интеграл по формуле Симпсона с шагом h =',simpson_integral(int_func, int_a, int_b, int_n))
	print('Интеграл по формуле Симпсона с шагом 2h =',simpson_integral(int_func, int_a, int_b, int_n // 2))
	print('Интеграл по формуле Ньютона-Лейбница =', newton_leibniz_integral(int_expr, int_a, int_b))
	print('int = ', sp.integrate(int_expr, (x, int_a, int_b)))
	#print('integral =',np.arcsinh(int_b) / 2 + (int_b * (int_b**2 + 1)**0.5)/2)

	diff_expr = 2*x*y**2 + y
	diff_func = sp.lambdify((x, y), diff_expr)
	diff_a = -1
	diff_b = 0.6
	y_x0 = 0.2
	x0 = -1

	diff_n = ode_error_estimation(ode_method_runge_kutta, diff_func, diff_a, diff_b, x0, y_x0, 4, eps)

	print('\nРешение ДУ: \nn =', diff_n)
	print('h =', abs(diff_b - diff_a) / diff_n)
	print('\n 	Метод Рунге-Кутта:')
	runge_x, runge_y = ode_method_runge_kutta(diff_func, diff_a, diff_b, x0, y_x0, diff_n)
	r_x_2, r_y_2 = ode_method_runge_kutta(diff_func, diff_a, diff_b, x0, y_x0, diff_n // 2)
	runge_chedule(runge_x, runge_y, r_x_2, r_y_2)

	print('\n 	Метод Адамса:')
	adams_x, adams_y = ode_method_adams(diff_func, diff_a, diff_b, x0, y_x0, diff_n)
	a_x_2, a_y_2 = ode_method_adams(diff_func, diff_a, diff_b, x0, y_x0, diff_n // 2)
	adams_chedule(adams_x, adams_y, a_x_2, a_y_2)

	print('\n 	Метод  Эйлера:')
	eiler_x, eiler_y = ode_method_eiler(diff_func, diff_a, diff_b, x0, y_x0, diff_n)
	e_x_2, e_y_2 = ode_method_eiler(diff_func, diff_a, diff_b, x0, y_x0, diff_n // 2)
	eiler_chedule(eiler_x, eiler_y, e_x_2, e_y_2)

	print('\n 	Точное решение задачи Коши:')
	f = sp.Function('f')
	diff_solution = sp.dsolve(sp.Eq(sp.diff(f(x), x) - f(x) - 2 * x * f(x)**2), f(x))
	print(diff_solution)
	C1 = sp.solve(np.exp(x0)/(x + 2*(-x0 + 1)*np.exp(x0))-y_x0, x)
	print('C1 =',C1)
	func_solution = sp.lambdify(x, sp.exp(x)/(C1[0] + 2*(1-x)*sp.exp(x)))
	range_x = np.linspace(diff_a, diff_b)
	exact_chedule(func_solution, range_x)

	solved_y = np.array([func_solution(xi) for xi in runge_x])
	print('\n  xi   |Exact y[i] | Runge-Kutta y[i]|  deltaR[i] | Adams y[i] | deltaA[i] |' )
	for i in range(len(runge_x)-1):
		print('|{0}|  {1}  |   {2}   |{3}| {4} |{5}|'.format("{0:0.3f}".format(runge_x[i]), "{0:0.5f}".format(solved_y[i]),\
		 "{0:0.9f}".format(runge_y[i]), "{0:0.10f}".format(abs(runge_y[i] - solved_y[i])), "{0:0.8f}".format(adams_y[i]), \
		 "{0:0.9f}".format(abs(adams_y[i] - solved_y[i]))))

	plt.plot(eiler_x, eiler_y, label='Эйлер')
	plt.plot(runge_x, runge_y, label='Рунге-Кутта')
	plt.plot(adams_x, adams_y, label='Адамс')
	plt.plot(range_x, func_solution(range_x), label='Точное')
	plt.title('Все графики')
	plt.legend()
	plt.grid()
	plt.show()


def integral_error_estimation(int_method, func, a, b, method_coef, eps):   #правило Рунге
    n = 1
    while True:
        if abs(int_method(func, a, b, 2 * n) - int_method(func, a, b, n)) / (2 ** method_coef - 1) < eps:
            break            
        n *= 2      
    return n * 2

def rough_error_estimation(a, b, method_coef, eps): 	#грубое приближение начального шага
    h0 = eps ** (1 / method_coef)
    n0 = int((b - a) / h0 + 0.5)
    return n0 - n0 % 2

def trapezium_integral(func, a, b, n):
    h = (b - a) / n
    return h * sum([(func(a + h * i) + func(a + h * (i + 1))) / 2 for i in range(n)])   

def simpson_integral(func, a, b, n): 
    h = (b - a) / n
    return h / 3 * sum([func(a + h * i) + 4 * func(a + h * (i + 1)) + func(a + h * (i + 2)) for i  in range(0, n - 1, 2)])	

def newton_leibniz_integral(expr, a, b):
	x = sp.symbols('x')
	F  = sp.integrate(expr, x)
	return F.subs(x, b) - F.subs(x, a)

def ode_error_estimation(ode_method, func, a, b, x0, y_x0, method_coef, eps):  
    n = 1
    while True:
        _, y1 = ode_method(func, a, b, x0, y_x0, 2 * n)
        _, y2 = ode_method(func, a, b, x0, y_x0, n)
        if (1/15)*abs(y2[-1] - y1[-1]) < eps:
            break
        n *= 2        
    return n * 2

def ode_method_runge_kutta(func, a, b, x0, y_x0, n):
    if x0 != a:
        raise ValueError('Must be equal')        
    h = (b - a) / n
    x = np.empty(n + 1)
    y = np.empty(n + 1)
    x[0] = x0
    y[0] = y_x0   
    for i in range(n):
        K1 = h * func(x[i], y[i])
        K2 = h * func(x[i] + h / 2, y[i] + K1 / 2)
        K3 = h * func(x[i] + h / 2, y[i] + K2 / 2)
        K4 = h * func(x[i] + h, y[i] + K3)
        y[i + 1] = y[i] + 1 / 6 * (K1 + K4 + 2 * (K2 + K3))
        x[i + 1] = x[i] + h       
    return x, y 

def runge_chedule(runge_x, runge_y, r_x_2, r_y_2):
	print(' x[i]|    y[i]      |    ~y[i]     |   delta[i]   |')
	for i in range(len(runge_x)-1):
		if i & 1 == 0:
			print('|{0}| {1} | {2} | {3} |'.format(round(runge_x[i],3),"{0:0.10f}".format(runge_y[i]), "{0:0.10f}".format(r_y_2[i // 2]),\
			"{0:0.10f}".format( abs(r_y_2[i // 2] - runge_y[i]))))
		else:
			print('|{0}| {1} |{2}|{3}|'.format(round(runge_x[i],3), "{0:0.10f}".format(runge_y[i]), "              ", "              "))

	plt.plot(runge_x, runge_y, label='h')
	plt.plot(r_x_2, r_y_2, label='2 * h')
	plt.title('Кривая методом Рунге-Кутта')
	plt.legend()
	plt.grid()
	plt.show()

def ode_method_adams(f, a, b, x0, f_x0, n):
    if x0 != a:
        raise ValueError('Must be equal')        
    h = (b - a) / n
    x = np.empty(n + 1)
    y = np.empty(n + 1)
    x[0] = x0
    y[0] = f_x0
    x[1] = x[0] + h
    y[1] = y[0] + h * f(x[0], y[0])
    for i in range(1, n):
        predictor = y[i] + h / 2 * (3 * f(x[i], y[i]) - f(x[i - 1], y[i - 1]))
        x[i + 1] = x[i] + h
        y[i + 1] = y[i] + h / 2 * (f(x[i], y[i]) + f(x[i + 1], predictor))        
    return x, y

def adams_chedule(adams_x, adams_y, a_x_2, a_y_2):
	print(' x[i]|    y[i]      |    ~y[i]     |   delta[i]   |')
	for i in range(len(adams_x)-1):
		if i & 1 == 0:
			print('|{0}| {1} | {2} | {3} |'.format(round(adams_x[i],3),"{0:0.10f}".format(adams_y[i]), "{0:0.10f}".format(a_y_2[i // 2]),\
				"{0:0.10f}".format(abs(a_y_2[i // 2] - adams_y[i]))))
		else:
			print('|{0}| {1} |{2}|{3}|'.format(round(adams_x[i],3), "{0:0.10f}".format(adams_y[i]), "              ", "              "))

	plt.plot(adams_x, adams_y, label='h')
	plt.plot(a_x_2, a_y_2, label='2 * h')
	plt.title('Кривая методом Адамса')
	plt.legend()
	plt.grid()
	plt.show()

def ode_method_eiler(func, a, b, x0, f_x0, n):
    if x0 != a:
        raise ValueError('Must be equal')        
    h = (b - a) / n
    x = np.empty(n + 1, float)
    y = np.empty(n + 1, float)
    x[0] = x0
    y[0] = f_x0    
    for i  in range(n):
        y[i + 1] = y[i] + h * func(x[i], y[i])
        x[i + 1] = x[i] + h   
    return x, y

def eiler_chedule(eiler_x, eiler_y, e_x_2, e_y_2):
	print(' x[i]|    y[i]      |    ~y[i]     |   delta[i]   |')
	for i in range(len(eiler_x)-1):
		if i & 1 == 0:
			print('|{0}| {1} | {2} | {3} |'.format(round(eiler_x[i],3),"{0:0.10f}".format(eiler_y[i]), "{0:0.10f}".format(e_y_2[i // 2]),\
				"{0:0.10f}".format(abs(e_y_2[i // 2] - eiler_y[i]))))
		else:
			print('|{0}| {1} |{2}|{3}|'.format(round(eiler_x[i],3), "{0:0.10f}".format(eiler_y[i]), "              ", "              "))

	plt.plot(eiler_x, eiler_y, label='h')
	plt.plot(e_x_2, e_y_2, label='2 * h')
	plt.title('Кривая методом Эйлера')
	plt.legend()
	plt.grid()
	plt.show()

def exact_chedule(func_solution, range_x):
	plt.plot(range_x, func_solution(range_x))
	plt.title('Тoчное решение')
	plt.grid()
	plt.show()

if __name__ == "__main__":
	try:
		main()
	except ValueError as ve:
		print(ve)
	except Error as er:
		print(er)