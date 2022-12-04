use std::collections::HashSet;

fn priority(c: char) -> u32 {
    if c.is_ascii_lowercase() {
        (c as u32) - ('a' as u32) + 1
    } else {
        (c as u32) - ('A' as u32) + 27
    }
}

fn main() {
    let rucksacks: Vec<&str> = include_str!("../input").trim().split('\n').collect();
    let mut priority_sum = 0;
    for rucksack in &rucksacks {
        let l = rucksack.len();
        let compartment_one: HashSet<char> = rucksack[..(l / 2)].chars().collect();
        let compartment_two: HashSet<char> = rucksack[(l / 2)..].chars().collect();
        let in_both = compartment_one
            .intersection(&compartment_two)
            .next()
            .unwrap_or(&'!');
        priority_sum = priority_sum + priority(*in_both);
    }
    println!("Part 1: {:?}", priority_sum);

    priority_sum = 0;
    for i in (0..rucksacks.len()).step_by(3) {
        let rucksack_one: HashSet<char> = rucksacks[i].chars().collect();
        let rucksack_two: HashSet<char> = rucksacks[i + 1].chars().collect();
        let rucksack_three: HashSet<char> = rucksacks[i + 2].chars().collect();
        let in_all = rucksack_one
            .intersection(&rucksack_two)
            .filter(|x| rucksack_three.contains(x))
            .next()
            .unwrap_or(&'!');
        priority_sum = priority_sum + priority(*in_all);
    }
    println!("Part 2: {:?}", priority_sum);
}
