use std::collections::HashMap;
use std::str::FromStr;

#[macro_use]
extern crate scan_fmt;

fn main() {
    let mut input = include_str!("../input").split("\n\n");
    let mut stack_input = input.next().unwrap().split('\n').rev();
    let num_stacks = stack_input
        .next()
        .unwrap()
        .trim()
        .split_whitespace()
        .map(|x| usize::from_str(x).unwrap())
        .max()
        .unwrap();
    let mut stacks: HashMap<usize, Vec<char>> = HashMap::new();
    for i in 1..=num_stacks {
        stacks.insert(i, Vec::new());
    }
    for layer in stack_input {
        for i in 1..=num_stacks {
            let c = layer.chars().nth(1 + (i - 1) * 4).unwrap_or(' ');
            if c != ' ' {
                stacks.get_mut(&i).unwrap().push(c);
            }
        }
    }

    for line in input.next().unwrap().trim().split('\n') {
        let (n, source, dest) =
            scan_fmt!(line, "move {d} from {d} to {d}", u32, usize, usize).unwrap();
        for _ in 0..n {
            let c = stacks.get_mut(&source).unwrap().pop().unwrap();
            stacks.get_mut(&dest).unwrap().push(c)
        }
    }

    let mut result = String::from("");

    for i in 1..=num_stacks {
        result.push(*stacks[&i].last().unwrap());
    }

    println!("Part 1: {:?}", result);

    let mut input = include_str!("../input").split("\n\n");
    let mut stack_input = input.next().unwrap().split('\n').rev();
    let num_stacks = stack_input
        .next()
        .unwrap()
        .trim()
        .split_whitespace()
        .map(|x| usize::from_str(x).unwrap())
        .max()
        .unwrap();
    let mut stacks: HashMap<usize, Vec<char>> = HashMap::new();
    for i in 1..=num_stacks {
        stacks.insert(i, Vec::new());
    }
    for layer in stack_input {
        for i in 1..=num_stacks {
            let c = layer.chars().nth(1 + (i - 1) * 4).unwrap_or(' ');
            if c != ' ' {
                stacks.get_mut(&i).unwrap().push(c);
            }
        }
    }

    for line in input.next().unwrap().trim().split('\n') {
        let (n, source, dest) =
            scan_fmt!(line, "move {d} from {d} to {d}", usize, usize, usize).unwrap();
        let l = stacks.get_mut(&source).unwrap().len();
        let mut cs = stacks.get_mut(&source).unwrap().split_off(l - n);
        stacks.get_mut(&dest).unwrap().append(&mut cs);
    }

    let mut result = String::from("");

    for i in 1..=num_stacks {
        result.push(*stacks[&i].last().unwrap());
    }

    println!("Part 2: {:?}", result);
}
