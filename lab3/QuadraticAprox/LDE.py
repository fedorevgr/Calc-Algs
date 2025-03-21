from pandas import DataFrame
from numpy.linalg import solve
from numpy import ndarray

from math import pow

from typing import Final,Callable


class Approx:
	_coefficients: ndarray[float]
	_N: Final[int] = 2

	def __init__(self, data: DataFrame, p, g, f):
		"""
		data: DataFrame - x, y
		"""
		l = lambda x: x * x
		lStrih = lambda x: 2 * x
		lStrihShtrih = lambda x: 2

		eqSystem: DataFrame = DataFrame(index=range(self._N), columns=range(self._N), dtype=float)
		vals: ndarray = ndarray(self._N, dtype=float)

		for i, row in data.iterrows():
			x = row.x
			for m in range(self._N):
				k = m + 1
				eqSystem.iloc[m, i] = (k*(k-1)*pow(x, k-2) if x else 0) + p(x)*k*pow(x, k-1) + g(x)*pow(x, k)

			vals[i] = f(x) - lStrihShtrih(x) - p(x)*lStrih(x) - g(x)*l(x)

		self._coefficients = solve(eqSystem, vals)

	def __call__(self, x: float,  y: float) -> float:
		return self._coefficients[0] + self._coefficients[1] * x + self._coefficients[2] * y

	def __str__(self) -> str:
		return f"({self._coefficients[0]:g}) + ({self._coefficients[1]:g}) * x + ({self._coefficients[2]:g}) * y"

	def coefficients(self) -> ndarray:
		return self._coefficients