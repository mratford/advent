from day05 import intcode
from pyrsistent import pvector


def run_inputs(program, inputs):
    return [list(intcode(pvector(program), input))[-1] for input in inputs]


def test_eq8_pos():
    assert run_inputs([3,9,8,9,10,9,4,9,99,-1,8], [7, 8, 9]) == [0, 1, 0]
    
def test_lt8_pos():
    assert run_inputs([3,9,7,9,10,9,4,9,99,-1,8], [7, 8, 9]) == [1, 0, 0]
    
def test_eq8_imm():
    assert run_inputs([3,3,1108,-1,8,3,4,3,99], [7, 8, 9]) == [0, 1, 0]
    
def test_lt8_imm():
    assert run_inputs([3,3,1107,-1,8,3,4,3,99], [7, 8, 9]) == [1, 0, 0]
    
def test_jmp_pos():
    assert (run_inputs([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], [-1, 0, 1])
            == [1, 0, 1])

def test_jmp_imm():
    assert (run_inputs([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], [-1, 0, 1])
            == [1, 0, 1])

    
