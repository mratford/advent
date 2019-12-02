use std::fs;


fn run_program(intcode: &Vec<usize>) -> Vec<usize> {
    let mut program = intcode.clone();

    for p in (0..(program.len())).step_by(4) {
        let instruction = program[p];
        let noun_i = program[p + 1];
        let verb_i = program[p + 2];
        let result_i = program[p + 3];
        
        match instruction {
            1 => program[result_i] = program[noun_i] + program[verb_i],
            2 => program[result_i] = program[noun_i] * program[verb_i],
            99 => break,
            x => panic!("Unknown code {}", x)
        }
    }

    program
}


fn main() {
    let data = fs::read_to_string("../input").unwrap();
    let mut intcode: Vec<usize> = data.trim().split(',').map(|x| str::parse::<usize>(x).unwrap()).collect();

    intcode[1] = 12;
    intcode[2] = 2;

    let p = run_program(&intcode);
    println!("{}", p[0]);

    for noun in 1..100 {
        for verb in 1..100 {
            intcode[1] = noun; 
            intcode[2] = verb;

            let p = run_program(&intcode);
            if p[0] == 19690720 {
                println!("{}", noun * 100 + verb);
                break;
            }
        }
    }
}
