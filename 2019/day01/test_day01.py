from day01 import fuel_needed, module_fuel


def test_fuel_1():
    assert(fuel_needed(12) == 2)


def test_fuel_2():
    assert(fuel_needed(14) == 2)


def test_fuel_3():
    assert(fuel_needed(1969) == 654)


def test_fuel_4():
    assert(fuel_needed(100756) == 33583)


def test_total_1():
    assert(module_fuel(14) == 2)


def test_total_2():
    assert(module_fuel(1969) == 966)


def test_total_3():
    assert(module_fuel(100756) == 50346)