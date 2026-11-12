import aoc/input
import aoc/point.{type Point, Point}
import argv
import gleam/int
import gleam/io
import gleam/list
import gleam/set
import gleam/string

pub fn main() -> Nil {
  case argv.load().arguments {
    ["1"] -> io.println(part_1())
    ["2"] -> io.println(part_2())
    _ -> io.println("usage: ./program <1 or 2>")
  }
}

fn part_1() -> String {
  solve_1(input.load(2015, 3))
}

fn part_2() -> String {
  solve_2(input.load(2015, 3))
}

pub fn solve_1(input: String) -> String {
  input
  |> get_directions
  |> path
  |> set.from_list
  |> set.size
  |> int.to_string
}

pub fn solve_2(input: String) -> String {
  let #(santa, robot) =
    input
    |> get_directions
    |> alternate
  [santa, robot]
  |> list.map(path)
  |> list.map(set.from_list)
  |> list.fold(set.new(), set.union)
  |> set.size
  |> int.to_string
}

pub fn get_direction(move: String) -> Result(Point, Nil) {
  case move {
    "^" -> Ok(point.n)
    ">" -> Ok(point.e)
    "v" -> Ok(point.s)
    "<" -> Ok(point.w)
    _ -> Error(Nil)
  }
}

pub fn get_directions(moves: String) -> List(Point) {
  list.filter_map(string.to_graphemes(moves), get_direction)
}

pub fn path(directions: List(Point)) -> List(Point) {
  let start = Point(0, 0)
  [start, ..list.scan(directions, start, point.add)]
}

pub fn alternate(l: List(a)) -> #(List(a), List(a)) {
  alternate_loop(l, [], [])
}

fn alternate_loop(l: List(a), xs: List(a), ys: List(a)) {
  case l {
    [] -> #(list.reverse(xs), list.reverse(ys))
    [x] -> alternate_loop([], [x, ..xs], ys)
    [x, y, ..rest] -> alternate_loop(rest, [x, ..xs], [y, ..ys])
  }
}
