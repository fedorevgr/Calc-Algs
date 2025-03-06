from .Table import ABOBA
from .Multydimetia import MultidimensionalInterpolatorInator as MII
from .Multydimetia import Method
from pprint import pprint

pprint(ABOBA)
pprint(MII.interp(ABOBA, [1.4, 1.4, 1.4], Method.Spline))
