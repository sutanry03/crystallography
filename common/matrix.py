from dataclasses import dataclass
from typing import Any

class CreatedErrors(Exception):
    pass

def get_adjugate_matrix(
    matrix: tuple[tuple[float, ...], ...]
) -> tuple[tuple[Any, ...], ...]:
    dim = len(matrix)
    if dim == 1:
        return matrix
    if dim < 1:
        raise CreatedErrors("")
    return tuple(tuple(tuple(
        tuple(
            vj
            for nj, vj in enumerate(vi)
            if nj != j
        )
        for ni, vi in enumerate(matrix)
        if ni != i
    ) for j in range(dim) ) for i in range(dim) )

def get_det(matrix) -> float:
    result: list[list[Any]] = []
    for line in get_adjugate_matrix(matrix):
        result.append(list())
        for adjugate in line:
            adjugate = (
                get_det(adjugate)
                if len(adjugate) > 1
                else adjugate[0][0]
            )
            result[-1].append(adjugate)

    return sum(
        matrix[0][i] * (
            get_det(result[0][i])
            if not isinstance(result[0][i], float)
            else result[0][i]
        ) * (-1.) ** float(i)
        for i in range(len(result))
    )

def inverse(matrix) -> tuple[tuple[float, ...], ...]:
    dim = len(matrix)
    det = get_det(matrix)
    result: list[list[Any]] = []
    for i in range(dim):
        result.append(list())
        for j in range(dim):
            tmp = get_adjugate_matrix(matrix)[j][i]
            tmp = get_det(tmp) /det * (-1.) ** float(i+j)
            result[-1].append(tmp)
    return tuple(tuple(j for j in i) for i in result)
