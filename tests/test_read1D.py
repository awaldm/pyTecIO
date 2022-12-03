import pathlib
import pytest
#from pytecio import read_tecplot
import pytecio.read_tecplot as tec
def test_find_test_data():
    testdata_path = pathlib.Path(__file__).parent / 'testdata'
    assert testdata_path.is_dir()

def test_read_1D():
    testdata_path = pathlib.Path(__file__).parent / 'testdata'
    testfile_1D = testdata_path / 'testdata_1D.dat'
    tec.read1D(testfile_1D, verbose = True)
