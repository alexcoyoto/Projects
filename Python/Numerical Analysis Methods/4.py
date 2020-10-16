#!/usr/bin/env python3
import numpy as np
from numpy.linalg import *
import math

def main():
	np.set_printoptions(formatter={'float': '{: 0.3f}'.format})
	with open('file', 'r') as f:
		matrix = [float(num) for num in f.read().split()]
		a = np.array(matrix).reshape(int(len(matrix)**0.5), int(len(matrix)**0.5) + 1)
	print('Расширенная матрица системы: \n',a)
	if (if_symmetr([row[:-1] for row in a]) == False):
		matrix_A = np.array([row[:-1] for row in a]).transpose() @ [row[:-1] for row in a]
		print('\nСимметричная матрица A:')
		for i in range(len(a)):
			print(matrix_A[i])
	else:
		matrix_A = np.array([row[:-1] for row in a])
	find_eigens(matrix_A, 0.02)
	print("\nПроверка")
	print('Собственные значения:\n', np.linalg.eig(matrix_A)[0])
	print('Собственные векторы:\n', np.linalg.eig(matrix_A)[1])

def if_symmetr(A):
	for i in range(len(A)):
		for j in range(len(A)):
			if A[i][j] == A[j][i]:
				continue
			else:
				return False 
	return True

def upper_max(A):
	MAX = A[0][1]
	pos = 0, 1
	for i in range(len(A)):
		for j in range(i + 1, len(A)):
			if abs(A[i][j]) > MAX:
				MAX = abs(A[i][j])
				pos = i, j
	return MAX, pos

def find_eigens(A, eps):
	X = np.eye(len(A))
	count = 0
	while upper_max(A)[0] > eps:
		print('Шаг ', count)
		m, [l, r] = upper_max(A)
		fi = 1/2 * math.atan(2 * m / (A[l][l] - A[r][r]))
		print('fi =', fi)
		
		H = np.eye(len(A))
		H[r][r] = H[l][l] = math.cos(fi)
		H[l][r] = -math.sin(fi)
		H[r][l] = - H[l][r]
		print('H =\n', H)
		X = np.dot(X,H)
		A = np.dot(np.dot(H.transpose(), A), H)
		print('A =\n', A)

		count += 1
	print('\nСобственные значения:\n', A.diagonal())
	print('\nСобственные векторы: \n', X)

if __name__ == '__main__':
	main()