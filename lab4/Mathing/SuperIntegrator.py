from math import isclose
from typing import Callable
from numpy import arange, linspace, ndarray, sign, vectorize


type f_xT = Callable[[float], float]


class Point:
	x: float
	y: float

	def __init__(self, x: float, y: float):

		self.x = x
		self.y = y

class Solver:
	EPS = 1e-9

	STEP: float = 1e-5

	def __init__(self, func: f_xT):
		self.func = func

	def simpson(self, a, b) -> float:
		if isclose(a, b, abs_tol=1e-9):
			return 0

		step: float = self.STEP * sign(b - a)
		args: ndarray[float] = arange(a, b + step, step, dtype=float)
		vals: ndarray[float] = vectorize(self.func)(args)

		return step * (
			self.func(a) +
			2 * sum(map(self.func, args[2::2])) +
			4 * sum(map(self.func, args[1::2])) +
			self.func(b)
		) / 3

		#return sum(vals[i-1] + 4 * vals[i] + vals[i+1] for i in range(1, len(vals)-1, 2)) * step / 3


	def trapezes(self, a: float, b: float) -> float:
		if isclose(a, b, abs_tol=1e-9):
			return 0

		step: float = self.STEP * sign(b - a)
		args: ndarray[float] = arange(a, b + step, step, dtype=float)

		summ = sum(map(self.func, args))
		return (summ - self.func(a) / 2 - self.func(b) / 2) * step


	def solve(self, a: float, eq: float, between: tuple[float, float], meth: Callable[[float, float], float]) -> float | None:
		left: Point = Point(between[0], meth(a, between[0]) - eq)
		right: Point =  Point(between[1], meth(a, between[1]) - eq)

		if left.y * right.y > 0:
			return None

		middle: Point

		while True:
			mid = (left.x + right.x) / 2
			middle = Point(mid, meth(a, mid) - eq)


			if middle.y * right.y < 0:
				left = middle
			else:
				right = middle

			if isclose(right.x, left.x, rel_tol=self.EPS):
				break

		return right.x