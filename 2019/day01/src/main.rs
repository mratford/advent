use std::fs::File;
use std::io::{BufReader, BufRead};
use std::cmp::max;

fn fuel_needed(mass: i32) -> i32 {
    max((mass / 3) - 2, 0)
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

    println!("Part 1: {:?}", masses.into_iter().map(fuel_needed).sum::<i32>())
}

