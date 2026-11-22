import aoc/input
import aoc/parse
import argv
import gleam/dict.{type Dict}
import gleam/int
import gleam/io
import gleam/list
import gleam/set.{type Set}
import gleam/string

pub fn main() -> Nil {
  case argv.load().arguments {
    ["1"] -> io.println(part_1())
    ["2"] -> io.println(part_2())
    _ -> io.println("usage: ./program <1 or 2>")
  }
}

fn part_1() -> String {
  solve_1(input.load(2015, 5))
}

fn part_2() -> String {
  solve_2(input.load(2015, 5))
}

pub fn solve_1(input: String) -> String {
  input
  |> parse.splitlines
  |> list.count(is_nice)
  |> int.to_string
}

pub fn solve_2(input: String) -> String {
  input
  |> parse.splitlines
  |> list.count(is_nice_correct)
  |> int.to_string
}

pub fn has_three_vowels(chars: List(UtfCodepoint)) -> Bool {
  chars
  |> list.filter(is_vowel)
  |> list.length
  |> fn(x) { x >= 3 }
}

pub fn is_vowel(char: UtfCodepoint) -> Bool {
  "aeiou"
  |> string.to_utf_codepoints
  |> list.contains(char)
}

pub fn pairs(xs: List(a)) -> List(#(a, a)) {
  pairs_loop(xs, [])
}

pub fn pairs_loop(xs: List(a), acc: List(#(a, a))) -> List(#(a, a)) {
  case xs {
    [x, y, ..rest] -> pairs_loop([y, ..rest], [#(x, y), ..acc])
    _ -> acc
  }
}

pub fn has_double(pairs: List(#(a, a))) -> Bool {
  case pairs {
    [#(x, y), ..] if x == y -> True
    [_, ..rest] -> has_double(rest)
    _ -> False
  }
}

pub fn banned_pairs() -> Set(#(UtfCodepoint, UtfCodepoint)) {
  ["ab", "cd", "pq", "xy"]
  |> list.map(string.to_utf_codepoints)
  |> list.map(pairs)
  |> list.flatten
  |> set.from_list
}

pub fn has_banned_pair(pairs: List(#(UtfCodepoint, UtfCodepoint))) -> Bool {
  pairs
  |> set.from_list
  |> set.intersection(banned_pairs())
  |> set.size
  |> fn(x) { x > 0 }
}

pub fn is_nice(str: String) -> Bool {
  let chars = string.to_utf_codepoints(str)
  let char_pairs = pairs(chars)
  has_three_vowels(chars)
  && has_double(char_pairs)
  && !has_banned_pair(char_pairs)
}

pub fn is_nice_correct(str: String) -> Bool {
  let chars = string.to_utf_codepoints(str)
  has_repeated_pair(chars) && has_repeated_letter(chars)
}

pub fn has_repeated_letter(chars: List(UtfCodepoint)) -> Bool {
  case chars {
    [x, _, z, ..] if x == z -> True
    [_, y, z, ..rest] -> has_repeated_letter([y, z, ..rest])
    _ -> False
  }
}

pub fn has_repeated_pair(chars: List(UtfCodepoint)) -> Bool {
  has_repeated_pair_loop(chars, 0, dict.new())
}

pub fn has_repeated_pair_loop(
  chars: List(UtfCodepoint),
  pos: Int,
  seen: Dict(#(UtfCodepoint, UtfCodepoint), Int),
) -> Bool {
  case chars {
    [x, y, ..rest] ->
      case dict.get(seen, #(x, y)) {
        Ok(p) if pos - p >= 2 -> True
        Ok(_) -> has_repeated_pair_loop([y, ..rest], pos + 1, seen)
        _ ->
          has_repeated_pair_loop(
            [y, ..rest],
            pos + 1,
            dict.insert(seen, #(x, y), pos),
          )
      }
    _ -> False
  }
}
