import aoc/input
import aoc/parse
import argv
import gleam/int
import gleam/io
import gleam/list
import gleam/result
import gleam/string

pub fn main() -> Nil {
  case argv.load().arguments {
    ["1"] -> io.println(part_1())
    ["2"] -> io.println(part_2())
    _ -> io.println("usage: ./program <1 or 2>")
  }
}

fn part_1() -> String {
  solve_1(input.load(2015, 2))
}

fn part_2() -> String {
  solve_2(input.load(2015, 2))
}

fn parse_line(s: String) -> List(Int) {
  let assert Ok([l, w, h]) = string.split(s, "x") |> list.try_map(int.parse)
    as { "Error: could not parse " <> s }
  [l, w, h]
}

fn parse_input(s: String) -> List(List(Int)) {
  s
  |> parse.splitlines
  |> list.map(parse_line)
}

fn area(side: #(Int, Int)) -> Int {
  side.0 * side.1
}

fn areas(present: List(Int)) -> List(Int) {
  present
  |> list.combination_pairs
  |> list.map(area)
}

pub fn paper_needed(present: List(Int)) -> Int {
  let xs = areas(present)
  { 2 * int.sum(xs) } + { list.reduce(xs, int.min) |> result.unwrap(0) }
}

pub fn ribbon_needed(present: List(Int)) -> Int {
  case list.sort(present, int.compare) {
    [x, y, z] -> { 2 * x } + { 2 * y } + { x * y * z }
    _ -> panic as "Is this a present from another dimension?"
  }
}

pub fn solve_1(input: String) -> String {
  let sides = input |> parse_input
  sides |> list.map(paper_needed) |> int.sum |> int.to_string
}

pub fn solve_2(input: String) -> String {
  let sides = input |> parse_input
  sides |> list.map(ribbon_needed) |> int.sum |> int.to_string
}
