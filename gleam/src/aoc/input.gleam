import gleam/int
import simplifile

pub fn load(year: Int, day: Int) -> String {
  case
    simplifile.read(
      "input/aoc"
      <> int.to_string(year)
      <> "/day"
      <> int.to_string(day)
      <> "/input",
    )
  {
    Ok(data) -> data
    Error(e) -> "Error: " <> simplifile.describe_error(e)
  }
}
