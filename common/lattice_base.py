from dataclasses import dataclass

@dataclass
class Vect:
    v: tuple[float, ...]

@dataclass
class LatticeBasis:
    basis: tuple[Vect, ...]

    def __post_init__(self):
        s = {0:1, 1:0, 2:0}
        l = {0:2, 1:2, 2:1}
        self._adjugate = list(
            list(
                self.basis[s[i]].v[s[j]] * self.basis[l[i]].v[l[j]]
                - self.basis[l[i]].v[s[j]] * self.basis[s[i]].v[l[j]]
                for j in range(3)
            )
            for i in range(3)
        )
        self.det = sum(
            (self.basis[0].v[i] * self._adjugate[0][i])*(-1.)**float(i)
            for i in range(3)
        )

    def inverse(self) -> "LatticeBasis":
        return LatticeBasis(basis=tuple(
            Vect(tuple(
                self._adjugate[j][i]/self.det * (-1.) ** float(i+j)
                for j in range(3)
            ))
            for i in range(3)
        ))

