from typing import Callable

from numpy import ndarray, array, linspace
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
	EPS = 1e-6

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
		# mesh = linspace(self.leftBound.x, self.rightBound.x, N)
		# step: float = (self.rightBound.x - self.leftBound.x) / N

	def solve(self):
		eqSystem: ndarray = ndarray((self.N, self.N), dtype=float)
		free: ndarray = ndarray(self.N, dtype=float)
		delta: ndarray = ndarray(self.N, dtype=float)


 		for i in range(1, self.N-1):
			...