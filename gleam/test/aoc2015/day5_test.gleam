import aoc2015/day5
import gleam/string

pub fn is_nice_test() {
  assert day5.is_nice("ugknbfddgicrmopn")
}

pub fn is_nice_2_test() {
  assert day5.is_nice("aaa")
}

pub fn is_nice_3_test() {
  assert !day5.is_nice("jchzalrnumimnmhp")
}

pub fn is_nice_4_test() {
  assert !day5.is_nice("haegwjzuvuyypxyu")
}

pub fn is_nice_5_test() {
  assert !day5.is_nice("dvszwmarrgswjxmb")
}

pub fn has_repeated_letter_1_test() {
  let chars = string.to_utf_codepoints("qjhvhtzxzqqjkmpb")
  assert day5.has_repeated_letter(chars)
}

pub fn has_repeated_letter_2_test() {
  let chars = string.to_utf_codepoints("xvx")
  assert day5.has_repeated_letter(chars)
}

pub fn has_repeated_letter_3_test() {
  let chars = string.to_utf_codepoints("qjhhtzzqqjkqqmpb")
  assert !day5.has_repeated_letter(chars)
}
