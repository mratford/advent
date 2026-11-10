import aoc2015/day1

pub fn part_1_test() {
  assert day1.solve_1(")())())") == "-3"
}

pub fn part_2_test() {
  assert day1.solve_2("()())") == "5"
}
