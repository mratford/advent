import day02
import pytest
from pyrsistent import pvector

@pytest.mark.parametrize("test_input,expected", 
    [([1,0,0,0,99], [2,0,0,0,99]),
     ([2,3,0,3,99], [2,3,0,6,99]),
     ([2,4,4,5,99,0], [2,4,4,5,99,9801]),
     ([1,1,1,4,99,5,6,0,99], [30,1,1,4,2,5,6,0,99])])
def test_run_program(test_input, expected):
    day02.run_program(pvector(test_input)) == pvector(expected)