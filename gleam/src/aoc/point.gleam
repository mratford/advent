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
