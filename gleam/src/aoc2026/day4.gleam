import aoc/input
import argv
import gleam/io

pub fn main() -> Nil {
  case argv.load().arguments {
    ["1"] -> io.println(part_1())
    ["2"] -> io.println(part_2())
    _ -> io.println("usage: ./program <1 or 2>")
  }
}

fn part_1() -> String {
  solve_1(input.load(2026, 4))
}

fn part_2() -> String {
  solve_2(input.load(2026, 4))
}

pub fn solve_1(_input: String) -> String {
  "answer"
}

pub fn solve_2(_input: String) -> String {
  "answer"
}
