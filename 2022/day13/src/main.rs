use std::fs;

enum Packet {
    Value(i64),
    List(Vec<Packet>),
}

fn parse_bucket(s: &str) -> Result<Packet, i64> {
    let stack = <Vec<Vec<Packet>>>::new();
    for c in s.chars() {
        if c == '[' {}
    }
    Ok(Packet::Value(1))
}

fn parse_data(s: &str) -> Vec<Vec<Packet>> {
    s.trim()
        .split("\n\n")
        .map(|x| x.split('\n'))
        .map(|xs| {
            xs.map(|x| parse_bucket(x).unwrap())
                .collect::<Vec<Packet>>()
        })
        .collect::<Vec<Vec<Packet>>>()
}

fn main() {
    let s = std::fs::read_to_string("test_input").unwrap();
    let packet_pairs = parse_data(&s);
}
