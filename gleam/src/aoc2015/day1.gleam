import aoc/input
import argv
import gleam/int
import gleam/io
import gleam/list
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
  input
  |> moves
  |> list.fold(0, int.add)
  |> int.to_string
}

fn moves(instructions: String) -> List(Int) {
  instructions
  |> string.to_graphemes
  |> list.filter_map(fn(x) {
    case x {
      "(" -> Ok(1)
      ")" -> Ok(-1)
      _ -> Error(Nil)
    }
  })
}

pub fn solve_2(input: String) -> String {
  input
  |> moves
  |> list.scan(0, int.add)
  |> list.take_while(fn(x) { x != -1 })
  |> list.length
  |> int.add(1)
  |> int.to_string
}
