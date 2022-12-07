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

    let mut current_dir = String::from("/");
    let mut directories: HashMap<String, HashMap<String, File>> = HashMap::new();

    for command in code {
        if !directories.contains_key(&current_dir) {
            directories.insert(current_dir.clone(), HashMap::new());
        }

        match command {
            Command::Cd(dir) => {
                if dir.starts_with("/") {
                    current_dir = dir;
                } else if dir == ".." {
                    current_dir = Path::new(&current_dir)
                        .parent()
                        .unwrap()
                        .to_str()
                        .unwrap()
                        .to_string();
                } else {
                    current_dir = Path::new(&current_dir)
                        .join(&dir)
                        .to_str()
                        .unwrap()
                        .to_string();
                }
            }
            Command::Ls(items) => {
                for item in items {
                    match item {
                        LsItem::Directory(dir) => {
                            if !directories.contains_key(&dir) {
                                directories.insert(dir.clone(), HashMap::new());
                            }
                        }
                        LsItem::File(File { name, size }) => {
                            directories[&current_dir].insert(
                                name.clone(),
                                File {
                                    name: name.clone(),
                                    size: size,
                                },
                            );
                        }
                    }
                }
            }
            Command::WTF => (),
        }
    }
}
