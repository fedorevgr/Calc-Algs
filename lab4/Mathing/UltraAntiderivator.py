from typing import Callable

from numpy import ndarray, array, linspace
from pandas import DataFrame

type f_xT = Callable[[float], float]


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
	leftBound: Point = Point(0, 1)
	rightBound: Point = Point(1, 3)

	def __init__(self, N: int):
		"""
		F(y_n-1, y_n, y_n+1) = y_n-1 - 2y_n + y_n+1 - f(x_n, y_n) * h^2
		f(x, y) = (x^3 + y^3) * h^2
		DF x dY = -F     D - div
		Y += dY
		Y = (y_n-1, y_n, y_n+1)
		"""
		mesh = linspace(self.leftBound.x, self.rightBound.x, N)
		step: float = (self.rightBound.x - self.leftBound.x) / N
