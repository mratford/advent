from intcode import Intcode
from pyrsistent import pvector


def test_1_1():
    assert (
        Intcode('109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99')
        .run(pvector())
        == pvector([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]))
