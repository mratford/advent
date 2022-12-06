use itertools::Itertools;
use std::fs;

fn read_data(filename: &str) -> String {
    fs::read_to_string(&filename).unwrap().trim().to_string()
}

fn find_marker(signal: &String, n: usize) -> Option<usize> {
    for i in n..(signal.len()) {
        if signal[(i - n)..i].chars().all_unique() {
            return Some(i);
        }
    }
    None
}

fn main() {
    let signal = read_data("input");
    println!("Part 1: {:?}", find_marker(&signal, 4));
    println!("Part 2: {:?}", find_marker(&signal, 14));
}
