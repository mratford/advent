from day04 import valid, valid_2


def test_1_1():
    assert valid(111111)


def test_1_2():
    assert not valid(223450)


def test_1_3():
    assert not valid(123789)


def test_2_1():
    assert valid_2(112233)
    
    
def test_2_2():
    assert not valid_2(123444)
    
    
def test_2_3():
    assert valid_2(111122)