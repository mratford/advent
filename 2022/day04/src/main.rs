fn main() {
    let lines: Vec<&str> = include_str!("../input").trim().split('\n').collect();
    let mut total = 0;
    let mut total_2 = 0;
    for line in &lines {
        let mut ranges = line.split(',');
        let mut r1 = ranges.next().unwrap().split('-');
        let l1 = r1.next().unwrap().parse::<i32>().unwrap();
        let u1 = r1.next().unwrap().parse::<i32>().unwrap();
        let mut r2 = ranges.next().unwrap().split('-');
        let l2 = r2.next().unwrap().parse::<i32>().unwrap();
        let u2 = r2.next().unwrap().parse::<i32>().unwrap();
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
