use std::fs::File;
use std::io::{BufReader, BufRead};
use std::cmp::max;

fn fuel_needed(mass: &i32) -> i32 {
    max((mass / 3) - 2, 0)
}

// Dreadful in many ways, but this is my first program in Rust
fn actual_fuel_needed(mass: &i32) -> i32 {
    let f = fuel_needed(mass);
    if f == 0 {
        0
    } else {
        f + actual_fuel_needed(&f)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_12() {
        assert_eq!(fuel_needed(12), 2);
    }

    #[test]
    fn test_14() {
        assert_eq!(fuel_needed(14), 2);
    }

    #[test]
    fn test_1969() {
        assert_eq!(fuel_needed(1969), 654);
    }

    #[test]
    fn test_100756() {
        assert_eq!(fuel_needed(100756), 33583)
    }
}

fn main() {
    let f = match File::open("../input") {
        Err(error) => panic!("{:?}", error),
        Ok(f) => f
    };
    let f = BufReader::new(f);

    let mut masses: Vec<i32> = vec![];

    for line in f.lines() {
        match line {
            Err(error) => panic!("{:?}", error),
            Ok(string) => match string.trim().parse::<i32>() {
                Err(error) => panic!("{:?}", error),
                Ok(mass) => masses.push(mass)
            }
        }
    }

    println!("Part 1: {:?}", masses.iter().map(fuel_needed).sum::<i32>());
    println!("Part 2: {:?}", masses.iter().map(actual_fuel_needed).sum::<i32>());
}

