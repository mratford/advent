import aoc/input
import aoc/parse
import aoc/point.{type Point, Point}
import aoc/tools
import argv
import gleam/dict.{type Dict}
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
  solve_1(input.load(2015, 6))
}

fn part_2() -> String {
  solve_2(input.load(2015, 6))
}

pub fn solve_1(input: String) -> String {
  input
  |> parse_data
}

pub fn solve_2(_input: String) -> String {
  "answer"
}

pub type Light {
  On
  Off
}

pub fn turn_on(_: Light) -> Light {
  On
}

pub fn turn_off(_: Light) -> Light {
  Off
}

pub fn toggle(light: Light) -> Light {
  case light {
    On -> Off
    Off -> On
  }
}

pub fn point_range(from: Point, to: Point) -> List(Point) {
  let min_x = int.min(from.x, to.x)
  let max_x = int.max(from.x, to.x)
  let min_y = int.min(from.y, to.y)
  let max_y = int.max(from.y, to.y)
  tools.product(
    int.range(min_x, max_x + 1, [], list.prepend),
    int.range(min_y, max_y + 1, [], list.prepend),
  )
  |> list.map(fn(t) { Point(t.0, t.1) })
}

pub fn new_grid() -> Dict(Point, Light) {
  point_range(Point(0, 0), Point(999, 999))
  |> list.fold(dict.new(), fn(d, p) { dict.insert(d, p, Off) })
}

pub fn apply_over_range(
  grid: Dict(Point, Light),
  f: fn(Light) -> Light,
  range: List(Point),
) -> Dict(Point, Light) {
  list.fold(range, grid, fn(acc, x) { dict.insert(f(dict.get
}

pub fn parse_data(
  input: String,
) -> Result(List(#(fn(Light) -> Light, List(Point))), String) {
  input
  |> parse.splitlines()
  |> list.try_map(parse_line)
}

pub fn parse_line(
  line: String,
) -> Result(#(fn(Light) -> Light, List(Point)), String) {
  let fields = string.split(line, " ")
  case fields {
    ["turn", "on", p1, _, p2] -> parse_fields(turn_on, p1, p2)
    ["turn", "off", p1, _, p2] -> parse_fields(turn_off, p1, p2)
    ["toggle", p1, _, p2] -> parse_fields(toggle, p1, p2)
    _ -> Error("Failed to parse " <> line)
  }
}

pub fn parse_fields(
  f: fn(Light) -> Light,
  p1: String,
  p2: String,
) -> Result(#(fn(Light) -> Light, List(Point)), String) {
  case point.from_string(p1), point.from_string(p2) {
    Ok(x), Ok(y) -> Ok(#(f, point_range(x, y)))
    _, _ -> Error("Failed to parse points " <> p1 <> " " <> p2)
  }
}
