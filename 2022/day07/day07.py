from collections import defaultdict
from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class File:
    name: str
    size: int


@dataclass
class Directory:
    name: str
    files: dict = field(default_factory=dict)
    dirs: dict = field(default_factory=list)


@dataclass
class FileSystem:
    directories: dict = field(default_factory=lambda: {Path("/"): Directory("/")})
    # Cache the sizes so they're not calculated more than once
    _sizes: dict = field(default_factory=dict)

    def add_directory(self, path: Path):
        p = Path("/")
        for d in path.parts[1:]:
            if p / d not in self.directories:
                self.directories[p].dirs.append(p / d)
                self.directories[p / d] = Directory(p / d)
            p = p / d

    def add_file(self, path: Path, size: int):
        self.add_directory(path.parent)
        self.directories[path.parent].files[path] = File(str(path), size)
        # File system has changed so need to recalculate sizes
        self._sizes = {}

    def __str__(self):
        return "\n".join(str(self.directories[d]) for d in self.directories)

    def size_of_directory(self, path: Path) -> int:
        if path not in self._sizes:
            self._sizes[path] = sum(
                f.size for f in self.directories[path].files.values()
            ) + sum(self.size_of_directory(d) for d in self.directories[path].dirs)
        return self._sizes[path]

    def size_of_all_directories(self) -> int:
        return {d: self.size_of_directory(d) for d in self.directories}


def parse(commands):
    command_blocks = commands.split("$ ")
    current_dir = Path("/")
    fs = FileSystem()

    for block in command_blocks:
        if block:
            lines = [line.strip() for line in block.strip().splitlines() if line]
            if lines[0].startswith("cd"):
                if lines[0][3] == "/":
                    current_dir = Path(lines[0][3:])
                elif lines[0][3:] == "..":
                    current_dir = current_dir.parent
                else:
                    current_dir = current_dir / lines[0][3:]
                fs.add_directory(current_dir)
            else:  # list block
                for item in lines[1:]:
                    if item.startswith("dir"):
                        # Make sure this exists just in case
                        fs.add_directory(current_dir / item[4:])
                    else:
                        split = item.split()
                        fs.add_file(current_dir / split[1], int(split[0]))

    return fs


def part_1(fs: FileSystem) -> int:
    return sum(size for size in fs.size_of_all_directories().values() if size <= 100000)


def part_2(fs: FileSystem) -> int:
    space = 70000000 - fs.size_of_directory(Path("/"))
    space_needed = 30000000 - space
    return min(
        size for size in fs.size_of_all_directories().values() if size >= space_needed
    )


if __name__ == "__main__":
    fs = parse(open("input").read())
    print("Part 1:", part_1(fs))
    print("Part 2:", part_2(fs))
