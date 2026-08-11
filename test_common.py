import compileall
import pathlib
from common.matrix import inverse

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
