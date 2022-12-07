use itertools::Itertools;
use std::collections::HashMap;
use std::path::{Path, PathBuf};
use std::{clone, fs};

#[derive(Debug)]
struct File {
    name: String,
    size: u64,
}

// #[derive(Debug)]
// struct Directory {
//     // name: String,
//     // directories: Vec<Directory>,
//     files: Vec<File>,
// }

#[derive(Debug)]
enum LsItem {
    Directory(String),
    File(File),
}

#[derive(Debug)]
enum Command {
    Ls(Vec<LsItem>),
    Cd(String),
    WTF,
}

fn parse_ls_item(item: String) -> LsItem {
    match &item[..3] {
        "dir" => LsItem::Directory(String::from(&item[4..])),
        _ => {
            let mut split = item.split_whitespace();
            let size = split
                .next()
                .expect("Failed to parse file size")
                .parse::<u64>()
                .expect("Failed to parse file size as integer");
            let name = split.next().expect("Failed to parse file name");
            LsItem::File(File {
                name: String::from(name).clone(),
                size: size,
            })
        }
    }
}

fn parse_ls(block: &String) -> Vec<LsItem> {
    block
        .split('\n')
        .map(|x| x.to_string())
        .dropping(1)
        .map(|x| parse_ls_item(x.to_string()))
        .collect::<Vec<LsItem>>()
}

fn parse_block(block: &String) -> Command {
    match &block[..2] {
        "cd" => Command::Cd(block[3..].to_string()),
        "ls" => Command::Ls(parse_ls(&block)),
        _ => Command::WTF,
    }
}

fn parse(code: &String) -> Vec<Command> {
    code.split("$ ")
        .map(|x| x.trim().to_string())
        .filter(|x| x != "")
        .map(|x| parse_block(&x))
        .collect()
}

fn main() {
    let input = fs::read_to_string("test_input").unwrap();
    let code = parse(&input);

    let mut current_dir: Vec<String> = Vec::new();
    let mut sizes: HashMap<String, u64> = HashMap::new();
    current_dir.push(String::from("/"));
    sizes.insert("/".to_string(), 0);

    for command in code {
        let cd_str = current_dir.join("/").to_string();
        if !sizes.contains_key(&cd_str) {
            sizes.insert(cd_str, 0);
        }
        println!("{:?}", command);
        match command {
            Command::Cd(dir) => {
                if dir == "/" {
                    current_dir = Vec::new();
                    current_dir.push(String::from("/"));
                } else if dir == ".." {
                    current_dir.pop().unwrap();
                } else {
                    current_dir.push(dir);
                }
            }
            Command::Ls(items) => {
                for item in items {
                    match item {
                        LsItem::Directory(dir) => {
                            // do nothing
                        }
                        LsItem::File(File { name, size }) => {
                            println!("{:?} {:?}", current_dir, current_dir.len());
                            for i in 1..=current_dir.len() {
                                println!("{:?} {:?}", i, size);
                                *sizes
                                    .get_mut(&current_dir[0..i].join("/").to_string())
                                    .unwrap() += size;
                                println!(
                                    "Look {:?} {:?}",
                                    current_dir[0..i].join("/").to_string(),
                                    sizes
                                );
                            }
                        }
                    }
                }
            }
            Command::WTF => (),
        }

        println!("Sizes {:?}", sizes);
        println!("Current dir {:?}", current_dir);
    }

    let xs: Vec<u64> = sizes.values().filter(|x| **x <= 100000).sum();
    println!("{:?}", xs);
    //let part_1: u64 = xs.iter().filter(|x| x <= &&&100000).sum() as u64;
}
