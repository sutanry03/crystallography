import math
import pathlib
import compileall
from common.matrix import inverse
from common.lattice import (
    Cubic,
    Hexagonal,
    Tetragonal,
    Orthorhombic,
    Trigonal,
    Monoclinic,
    Triclinic,
    Lattice,
)
from common.symmetry import (
    _drop_duplicates,
    map_symmetry_of_cluster
)

def test_library_syntax():
    target_dir = pathlib.Path("./common")
    is_valid = compileall.compile_dir(target_dir, quiet=1)
    assert is_valid

def test_double_inverse_give_back_itself():
    sample = (
        (1., 2., 3.),
        (1., 1., 0.),
        (1., 1., 1.),
    )
    inv = inverse(sample)
    assert sample == inverse(inv)

def test_Cubic_lattice_params():
    cb = Cubic(a=4.04)
    assert cb is not None
    assert cb._check_lattice_params() == True

def test_Hexagonal_lattice_params():
    hx = Hexagonal(a=3.85, c=5.12)
    assert hx is not None
    assert hx._check_lattice_params() == True

def test_Tetragonal_lattice_params():
    tg01 = Tetragonal(a=3.85, c=5.12)
    assert tg01 is not None
    assert tg01._check_lattice_params() == True
    try:
        tg02 = Tetragonal(a=3.85, c=3.85)
        assert False
    except:
        assert True

def test_Orthorhombic_lattice_params():
    or01 = Orthorhombic(a=3.85, b=4.04, c=5.12)
    assert or01 is not None
    assert or01._check_lattice_params() == True
    try:
        or02 = Orthorhombic(a=3.85, b=3.85, c=3.85)
        assert False
    except:
        assert True
    try:
        or03 = Orthorhombic(a=3.85, b=3.85, c=5.12)
        assert False
    except:
        assert True
    try:
        or04 = Orthorhombic(a=3.85, b=5.12, c=5.12)
        assert False
    except:
        assert True
    try:
        or05 = Orthorhombic(a=3.85, b=4.04, c=3.85)
        assert False
    except:
        assert True

def test_Trigonal_lattice_params():
    tr01 = Trigonal(a=3.61, alpha=75.)
    assert tr01 is not None
    assert tr01._check_lattice_params() == True
    try:
        tr02 = Trigonal(a=3.61, alpha=135.)
        assert False
    except:
        assert True

def test_Monoclinic_lattice_params():
    mc01 = Monoclinic(a=3.61, b=4.04, c=5.83, beta=75.)
    assert mc01 is not None
    assert mc01._check_lattice_params() == True

def test_Triclinic_lattice_params():
    tc01 = Triclinic(
        a=3.61, b=4.04, c=5.83,
        alpha=45., beta=90., gamma=105.
    )
    assert tc01 is not None
    assert tc01._check_lattice_params() == True
    try:
        tc02 = Triclinic(
            a=3.61, b=4.04, c=5.83,
            alpha=30., beta=60., gamma=105.
        )
        assert False
    except:
        assert True

def test_invalid_angle_cannot_generate_last_axis():
    for beta in range(1, 18):
        for gamma in range(1, 18):
            bt = beta*math.pi/18.
            g = gamma*math.pi/18.
            phi = round(math.acos(math.cos(bt-g))/math.pi * 180, 1)
            phi = phi if phi > 0.01 else 0.11
            phi = phi if phi < 179.99 else 179.89
            theta = round(math.acos(math.cos(bt+g))/math.pi * 180, 1)
            theta = theta if theta > 0.01 else 0.11
            theta = theta if theta < 179.99 else 179.89

            to_test = None
            to_test = Lattice()
            try:
                to_test._calc_baseC(1., phi-0.1, beta*10, gamma*10)
                assert False
            except:
                assert True
            try:
                to_test._calc_baseC(1., phi+0.1, beta*10, gamma*10)
                to_test._calc_baseC(1., theta-0.1, beta*10, gamma*10)
                assert True
            except:
                assert False
            try:
                to_test._calc_baseC(1., theta+0.1, beta*10, gamma*10)
                assert False
            except:
                assert True

def test_map_symmetry_of_cluster():
    for cryst in [
        Cubic(a=1.0),
        Hexagonal(a=1.0,c=1.0),
        Tetragonal(a=1.0,c=1.0),
        Orthorhombic(a=1.0,b=1.0,c=1.0),
        Trigonal(a=1.0,alpha=75.),
        Monoclinic(a=1.0,b=1.0,c=1.0,beta=75.),
        Triclinic(
            a=1.0,b=1.0,c=1.0,
            alpha=60.,beta=75.,gamma=120.
        ),
    ]:
        c = map_symmetry_of_cluster(
            ((0.1, 0.3, 0.4),),
            cryst.symm_modes
        )
        d = _drop_duplicates(c)
        assert len(d) == cryst.symms
