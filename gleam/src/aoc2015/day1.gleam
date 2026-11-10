import aoc/input
import argv
import gleam/int
import gleam/io
import gleam/string

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

pub fn solve_1(input: String) -> String {
  lift(input, 0) |> int.to_string
}

fn lift(instructions: String, floor: Int) -> Int {
  case instructions {
    "" -> floor
    "(" <> rest -> lift(rest, floor + 1)
    ")" <> rest -> lift(rest, floor - 1)
    _ ->
      lift(
        string.slice(instructions, 1, string.length(instructions) - 1),
        floor,
      )
  }
}

pub fn solve_2(input: String) -> String {
  find_basement(input, 0, 0) |> int.to_string()
}

fn find_basement(instructions: String, floor: Int, position: Int) -> Int {
  case floor {
    -1 -> position
    _ ->
      case instructions {
        "(" <> rest -> find_basement(rest, floor + 1, position + 1)
        ")" <> rest -> find_basement(rest, floor - 1, position + 1)
        _ -> -1
      }
  }
}
