#[macro_use]
extern crate scan_fmt;

fn main() {
    let lines: Vec<&str> = include_str!("../input").trim().split('\n').collect();
    let mut total = 0;
    let mut total_2 = 0;
    for line in &lines {
        let (l1, u1, l2, u2) = scan_fmt!(line, "{d}-{d},{d}-{d}", i32, i32, i32, i32).unwrap();
        if (l1 <= l2 && u1 >= u2) || (l2 <= l1 && u2 >= u1) {
            total += 1;
        }
        if (u1 >= l2 && l1 <= u2) || (u2 >= l1 && l2 <= u1) {
            total_2 += 1
        }
    }
    println!("Part 1: {}", total);
    println!("Part 2: {}", total_2);
}
