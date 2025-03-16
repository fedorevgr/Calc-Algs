from pandas import DataFrame
from numpy import ndarray, float64
from typing import Final
from numpy.linalg import solve


from . import valT


class Approx:
	_coefficients: ndarray[float]
	_N: Final[int] = 3

	def __init__(self, data: DataFrame):
		"""
		:param data: i, x, y, z, weight
		:param power:
		"""
		eqSystem: DataFrame = DataFrame(index=range(self._N), columns=range(self._N), dtype=float)
		vals: ndarray = ndarray(self._N, dtype=float)

		eqSystem.loc[0, :] = [sum(data.weight), sum(data.weight * data.x), sum(data.weight * data.y)]
		vals[0] = sum(data.weight * data.z)

		eqSystem.loc[1, :] = [sum(data.weight * data.x), sum(data.weight * data.x * data.x), sum(data.weight * data.y * data.x)]
		vals[1] = sum(data.weight * data.z * data.x)

		eqSystem.loc[2, :] = [sum(data.weight * data.y), sum(data.weight * data.x * data.y),
							  sum(data.weight * data.y * data.y)]
		vals[2] = sum(data.weight * data.z * data.y)

		self._coefficients = solve(eqSystem, vals)

	def __call__(self, x: float,  y: float) -> float:
		return self._coefficients[0] + self._coefficients[1] * x + self._coefficients[2] * y

	def __str__(self) -> str:
		return f"({self._coefficients[0]:g}) + ({self._coefficients[1]:g}) * x + ({self._coefficients[2]:g}) * y"

	def coefficients(self) -> ndarray:
		return self._coefficients