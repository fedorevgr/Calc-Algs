from numpy import ndarray
from pandas import DataFrame
from numpy.linalg import det, solve
from math import pow

from typing import Callable

from . import valT


type _funcT = Callable[[float], float]


class Approx:
	_coefficients: ndarray

	_fs: list[_funcT]

	def __init__(self, data: DataFrame, power: int = 0):
		"""
		power of polynomial
		a_0, a_1, ..., a_power

		data: i, x_i, y_i, p_i
		"""
		self._fs = [Approx.approxFunc(i) for i in range(power)]

		eqSystem: DataFrame = DataFrame(index=range(power), columns=list(range(power)), dtype=float)
		vals: ndarray = ndarray(power, dtype=float)

		for m, row in eqSystem.iterrows():  # m = 0..n
			for k in range(power):
				eqSystem.iloc[m,k] = sum(
					row.weight * self._fs[k](row.x) * self._fs[m](row.x)
					for i, row in data.iterrows()
				)
			vals[m] = sum(row.weight * row.y * self._fs[m](row.x) for i, row in data.iterrows())

		self._coefficients = solve(eqSystem, vals)


	@staticmethod
	def approxFunc(i: int) -> _funcT:
		return lambda x: pow(x, i)

	def __call__(self, x: float) -> float:
		return sum(a * f(x) for a, f in zip(self._coefficients, self._fs))

	def __str__(self) -> str:
		return "+".join(f"({a:g}) * (x ^ {k})" for k, a in enumerate(self._coefficients))

	def coefficients(self) -> ndarray:
		return self._coefficients