import compileall
import pathlib
from common.funct_def import add, multiply

def test_library_syntax():
    target_dir = pathlib.Path("./common")
    is_valid = compileall.compile_dir(target_dir, quiet=1)
    assert is_valid

def test_add():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(-1, -1) == -2

def test_multiply():
    assert multiply(1, 2) == 2
    assert multiply(-1, 1) == -1
    assert multiply(-1, -1) == 1


