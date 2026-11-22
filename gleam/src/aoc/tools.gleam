import gleam/list

pub fn product(xs: List(a), ys: List(b)) -> List(#(a, b)) {
  xs
  |> list.flat_map(fn(x) { list.map(ys, fn(y) { #(x, y) }) })
}
