import aoc/input
import aoc/parse
import aoc/point.{type Point, Point}
import argv
import gleam/dict.{type Dict}
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
  solve_1(input.load(2015, 6))
}

fn part_2() -> String {
  solve_2(input.load(2015, 6))
}

pub fn solve_1(input: String) -> String {
  let assert Ok(data) = parse_data(input)
  apply_over_ranges(new_grid(), data, light_action)
  |> dict.values
  |> list.count(fn(l) { l == On })
  |> int.to_string
}

pub fn solve_2(input: String) -> String {
  let assert Ok(data) = parse_data(input)
  apply_over_ranges(new_grid_2(), data, int_action)
  |> dict.values
  |> int.sum
  |> int.to_string
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

pub fn light_action(switch: Switch) -> fn(Light) -> Light {
  case switch {
    TurnOn -> fn(_) { On }
    TurnOff -> fn(_) { Off }
    Toggle -> fn(light) {
      case light {
        On -> Off
        Off -> On
      }
    }
  }
}

pub fn int_action(switch: Switch) -> fn(Int) -> Int {
  case switch {
    TurnOn -> fn(x) { x + 1 }
    TurnOff -> fn(x) { int.max(0, x - 1) }
    Toggle -> fn(x) { x + 2 }
  }
}

pub fn point_range(range: Range) -> List(Point) {
  let min_x = int.min(range.from.x, range.to.x)
  let max_x = int.max(range.from.x, range.to.x)
  let min_y = int.min(range.from.y, range.to.y)
  let max_y = int.max(range.from.y, range.to.y)
  int.range(min_x, max_x + 1, [], fn(acc, x) {
    list.prepend(
      acc,
      int.range(min_y, max_y + 1, [], fn(acc_inner, y) {
        list.prepend(acc_inner, Point(x, y))
      }),
    )
  })
  |> list.flatten
}

pub fn apply_over_range(
  grid: Dict(Point, a),
  f: fn(a) -> a,
  range: Range,
) -> Dict(Point, a) {
  let min_x = int.min(range.from.x, range.to.x)
  let max_x = int.max(range.from.x, range.to.x)
  let min_y = int.min(range.from.y, range.to.y)
  let max_y = int.max(range.from.y, range.to.y)
  int.range(min_x, max_x + 1, [], fn(acc, x) {
    int.range(min_y, max_y + 1, acc, fn(acc_inner, y) {
      let p = Point(x, y)
      let assert Ok(v) = dict.get(grid, p)
      list.prepend(acc_inner, #(p, f(v)))
    })
  })
  |> dict.from_list
  |> fn(x) { dict.merge(grid, x) }
}

pub fn new_grid() -> Dict(Point, Light) {
  point_range(Range(Point(0, 0), Point(999, 999)))
  |> list.fold(dict.new(), fn(d, p) { dict.insert(d, p, Off) })
}

pub fn new_grid_2() -> Dict(Point, Int) {
  point_range(Range(Point(0, 0), Point(999, 999)))
  |> list.fold(dict.new(), fn(d, p) { dict.insert(d, p, 0) })
}

pub fn apply_over_ranges(
  grid: Dict(Point, a),
  ranges: List(#(Switch, Range)),
  f: fn(Switch) -> fn(a) -> a,
) -> Dict(Point, a) {
  list.fold(ranges, grid, fn(g, rs) {
    let #(switch, r) = rs
    apply_over_range(g, f(switch), r)
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
