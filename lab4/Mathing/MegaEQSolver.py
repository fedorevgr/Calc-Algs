from typing import Callable

from math import isclose
from numpy import ndarray
from numpy.linalg import solve, matmul
from pandas import DataFrame


type vectorT = ndarray
type f_xT = Callable[[float], float]
type gradT = Callable[[vectorT], vectorT]
type f_nxT = Callable[[vectorT], float]


class ExtrapolationError(Exception):
	def __init__(self, eVal: vectorT):
		self.args = ("Value extrapolated", eVal)


class Solver:
	"""
	Implements Newton's method to solve equation
	Grad:
	d/dx d/dy d/dz
	"""
	EPS = 1e-3
	EXTRAPOLATION_FACTOR = 10

	def __init__(self, func: list[f_nxT], grad: list[gradT]):
		self.func = func
		self.grad = grad

	def solve(self, startApprox: vectorT):
		prevApprox: vectorT = startApprox
		nextApprox: vectorT
		delta: vectorT

		eqSystem = ndarray((len(startApprox), len(startApprox)), dtype=float)
		free: ndarray = ndarray(len(startApprox), dtype=float)

		n = 0
		while True:
			n+= 1
			for i, fg in enumerate(zip(self.func, self.grad)):
				eqSystem[i] = fg[1](prevApprox)
				free[i] = -1 * fg[0](prevApprox)

			delta = solve(eqSystem, free)
			nextApprox = prevApprox + delta

			if all(map(lambda x: isclose(*x, rel_tol=self.EPS), zip(prevApprox, nextApprox))):
				break
			if not all(map(lambda x: abs(x) < self.EXTRAPOLATION_FACTOR, delta)):
				raise ExtrapolationError(nextApprox)

			prevApprox = nextApprox

		return nextApprox, n
