from intcode import Intcode
import pytest
from pyrsistent import pvector
from pyrsistent.typing import PVector
from typing import Tuple, List
from itertools import permutations, cycle


# Day 2 tests

@pytest.mark.parametrize("test_input,expected", 
    [('1,0,0,0,99', [2,0,0,0,99]),
     ('2,3,0,3,99', [2,3,0,6,99]),
     ('2,4,4,5,99,0', [2,4,4,5,99,9801]),
     ('1,1,1,4,99,5,6,0,99', [30,1,1,4,2,5,6,0,99])])
def test_day_2(test_input, expected):
    Intcode(test_input).run([]) == pvector(expected)



# Day 5 tests

def run_inputs(program, inputs):
    return [Intcode(program).run(pvector([input]))[-1]
            for input in inputs]

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


# Day 7 tests

def run_phase_setting(phases: Tuple[int, ...], program: str) -> int:
    output = 0
    for phase in phases:
        code = Intcode(program)
        output = code.run(pvector([phase, output]))[-1]
    return output


def solve_part_1_day7(code: str) -> int:
    return max(run_phase_setting(phases, code)
               for phases in permutations(range(5)))


def run_phase_setting_2(phases: Tuple[int, ...], program: str) -> int:
    amps = [Intcode(program) for _ in range(5)]
    
    for i, phase in enumerate(phases):
        assert list(amps[i].run(pvector([phase]))) == []
        
    outputs: List[PVector[int]] = [pvector() for _ in range(5)]
    outputs[0] = amps[0].run(pvector([0]))
    
    # Input output 0 to amplifier 1 and carry on
    for i in cycle([1, 2, 3, 4, 0]):
        output = amps[i].run(outputs[i - 1 % 5])
        if output:
            outputs[i] = output
        else:
            break

    return outputs[-1][-1]
            

def solve_part_2_day7(code: str) -> int:
    return max(run_phase_setting_2(phases, code)
               for phases in permutations(range(5, 10)))    


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
    assert solve_part_1_day7(test_input) == expected


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
    assert solve_part_2_day7(test_input) == expected


# # Day 9

# def test_09_1_1():
#     assert (
#         Intcode('109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99')
#         .run(pvector())
#         == pvector([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]))

# def test_09_1_2():
#     assert (
#         len(str(Intcode('1102,34915192,34915192,7,4,7,99,0').run(pvector())[0]))
#         == 16)

# def test_09_1_3():
#     assert (
#         Intcode('104,1125899906842624,99').run(pvector())[0]
#         == 1125899906842624)
    
