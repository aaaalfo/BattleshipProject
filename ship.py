from typing import List, Tuple

class Ship:
    def __init__(self, positions: List[Tuple[int, int]]) -> None:
        self.positions = positions
        self.hits = set()

    def is_hit(self, coord: Tuple) -> bool:
        if coord in self.positions:
            self.hits.add(coord)
            return True
        return False

    def is_sunk(self) -> bool:
        return True if len(self.hits) == len(self.positions) else False