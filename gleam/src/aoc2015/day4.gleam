import argv
import gleam/bit_array
import gleam/crypto
import gleam/int
import gleam/io

pub fn main() -> Nil {
  case argv.load().arguments {
    ["1"] -> io.println(part_1())
    ["2"] -> io.println(part_2())
    _ -> io.println("usage: ./program <1 or 2>")
  }
}

fn part_1() -> String {
  solve_1("yzbqklnj")
}

fn part_2() -> String {
  solve_2("yzbqklnj")
}

pub fn solve_1(input: String) -> String {
  find_hash(input, 1) |> int.to_string
}

pub fn find_hash(key: String, n: Int) -> Int {
  let hash =
    crypto.hash(crypto.Md5, bit_array.from_string(key <> int.to_string(n)))
    |> bit_array.base16_encode
  case hash {
    "00000" <> _ -> n
    _ -> find_hash(key, n + 1)
  }
}

pub fn solve_2(input: String) -> String {
  find_hash_2(input, 1) |> int.to_string
}

pub fn find_hash_2(key: String, n: Int) -> Int {
  let hash =
    crypto.hash(crypto.Md5, bit_array.from_string(key <> int.to_string(n)))
    |> bit_array.base16_encode
  case hash {
    "000000" <> _ -> n
    _ -> find_hash_2(key, n + 1)
  }
}
