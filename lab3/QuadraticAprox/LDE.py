from fontTools.subset.svg import xpath
from pandas import DataFrame
from numpy.linalg import solve
from numpy import ndarray, linspace

from math import pow, exp

from typing import Final,Callable


type _fX = Callable[[float],float]


class Approx:
	_coefficients: ndarray[float]
	_powShift: int = 2
	_U0 = lambda x: 1-x
	_U0D = lambda x: -1
	_U0DD = lambda x: 0

	@staticmethod
	def _func(k:int) -> Callable[[float],float]:
		#k += Approx._powShift
		return lambda x:  pow(1-x, k) * pow(x, 2) # pow((-(x - 1)), k)

	@staticmethod
	def _funcD(k: int) -> Callable[[float], float]:
		#k += Approx._powShift
		if k == 0:
			return lambda x:  2 * x
		return lambda x: -1 * x * ((k + 2) * x - 2) * pow(1 - x, k-1) # pow((-(x - 1)), k - 1) * k * -1

	@staticmethod
	def _funcDD(k: int) -> Callable[[float], float]:
		#k += Approx._powShift
		if k == 1:
			return lambda x:  2 - 6 * x
		if k == 0:
			return lambda x:  2

		return lambda x: pow(1-x, k-2) * (
			(k * k + 3 * k + 2) * x * x - 4 * (k + 1) * x + 2
		)  # pow((-(x - 1)), k - 2) * k * (k - 1)

	@staticmethod
	def U(k: int, p: Callable[[float], float], g: Callable[[float], float]) -> Callable[[float],float]:
		return lambda x: Approx._funcDD(k)(x) + \
							p(x) * Approx._funcD(k)(x) + \
								g(x) * Approx._func(k)(x)

	@staticmethod
	def U0(p: Callable[[float], float], g: Callable[[float], float]) -> Callable[[float], float]:
		return lambda x: Approx._U0DD(x) + \
						 p(x) * Approx._U0D(x) + \
						 g(x) * Approx._U0(x)

	def __init__(self, points: ndarray[float], N: int, p: _fX, g: _fX, f: _fX) -> None:

		eqSystem: DataFrame = DataFrame(index=range(N), columns=range(N), dtype=float)
		B: ndarray = ndarray(N, dtype=float)

		for t, row in eqSystem.iterrows():
			tPower = t + 0
			for k in range(N):
				kPower = k + 0
				row[k] = sum(
					Approx.U(tPower, p, g)(x) * Approx.U(kPower, p, g)(x)
					for x in points
				)

			B[t] = sum(
				Approx.U(tPower, p, g)(x) * (f(x) - Approx.U0(p, g)(x))
				for x in points
			)

		self._coefficients = solve(eqSystem, B)

	def __call__(self, x: float) -> float:
		return Approx._U0(x) + sum([C * self._func(k)(x) for k, C in enumerate(self._coefficients)])

	def coefficients(self) -> ndarray:
		return self._coefficients