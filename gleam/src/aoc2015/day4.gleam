import aoc/input
import argv

pub fn main() -> Nil {
  case argv.load().arguments {
    ["1"] -> io.println(part_1())
    ["2"] -> io.println(part_2())
    _ -> io.println("usage: ./program <1 or 2>")
  }
}

fn part_1() -> String {
  solve_1(input.load(2015, 1))
}

fn part_2() -> String {
  solve_2(input.load(2015, 1))
}

fn solve_1(input: String) -> String {
  todo
}

fn solve_2(input: String) -> String {
  todo
}
