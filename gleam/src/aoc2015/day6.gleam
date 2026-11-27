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

pub type Switch {
  TurnOn
  TurnOff
  Toggle
}

pub type Range {
  Range(from: Point, to: Point)
}

pub fn light_action(light: Light, switch: Switch) -> Light {
  case light, switch {
    _, TurnOn -> On
    _, TurnOff -> Off
    On, Toggle -> Off
    Off, Toggle -> On
  }
}

pub fn point_range(range: Range) -> List(Point) {
  let min_x = int.min(range.from.x, range.to.x)
  let max_x = int.max(range.from.x, range.to.x)
  let min_y = int.min(range.from.y, range.to.y)
  let max_y = int.max(range.from.y, range.to.y)
  tools.product(
    int.range(min_x, max_x + 1, [], list.prepend),
    int.range(min_y, max_y + 1, [], list.prepend),
  )
  |> list.map(fn(t) { Point(t.0, t.1) })
}

pub fn new_grid() -> Dict(Point, Light) {
  point_range(Range(Point(0, 0), Point(999, 999)))
  |> list.fold(dict.new(), fn(d, p) { dict.insert(d, p, Off) })
}

pub fn apply_over_range(
  grid: Dict(Point, Light),
  switch: Switch,
  range: List(Point),
) -> Result(Dict(Point, Light), String) {
  list.try_fold(range, grid, fn(g, p) {
    case dict.get(g, p) {
      Ok(light) -> Ok(dict.insert(g, p, light_action(light, switch)))
      Error(_) -> Error(point.to_string(p) <> " not in grid")
    }
  })
}

pub fn parse_data(input: String) -> Result(List(#(Switch, Range)), String) {
  input
  |> parse.splitlines()
  |> list.try_map(parse_line)
}

pub fn parse_line(line: String) -> Result(#(Switch, Range), String) {
  let fields = string.split(line, " ")
  case fields {
    ["turn", "on", p1, _, p2] -> parse_fields(TurnOn, p1, p2)
    ["turn", "off", p1, _, p2] -> parse_fields(TurnOff, p1, p2)
    ["toggle", p1, _, p2] -> parse_fields(Toggle, p1, p2)
    _ -> Error("Failed to parse " <> line)
  }
}

pub fn parse_fields(
  switch: Switch,
  p1: String,
  p2: String,
) -> Result(#(Switch, Range), String) {
  case point.from_string(p1), point.from_string(p2) {
    Ok(x), Ok(y) -> Ok(#(switch, Range(x, y)))
    _, _ -> Error("Failed to parse points " <> p1 <> " " <> p2)
  }
}
