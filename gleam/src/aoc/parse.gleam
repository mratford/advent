import gleam/string

pub fn splitlines(s: String) -> List(String) {
  s
  |> string.trim
  |> string.split("\n")
}
