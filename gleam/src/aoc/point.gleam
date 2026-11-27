import gleam/int
import gleam/list
import gleam/string

pub const n = Point(0, 1)

pub const e = Point(1, 0)

pub const s = Point(0, -1)

pub const w = Point(-1, 0)

pub type Point {
  Point(x: Int, y: Int)
}

pub fn add(p1: Point, p2: Point) -> Point {
  Point(p1.x + p2.x, p1.y + p2.y)
}

pub fn from_string(s: String) -> Result(Point, String) {
  s
  |> string.split(",")
  |> list.try_map(int.parse)
  |> fn(ints) {
    case ints {
      Ok([x, y]) -> Ok(Point(x, y))
      _ -> Error("Could not convert " <> s <> " to a Point")
    }
  }
}

pub fn to_string(p: Point) -> String {
  int.to_string(p.x) <> "," <> int.to_string(p.y)
}
