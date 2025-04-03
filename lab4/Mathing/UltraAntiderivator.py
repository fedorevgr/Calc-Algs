from math import isclose
from typing import Callable

from numpy import ndarray, array, linspace, vectorize, concatenate, zeros
from numpy.linalg import solve
from pandas import DataFrame


type f_xT = Callable[[float], float]
type F_XT = Callable[[float, float], float]


class Point:
	def __init__(self, x: float, y: float):
		self.x = x
		self.y = y


class McQueen:
	@staticmethod
	def zoomZoomZoom(eq: DataFrame) -> ndarray:
		return array([1])


class Solve:
	"""
	Solves the equation:
		u''(x) = f(x, y)
	"""
	EPS = 1e-3
	MAX_OP = 100

	isClose: Callable[[ndarray, ndarray], ndarray] = vectorize(lambda x, y: isclose(x, y, rel_tol=Solve.EPS))

	leftBound: Point
	rightBound: Point

	f: F_XT
	fD: F_XT

	N: int

	def __init__(self, N: int, F: F_XT, deriveF: F_XT, limitCond: tuple[Point, ...]) -> None:
		"""
		F(y_n-1, y_n, y_n+1) = y_n-1 - 2y_n + y_n+1 - f(x_n, y_n) * h^2
		f(x, y) = (x^3 + y^3) * h^2
		DF x dY = -F     D - div
		Y += dY
		Y = (y_n-1, y_n, y_n+1)
		y0 = 1
		yN = 3
		"""
		self.leftBound = limitCond[0]
		self.rightBound = limitCond[1]

		self.f = F
		self.fD = deriveF

		self.N = N

	def solve(self, firstApproxFunc: f_xT):
		X = linspace(self.leftBound.x, self.rightBound.x, self.N)
		step: float = (self.rightBound.x - self.leftBound.x) / self.N
		Y: ndarray = vectorize(firstApproxFunc)(X)
		nextY: ndarray = ndarray(self.N, dtype=float)

		eqSystem: ndarray = zeros((self.N-2, self.N-2), dtype=float)

		free: ndarray = zeros(self.N-2, dtype=float)
		delta: ndarray = zeros(self.N-2, dtype=float)

		eqSystem[0][1] = 1
		eqSystem[-1][-2] = 1
		for i in range(1, self.N-2-1):
			eqSystem[i][i-1] = 1
			eqSystem[i][i+1] = 1

		for _ in range(self.MAX_OP):


			for rowI in range(self.N-2):
				eqSystem[rowI][rowI] = -(2 + self.fD(X[rowI+1], Y[rowI+1]) * step * step)

			free = -1 * (Y[:-2] - 2 * Y[1:-1] + Y[2:] - vectorize(self.f)(X, Y)[1:-1]  * step * step)

			delta = concatenate(([0], solve(eqSystem, free), [0]))

			nextY = Y + delta
			if all(self.isClose(nextY, Y)):
				break
			Y = nextY

		return X, nextY