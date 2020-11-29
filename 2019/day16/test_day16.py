from  day16 import pattern, phase, parse_data, answer_part_1

def test_pattern():
    assert pattern(3) == [0, 0, 0, 1, 1, 1, 0, 0, 0, -1, -1, -1]
    

def test_phase():
    assert phase(parse_data('12345678')) == parse_data('48226158')
    
    
def test_part_1():
    assert (answer_part_1('80871224585914546619083218645595') 
            == '24176176')
    assert (answer_part_1('19617804207202209144916044189917') 
            == '73745418')    
    assert (answer_part_1('69317163492948606335995924319873') 
            == '52432133')