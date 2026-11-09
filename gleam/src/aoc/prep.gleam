import argv
import gleam/int
import gleam/io
import gleam/result
import gleam/string
import simplifile

pub fn main() {
  case parse_args(argv.load().arguments) {
    Ok(#(year, n_days)) ->
      case prep(year, n_days) {
        Ok(_) -> Nil
        Error(e) -> io.println("error: " <> simplifile.describe_error(e))
      }
    _ -> io.println("usage: gleam run -m aoc/prep <year> <number of days>")
  }
}

fn parse_args(args: List(String)) -> Result(#(String, Int), Nil) {
  case args {
    [year, n_days] ->
      case int.parse(n_days) {
        Ok(n) -> Ok(#(year, n))
        Error(_) -> Error(Nil)
      }
    _ -> Error(Nil)
  }
}

fn prep(year: String, n_days: Int) -> Result(Nil, simplifile.FileError) {
  simplifile.create_directory("src/aoc" <> year)
  |> result.try(fn(_) { simplifile.create_directory("test/aoc" <> year) })
  |> result.try(fn(_) { simplifile.create_directory("data/aoc" <> year) })
  |> result.try(fn(_) {
    int.range(1, n_days + 1, Ok(Nil), fn(_, day) { prep_day(year, day) })
  })
}

fn prep_day(year: String, day: Int) -> Result(Nil, simplifile.FileError) {
  let date = year <> "/day" <> int.to_string(day)
  simplifile.read("templates/aoc_src.gleam")
  |> result.map(fn(s) {
    string.replace(s, "YEAR", year)
    |> string.replace("DAY", int.to_string(day))
  })
  |> result.try(fn(src) { simplifile.write("src/aoc" <> date <> ".gleam", src) })
  |> result.try(fn(_) {
    simplifile.copy_file(
      "templates/aoc_test.gleam",
      "test/aoc" <> date <> "_test.gleam",
    )
  })
  |> result.try(fn(_) { simplifile.create_directory("data/aoc" <> date) })
  |> result.try(fn(_) {
    simplifile.write("data/aoc" <> date <> "/.placeholder", "")
  })
}
