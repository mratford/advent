use std::fs;
use std::str;

fn main() {
    let r = fs::read_to_string("input");
    let s = r.unwrap();
    let elf_groups = s.trim().split("\n\n");
    let elves = elf_groups.map(|g| g.split('\n').map(|x| str::parse::<i64>(x).unwrap()));
    let mut calories: Vec<i64> = elves.map(|e| e.sum::<i64>()).collect();
    println!("Part 1: {:?}", calories.iter().max());

    calories.sort();
    calories.reverse();
    println!("Part 2: {:?}", calories[0..3].iter().sum::<i64>());
}
