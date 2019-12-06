from day06 import solve_part_1, solve_part_2, parse_orbits


test_data_1 = '''COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L'''


def test_part_1():
    assert solve_part_1(parse_orbits(test_data_1)) == 42
    
    
test_data_2 = '''COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN'''


def test_part_2():
    assert solve_part_2(parse_orbits(test_data_2)) == 4