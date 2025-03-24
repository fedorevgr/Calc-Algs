from pandas import DataFrame
from numpy import ndarray, float64, sqrt
from typing import Final, Iterable, Tuple, Callable
from numpy.linalg import solve

from math import pow


from . import valT

class Approx:
	_coefficients: ndarray[float]
	_POWER: int

	@staticmethod
	def iterate(power: int) -> Iterable[tuple[int, ...]]:
		r: int = 0
		for i in range(power + 1):
			for j in range(power - i + 1):
				yield r, i, j
				r += 1

	@staticmethod
	def forPLength(l: int) -> int:
		return (-1 + sqrt(1 + 8 * l)) // 2

	@staticmethod
	def Xvector(i: int, j: int) -> Callable[[float, float, float], float]:
		return lambda _1, _2, _3: pow(_1, i) * pow(_2, j) * pow(_3, 3 - i - j)

	def __init__(self, data: DataFrame, power: int) -> None:
		"""
		Vector: (x, y, 1)
		:param data: i, x, y, z, weight
		:param power: polynom power
		"""
		self._POWER = power
		ROWS = (power + 2) * (power + 1) // 2

		eqSystem: DataFrame = DataFrame(index=range(ROWS), columns=range(ROWS), dtype=float)
		vals: ndarray = ndarray(ROWS, dtype=float)

		for rowIndex, I, J in Approx.iterate(power):
			XIJ = Approx.Xvector(I, J)

			for colIndex, i, j in Approx.iterate(power):
				eqSystem.iloc[rowIndex, colIndex] = sum(
					rowM.weight * XIJ(rowM.x, rowM.y, 1) * Approx.Xvector(i, j)(rowM.x, rowM.y, 1)
					for m, rowM in data.iterrows()
				)

			vals[rowIndex] = sum(
				rowM.weight * XIJ(rowM.x, rowM.y, 1) * rowM.z
					for m, rowM in data.iterrows()
			)

		self._coefficients = solve(eqSystem, vals)

	def __call__(self, x: float,  y: float) -> float:
		return sum(
			self._coefficients[coefI] * Approx.Xvector(i, j)(x, y, 1)
			for coefI, i, j in Approx.iterate(self._POWER)
		)

	def __str__(self) -> str:
		return " + ".join(
			f"({self._coefficients[coefI]}) * (x ^ {i}) * (y ^ {j})"
			for coefI, i, j in Approx.iterate(self._POWER)
		)

	def coefficients(self) -> ndarray:
		return self._coefficients