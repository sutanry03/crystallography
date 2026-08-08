import math
from dataclasses import dataclass

@dataclass
class DataSamples:
    sample: list[float]

    def _moments(self, n_th: int) -> list[float]:
        moments: list[float] = [0.] * n_th
        for i in self.sample:
            for j in range(n_th):
                moments[j] += i**float(j+1)
        return list(e/len(self.sample) for e in moments)

    def alphas(self, n_th: int) -> list[float]:
        if n_th < 1:
            return []
        ms = self._moments(n_th)
        µ = ms[0]
        V = ms[1] - ms[0]**2.
        sgm = V**0.5
        result = [µ, sgm]
        if n_th <= 2:
            return result[:n_th]
        for n in range(3, n_th + 1):
            an = sum(
                (-1.)**float(k) * self._comb(n, k) * µ**float(k) * ms[n-k-1]
                for k in range(n-1)
            )
            an += float((-1.)**(n-1) * (n -1)) * µ ** float(n)
            an /= sgm**float(n)
            result.append(an)
        return result

    def _comb(self, n: int, k: int) -> float:
        c = math.factorial(n) // math.factorial(n - k) // math.factorial(k)
        return float(c)

    def z(self) -> list[float]:
        µ, sgm = self.alphas(2)
        return list((x-µ)/sgm for x in self.sample)
