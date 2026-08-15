from dataclasses import dataclass, field
from common.symmetry import (
    encrypt_cluster,
    decrypt_cluster,
    _drop_duplicates,
)

@dataclass
class Cluster:
    origin: tuple[
        tuple[float, ...], ...
    ] = field(init=False)
    bodies: int = field(init=False)
    slides: tuple[
        tuple[tuple[float, ...], ...]
        , ...
    ] = field(init=False)
    subclusters: tuple[
        tuple[tuple[float, ...], ...]
        , ...
    ] = field(init=False)

    def __init__(self, origin) -> None:
        self.origin = origin
        self.bodies = len(self.origin)

        whole_slides = tuple(
            tuple(
                tuple(
                    pt[i] - bass[i]
                    for i in range(len(pt))
                ) for pt in self.origin
            ) for bass in self.origin
        )
        en = tuple(encrypt_cluster(i, 5, 6) for i in whole_slides)
        unique: tuple[str, ...] = _drop_duplicates(en)
        self.slides = tuple(
            decrypt_cluster(i, 5, 6)
            for i in unique
        )

        single_pointouts = tuple(
            tuple(
                pt for m, pt in enumerate(self.origin)
                if n != m
            ) for n in range(len(self.origin))
        )
        en = tuple(encrypt_cluster(i, 5, 6) for i in single_pointouts)
        unique = _drop_duplicates(en)
        self.subcluster = tuple(
            decrypt_cluster(i, 5, 6)
            for i in unique
        )
