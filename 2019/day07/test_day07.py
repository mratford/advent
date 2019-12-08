from day07 import solve_part_1, solve_part_2, run_phase_setting
import pytest
from intcode import Intcode


test_data_1 = [
    ('3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0',
        43210),
    ('3,23,3,24,1002,24,10,24,1002,23,-1,23,' 
        + '101,5,23,23,1,24,23,23,4,23,99,0,0',
        54321),
    ('3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,' +
        '1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0',
        65210)  
]

@pytest.mark.parametrize("test_input,expected", test_data_1)
def test_1(test_input, expected):
    assert solve_part_1(test_input) == expected


test_data_2 = [
    ('3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,' +
     '27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5',
     139629729),
    ('3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,'
     '-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,'
     '53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10',
     18216)
]

@pytest.mark.parametrize("test_input,expected", test_data_2)
def test_2(test_input, expected):
    assert solve_part_2(test_input) == expected


def run_inputs(program, inputs):
    return [list(Intcode(program).run(iter([input])))[-1] for input in inputs]


def test_eq8_pos():
    assert run_inputs('3,9,8,9,10,9,4,9,99,-1,8', [7, 8, 9]) == [0, 1, 0]
    
def test_lt8_pos():
    assert run_inputs('3,9,7,9,10,9,4,9,99,-1,8', [7, 8, 9]) == [1, 0, 0]
    
def test_eq8_imm():
    assert run_inputs('3,3,1108,-1,8,3,4,3,99', [7, 8, 9]) == [0, 1, 0]
    
def test_lt8_imm():
    assert run_inputs('3,3,1107,-1,8,3,4,3,99', [7, 8, 9]) == [1, 0, 0]
    
def test_jmp_pos():
    assert (run_inputs('3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9', [-1, 0, 1])
            == [1, 0, 1])

def test_jmp_imm():
    assert (run_inputs('3,3,1105,-1,9,1101,0,0,12,4,12,99,1', [-1, 0, 1])
            == [1, 0, 1])

