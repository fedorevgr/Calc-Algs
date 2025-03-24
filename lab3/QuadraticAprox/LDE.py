from pandas import DataFrame
from numpy.linalg import solve
from numpy import ndarray, linspace

from math import pow

from typing import Final,Callable


type _fX = Callable[[float],float]


class Approx:
	_coefficients: ndarray[float]
	_N: Final[int] = 2
	_segments: int = 100

	def __init__(self, data: DataFrame, p: _fX, g: _fX, f: _fX) -> None:
		"""
		data: DataFrame - x, y
		"""
		h: float = (data[1, "x"] + data[0, "x"]) / self._segments
		x = linspace(data[0, "x"], data[1, "x"], self._segments, dtype=float)

		for i in range(1, self._segments):
			y[0].append(
				(
					(h ** 2 * f(x[i]) - (1.0 - (h / 2) * p(x[i])) * y[0][i - 1] - (h ** 2 * g(x[i]) - 2) * y[0][i]) /
					(1 + h / 2 * p(x[i]))
				)
			)
			y[1].append(
				(
					(-(1 - h / 2 * p(x[i])) * y[1][i - 1] - (h ** 2 * g(x[i]) - 2) * y[1][i]) /
					(1 + h / 2 * p(x[i]))
				)
			)

	def __call__(self, x: float,  y: float) -> float:
		return self._coefficients[0] + self._coefficients[1] * x + self._coefficients[2] * y

	def __str__(self) -> str:
		return f"({self._coefficients[0]:g}) + ({self._coefficients[1]:g}) * x + ({self._coefficients[2]:g}) * y"

	def coefficients(self) -> ndarray:
		return self._coefficients