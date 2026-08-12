import math
from typing import Literal
from dataclasses import dataclass, field
from common.matrix import inverse

class CreatedErrors(Exception):
    pass

@dataclass
class Lattice:
    A: tuple[float, float, float] = field(init=False)
    B: tuple[float, float, float] = field(init=False)
    C: tuple[float, float, float] = field(init=False)
    alpha: float = field(init=False)
    beta:  float = field(init=False)
    gamma: float = field(init=False)
    symms: int = field(init=False)
    basis: tuple[
        tuple[float, float, float],
        tuple[float, float, float],
        tuple[float, float, float]
    ] = field(init=False)
    invs: tuple[
        tuple[float, float, float],
        tuple[float, float, float],
        tuple[float, float, float]
    ] = field(init=False)
    bravais: list[Literal["P", "C", "I", "F"]] = field(init=False)
    japanese: str = field(init=False)

    def _check_lattice_params(self) -> bool:
        na = math.sqrt(sum(self.A[i] ** 2. for i in range(3)))
        nb = math.sqrt(sum(self.B[i] ** 2. for i in range(3)))
        nc = math.sqrt(sum(self.C[i] ** 2. for i in range(3)))
        # calc-alpha
        prod = sum(self.B[i] * self.C[i] for i in range(3))
        dgr_a = math.acos( prod/nb/nc ) / math.pi * 180.
        # calc-beta
        prod = sum(self.A[i] * self.C[i] for i in range(3))
        dgr_b = math.acos( prod/na/nc ) / math.pi * 180.
        # calc-gamma
        prod = sum(self.A[i] * self.B[i] for i in range(3))
        dgr_c = math.acos( prod/na/nb ) / math.pi * 180.
        return all((i < 1.0e-12 for i in (
            abs(self.alpha - dgr_a),
            abs(self.beta - dgr_b),
            abs(self.gamma - dgr_c)
        )))

    def _calc_baseC(self, c, al, bt, g):
        al *= math.pi / 180.
        bt *= math.pi / 180.
        g  *= math.pi / 180.
        return (
            c * math.cos(bt),
            c * (math.cos(al) - math.cos(bt) * math.cos(g)) / math.sin(g),
            c * math.sqrt(
                2. * math.cos(al) * math.cos(bt) * math.cos(g)
                - math.cos(al)**2
                - math.cos(bt + g) * math.cos(bt - g)
            ) / math.sin(g)
        )

@dataclass
class Cubic(Lattice):
    a: float

    def __post_init__(self): # type: ignore[override]
        a = self.a
        self.A = (a, 0., 0.)
        self.B = (0., a, 0.)
        self.C = (0., 0., a)
        self.alpha = 90.
        self.beta = 90.
        self.gamma = 90.
        self.symms = 48
        self.basis = (self.A, self.B, self.C)
        self.invs = inverse(self.basis)
        self.bravais = ["P", "I", "F"]
        self.japanese = "立方晶"

@dataclass
class Hexagonal(Lattice):
    a: float
    c: float

    def __post_init__(self): # type: ignore[override]
        a = self.a
        c = self.c
        self.A = (a, 0., 0.)
        self.B = (-a/2., a*math.sqrt(0.75), 0.)
        self.C = (0., 0., c)
        self.alpha = 90.
        self.beta = 90.
        self.gamma = 120.
        self.symms = 24
        self.basis = (self.A, self.B, self.C)
        self.invs = inverse(self.basis)
        self.bravais = ["P"]
        self.japanese = "六方晶"

@dataclass
class Tetragonal(Lattice):
    a: float
    c: float

    def __post_init__(self): # type: ignore[override]
        a = self.a
        c = self.c
        if a == c:
            CreatedErrors("Same parameters A and C were given. It's Cubic.")
        self.A = (a, 0., 0.)
        self.B = (0., a, 0.)
        self.C = (0., 0., c)
        self.alpha = 90.
        self.beta = 90.
        self.gamma = 90.
        self.symms = 24
        self.basis = (self.A, self.B, self.C)
        self.invs = inverse(self.basis)
        self.bravais = ["P", "I"]
        self.japanese = "直方晶"

@dataclass
class Orthorhombic(Lattice):
    a: float
    b: float
    c: float

    def __post_init__(self): # type: ignore[override]
        a = self.a
        b = self.b
        c = self.c
        if len(set((a,b,c))) != 3:
            CreatedErrors("Same value was detected in A/B/C. It's Cubic or Tetragonal.")
        self.A = (a, 0., 0.)
        self.B = (0., b, 0.)
        self.C = (0., 0., c)
        self.alpha = 90.
        self.beta = 90.
        self.gamma = 90.
        self.symms = 24
        self.basis = (self.A, self.B, self.C)
        self.invs = inverse(self.basis)
        self.bravais = ["P", "C", "I", "F"]
        self.japanese = "斜方晶"

@dataclass
class Trigonal(Lattice):
    a: float
    alpha: float

    def __post_init__(self): # type: ignore[override]
        a = self.a
        alpha = self.alpha
        if alpha <= 0. or 120. <= alpha:
            CreatedErrors("Given angle value is out of range.")
        c = a * math.cos(alpha / 180. * math.pi)
        s = a * math.sin(alpha / 180. * math.pi)
        self.A = (a, 0., 0.)
        self.B = (c, s,  0.)
        self.C = self._calc_baseC(a, alpha, alpha, alpha)
        self.alpha = alpha
        self.beta = alpha
        self.gamma = alpha
        self.symms = 24
        self.basis = (self.A, self.B, self.C)
        self.invs = inverse(self.basis)
        self.bravais = ["P"]
        self.japanese = "三方晶"

@dataclass
class Monoclinic(Lattice):
    a: float
    b: float
    c: float
    beta: float

    def __post_init__(self): # type: ignore[override]
        a = self.a
        b = self.b
        c = self.c
        beta = self.beta
        if beta == 90.:
            print("90. deg. was given, but it is Orthorhombic.")
        self.A = (a, 0., 0.)
        self.B = (0., b, 0.)
        self.C = (c*math.cos(beta*math.pi/180.), 0., c*math.sin(beta*math.pi/180.))
        self.alpha = 90.
        self.beta = beta
        self.gamma = 90.
        self.symms = 24
        self.basis = (self.A, self.B, self.C)
        self.invs = inverse(self.basis)
        self.bravais = ["P", "C"]
        self.japanese = "単斜晶"

@dataclass
class Triclinic(Lattice):
    a: float
    b: float
    c: float
    alpha: float
    beta: float
    gamma: float

    def __post_init__(self): # type: ignore[override]
        a = self.a
        b = self.b
        c = self.c
        alpha = self.alpha
        beta = self.beta
        gamma = self.gamma
        # range of alpha is limited by beta and gamma.
        bt = beta*math.pi/180.
        g = gamma*math.pi/180.
        theta = math.acos(math.cos(bt+g))/math.pi * 180
        phi = math.acos(math.cos(bt-g))/math.pi * 180
        if phi < alpha < theta:
            pass
        else:
            CreatedErrors("No allowed values for alpha.")
        self.A = (a, 0., 0.)
        self.B = (b*math.cos(g), b*math.sin(g), 0.)
        self.C = self._calc_baseC(a, alpha, beta, gamma)
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.symms = 2
        self.basis = (self.A, self.B, self.C)
        self.invs = inverse(self.basis)
        self.bravais = ["P"]
        self.japanese = "斜方晶"
