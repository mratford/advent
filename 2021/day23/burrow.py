from __future__ import annotations
from functools import total_ordering
from typing import List, Dict, Tuple, Union, Iterator
from dataclasses import dataclass
from heapq import heappush, heappop
import logging

logging.basicConfig(
    filename="burrow.log",
    level=logging.INFO,
    format="%(message)s",
)


@dataclass
class InvalidMoveError(Exception):
    message: str


AMPHIPODS = {"A": 1, "B": 10, "C": 100, "D": 1000}
ROOM_COLUMN = {a: c for a, c in zip(AMPHIPODS, (3, 5, 7, 9))}


class BurrowMap:
    def __init__(self, size_of_rooms: int = 2):
        self.size_of_rooms: int = size_of_rooms
        self.hallway: List[int] = [1, 2, 4, 6, 8, 10, 11]
        self.rooms: Dict[str, List[int]] = {
            a: list(range(1, size_of_rooms + 1)) for a in AMPHIPODS
        }

    def path_length(
        hallway_pos: int,
        amphipod_room: str,
        amphipod_room_pos: int,
    ) -> int:
        return abs(hallway_pos - ROOM_COLUMN[amphipod_room]) + amphipod_room_pos

    def hallway_path(self, x: int, y: int) -> List[int]:
        """Locations between x and y inclusive in hallway"""
        return [z for z in self.hallway if x <= z <= y or y <= z <= x]


@total_ordering
class BurrowState:
    burrow_map: BurrowMap = BurrowMap(2)

    def __init__(
        self,
        hallway: Dict[int, str],
        rooms: Dict[Tuple[str, int], str],
        energy_used: int = 0,
        room_length: Union[int, None] = None,
    ):
        self.hallway: Dict[int, str] = hallway
        self.rooms: Dict[Tuple[str, int], str] = rooms
        self.energy_used: int = energy_used
        self.h = self.heuristic()
        if room_length is not None:
            burrow_map = BurrowMap(room_length)

    @classmethod
    def parse(cls, position_string):
        lines = position_string.strip().splitlines()
        room_length = len(lines) - 3
        rooms = {}

        for a, c in ROOM_COLUMN.items():
            for i in range(1, room_length + 1):
                row = 1 + i
                rooms[(a, i)] = lines[row][c]

        return cls({}, rooms, 0, room_length)

    def clean_room(self, amphipod: str) -> bool:
        return all(self.rooms[(a, i)] == a for a, i in self.rooms if a == amphipod)

    def finished(self) -> bool:
        return not self.hallway and all(self.rooms[(a, i)] == a for a, i in self.rooms)

    def deepest_location_in_room(self, amphipod_room: str) -> Union[int, None]:
        for i in range(BurrowState.burrow_map.size_of_rooms, 0, -1):
            if (amphipod_room, i) not in self.rooms:
                return i
        return None

    def move_from_room(
        self, room_location: Tuple[str, int], hallway_location: int
    ) -> BurrowState:
        amphipod_room, i = room_location
        if self.clean_room(amphipod_room):
            raise InvalidMoveError("Can't move amphipod from clean room")
        path = BurrowState.burrow_map.hallway_path(
            ROOM_COLUMN[amphipod_room], hallway_location
        )
        if any(x in self.hallway for x in path):
            raise InvalidMoveError("Can't move amphipod as path is not clear")
        if room_location not in self.rooms:
            raise InvalidMoveError("Can't move amphipod from empty room location")
        new_rooms = self.rooms.copy()
        new_hallway = self.hallway.copy()
        amphipod = new_rooms.pop(room_location)
        new_hallway[hallway_location] = amphipod
        logging.debug("\n")
        logging.debug(self)
        logging.debug(f"Move from {room_location} to {hallway_location}")
        b = BurrowState(
            new_hallway,
            new_rooms,
            self.energy_used
            + BurrowMap.path_length(hallway_location, amphipod_room, i)
            * AMPHIPODS[amphipod],
        )
        logging.debug(b)
        return b

    def move_from_hallway(
        self, hallway_location: int, room_location: Tuple[str, int]
    ) -> BurrowState:
        amphipod_room, i = room_location
        if not self.clean_room(amphipod_room):
            raise InvalidMoveError(
                "Can't move amphipod to room with other types of amphipod"
            )
        if hallway_location not in self.hallway:
            raise InvalidMoveError("Can't move amphipod from empty hallway location")
        amphipod = self.hallway[hallway_location]
        if amphipod != amphipod_room:
            raise InvalidMoveError(
                "Can't move amphipod to another type of amphipod's room"
            )
        if i != self.deepest_location_in_room(amphipod_room):
            raise InvalidMoveError(
                "Can't move amphipod to location in room that isn't the furthest in"
            )
        path = BurrowState.burrow_map.hallway_path(
            ROOM_COLUMN[amphipod_room], hallway_location
        )
        if any(x in self.hallway for x in path if x != hallway_location):
            raise InvalidMoveError("Can't move amphipod as path is not clear")
        new_hallway = self.hallway.copy()
        new_rooms = self.rooms.copy()
        amphipod = new_hallway.pop(hallway_location)
        new_rooms[room_location] = amphipod
        logging.debug("---------")
        logging.debug(self)
        logging.debug(f"Move from {hallway_location} to {room_location}")
        b = BurrowState(
            new_hallway,
            new_rooms,
            self.energy_used
            + BurrowMap.path_length(hallway_location, amphipod_room, i)
            * AMPHIPODS[amphipod],
        )
        logging.debug(b)
        return b

    def halls_to_left(self, c: int) -> List[int]:
        return list(reversed([h for h in BurrowState.burrow_map.hallway if h < c]))

    def halls_to_right(self, c: int) -> List[int]:
        return [h for h in BurrowState.burrow_map.hallway if h > c]

    def all_moves_from_rooms(
        self,
    ) -> Iterator[Tuple[Tuple[str, int], int]]:
        for amphipod_room in AMPHIPODS:
            if not (self.clean_room(amphipod_room)):
                i = next(
                    (
                        i
                        for i in range(1, BurrowState.burrow_map.size_of_rooms + 1)
                        if (amphipod_room, i) in self.rooms
                    ),
                    None,
                )
                if i:
                    for halls_to_check in [
                        self.halls_to_left(ROOM_COLUMN[amphipod_room]),
                        self.halls_to_right(ROOM_COLUMN[amphipod_room]),
                    ]:
                        j = 0
                        while (
                            j < len(halls_to_check)
                            and halls_to_check[j] not in self.hallway
                        ):
                            yield ((amphipod_room, i), halls_to_check[j])
                            j += 1

    def all_moves_from_hallway(
        self,
    ) -> Iterator[Tuple[Tuple[str, int], int]]:
        for hallway_location in self.hallway:
            amphipod = self.hallway[hallway_location]
            path = BurrowState.burrow_map.hallway_path(
                ROOM_COLUMN[amphipod], hallway_location
            )
            if self.clean_room(amphipod) and not any(
                x in self.hallway for x in path if x != hallway_location
            ):
                yield (
                    hallway_location,
                    (amphipod, self.deepest_location_in_room(amphipod)),
                )

    def all_moves(self) -> Iterator[BurrowState]:
        for h, r in self.all_moves_from_hallway():
            yield self.move_from_hallway(h, r)
        for r, h in self.all_moves_from_rooms():
            yield self.move_from_room(r, h)

    def heuristic(self) -> int:
        h = 0
        for (a, i) in self.rooms:
            if a != self.rooms[(a, i)] or not self.clean_room(a):
                h += i * AMPHIPODS[a]
                if i == ROOM_COLUMN[a]:
                    h += 2 * AMPHIPODS[a]
                else:
                    h += abs(i - ROOM_COLUMN[a]) * AMPHIPODS[a]
        # for a in AMPHIPODS:
        #     if not self.clean_room(a):
        #         n = BurrowState.burrow_map.size_of_rooms
        #     else:
        #         n = self.deepest_location_in_room(a)
        #     if n:
        #         h += AMPHIPODS[a] * n * (n + 1) / 2
        for hallway_location in self.hallway:
            a = self.hallway[hallway_location]
            h += abs(hallway_location - ROOM_COLUMN[a]) * AMPHIPODS[a]
        return h

    def __eq__(self, other: BurrowState) -> bool:
        return self.energy_used + self.h == other.energy_used + other.h

    def __lt__(self, other: BurrowState) -> bool:
        return self.energy_used + self.h < other.energy_used + other.h

    def __str__(self):
        s = (
            "#############\n"
            f'#{"".join([self.hallway.get(i, ".") for i in range(1, 12)])}#\n'
        )
        for i in range(1, BurrowState.burrow_map.size_of_rooms + 1):
            s = s + f'{"##" if i == 1 else "  "}#'
            for a in AMPHIPODS:
                s = s + self.rooms.get((a, i), ".") + "#"
            s = s + f'{"##" if i == 1 else "  "}\n'
        s = s + "  #########\n" + f"Energy used = {self.energy_used}"
        return s


def solve(s):
    q = [BurrowState.parse(s)]
    while q:
        b = heappop(q)
        if b.finished():
            return b.energy_used
        for next_b in b.all_moves():
            heappush(q, next_b)


if __name__ == "__main__":
    input_string = open("input", "r").read().strip()
    print(solve(input_string))
