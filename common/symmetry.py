import math
from collections.abc import Iterable
from typing import Any

def _set_params(
    encrypting_exponent: int = 5,
    precision: int = 6,
    access_number: int = 48, #chr(48) == '0'
):
    cryption_dict = {
        i:chr(i)
        for i in range(
            access_number,
            access_number + 2 ** encrypting_exponent
        )
    }
    decryption_dict = {v:k for k,v in cryption_dict.items()}

    target = precision*math.log(10,2) / float(encrypting_exponent)
    lower = math.floor(target)
    upper = math.ceil(target)
    assert upper == lower + 1
    return lower, upper, cryption_dict, decryption_dict, access_number

def convert(r: float, N: int, P: int) -> str:
    """ 小数部分P桁を文字化. 2^(N*l) < 10^P < 2^(N*u) """
    l, u, cd, dd, an = _set_params(N, P)
    r = round(r*10.**P,0)
    a = ""
    for i in range(u):
        r, b = (r//(2**N), r%(2**N))
        a += cd[b+an]
    return a[::-1]

def encrypt_vector(vec: tuple[float, ...], N: int, P: int) -> str:
    """ ベクトルの文字化。小数部P桁精度, 整数部の絶対値は2^(N*u-1)未満 """
    l, u, cd, dd, an = _set_params(N, P)
    floor: int = 2**(N*u-1)
    k = ""
    for i in vec:
        i = float(i) + float(abs(floor))
        r = int(i)
        k0 = ""
        for j in range(u):
            r, b = (r//(2**N), r%(2**N))
            k0 += cd[b+an]
        k += k0[::-1] + convert(i - int(i), N, P)
    return k

def decrypt_vector(
    crypted_vector: str,
    N: int,
    P: int
) -> tuple[float, ...]:
    """ 文字化されたベクトルの複製(小数部P桁精度, 整数部の絶対値は2^(N*u-1)未満) """
    l, u, cd, dd, an = _set_params(N, P)
    decrypting = list(dd[i]-an for i in crypted_vector)
    (ix,dx), (iy, dy), (iz,dz) = list(
        [
            decrypting[u*2*i : u*(2*i+1)][::-1],
            decrypting[u*(2*i+1) : u*(2*i+2)][::-1]
        ]
        for i in range(3)
    )
    x = sum((2**(N*i))*ix[i] for i in range(u)) - 2 ** (N*u-1)
    y = sum((2**(N*i))*iy[i] for i in range(u)) - 2 ** (N*u-1)
    z = sum((2**(N*i))*iz[i] for i in range(u)) - 2 ** (N*u-1)
    x += sum((2**(N*i))*dx[i] for i in range(u)) / 10.**P
    y += sum((2**(N*i))*dy[i] for i in range(u)) / 10.**P
    z += sum((2**(N*i))*dz[i] for i in range(u)) / 10.**P
    return (x,y,z)

def encrypt_cluster(
    clusters: tuple[tuple[float, ...], ...],
    N: int,
    P: int
) -> str:
    return " ".join(sorted(list(encrypt_vector(i, N, P) for i in clusters)))

def decrypt_cluster(
    encrypted_cluster: str,
    N: int,
    P: int
) -> tuple[tuple[float, ...], ...]:
    return tuple(decrypt_vector(i, N, P) for i in encrypted_cluster.split())

def _drop_duplicates(inp: Iterable) -> tuple[Any, ...]:
    return tuple(t for t in dict.fromkeys(x for x in inp))

def get_rv_ex_sp(modes: list[list[int]]) -> list[Any]:
    rv = [
        lambda x,y,z: ( x, y, z),
        lambda x,y,z: (-x, y, z),
        lambda x,y,z: ( x,-y, z),
        lambda x,y,z: (-x,-y, z),
        lambda x,y,z: ( x, y,-z),
        lambda x,y,z: (-x, y,-z),
        lambda x,y,z: ( x,-y,-z),
        lambda x,y,z: (-x,-y,-z)
    ]

    ex = [
        lambda x,y,z: ( x, y, z),
        lambda x,y,z: ( y, x, z),
        lambda x,y,z: ( x, z, y),
        lambda x,y,z: ( z, y, x),
        lambda x,y,z: ( z, x, y),
        lambda x,y,z: ( y, z, x)
    ]

    sp = [
        lambda x,y,z: (  x,  y, z),
        lambda x,y,z: (x-y,  x, z),
        lambda x,y,z: ( -y,x-y, z),
        lambda x,y,z: ( -x, -y, z),
        lambda x,y,z: (y-x, -x, z),
        lambda x,y,z: (  y,y-x, z)
    ]

    rv = list(i for n,i in enumerate(rv) if n in modes[0])
    ex = list(i for n,i in enumerate(ex) if n in modes[1])
    sp = list(i for n,i in enumerate(sp) if n in modes[2])
    lambdas = []
    for i in rv:
        for j in ex:
            for k in sp:
                l = lambda x,y,z,i=i,j=j,k=k:i(*j(*k(x,y,z)))
                lambdas.append(l)
    return lambdas

def map_symmetry_of_cluster(
    cluster: tuple[tuple[float, ...], ...],
    modes: list[list[int]]
) -> tuple[tuple[tuple[float, ...], ...], ...]:
    lambdas = get_rv_ex_sp(modes)
    """ クラスター内の各点を同じ操作で写像してlistで括る。この写像クラスターlistを返却する。 """
    result = tuple(tuple(
        fnc(*vec)
        for vec in cluster
    ) for fnc in lambdas)
    return result

def mod_for_vector(vec: tuple[float, ...]) -> tuple[float, ...]:
    def m(x):
        while x < 0:
            x += 1
        while x >= 1:
            x -= 1
        return x
    return tuple(m(x) for x in vec)

def extract_identifying_cluster(
    cluster: tuple[tuple[float, ...], ...],
    modes: list[list[int]],
    N: int,
    P: int,
) -> str:
    return sorted(tuple(
        encrypt_cluster(i, N, P)
        for i in map_symmetry_of_cluster(cluster, modes)
    ))[-1]
