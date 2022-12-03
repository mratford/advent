use std::collections::HashMap;

fn score(my_move: &i64, their_move: &i64) -> i64 {
    match (my_move - their_move).rem_euclid(3) {
        0 => my_move + 4,
        1 => my_move + 7,
        2 => my_move + 1,
        _ => -10000000,
    }
}

fn score_2(my_move: &i64, their_move: &i64) -> i64 {
    match my_move {
        0 => (their_move - 1).rem_euclid(3) + 1,
        1 => their_move + 4,
        2 => (their_move + 1).rem_euclid(3) + 7,
        _ => -10000000,
    }
}

fn main() {
    let rps: HashMap<char, i64> =
        HashMap::from([('A', 0), ('B', 1), ('C', 2), ('X', 0), ('Y', 1), ('Z', 2)]);

    let mut total_score = 0;
    let s = include_str!("../input");
    for line in s.trim().split('\n') {
        let their_move = rps.get(&line.chars().nth(0).unwrap()).unwrap();
        let my_move = rps.get(&line.chars().nth(2).unwrap()).unwrap();
        total_score = total_score + score(&my_move, &their_move);
    }

    println!("Part 1: {}", total_score);

    let mut total_score = 0;
    let s = include_str!("../input");
    for line in s.trim().split('\n') {
        let their_move = rps.get(&line.chars().nth(0).unwrap()).unwrap();
        let my_move = rps.get(&line.chars().nth(2).unwrap()).unwrap();
        total_score = total_score + score_2(&my_move, &their_move);
    }

    println!("Part 2: {}", total_score);
}
