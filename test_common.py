import compileall
import pathlib
from common.lattice_base import Vect, LatticeBasis as LB

def test_library_syntax():
    target_dir = pathlib.Path("./common")
    is_valid = compileall.compile_dir(target_dir, quiet=1)
    assert is_valid

def test_double_inverse_give_back_itself():
    sample = [
        Vect(v=(1., 2., 3.)),
        Vect(v=(1., 1., 0.)),
        Vect(v=(1., 1., 1.)),
    ]
    bas = LB(basis=tuple(sample))
    inv = bas.inverse(dim=3)
    assert bas == inv.inverse(dim=3)

