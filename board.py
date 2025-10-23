from ship import Ship
from utils import COLOR_CYAN, COLOR_YELLOW, COLOR_RESET, COLOR_GREEN, COLOR_RED, parse_coordinate, ext
from typing import Tuple

class Board:

    SIZE = 10

    def __init__(self, hidden: bool = False) -> None:
        self.hidden = hidden
        self.grid = [["~"] * self.SIZE for _ in range(self.SIZE)]
        self.ships = []
        self.hits = set()
        self.misses = set()

    def mark_sunk_area(self, ship: Ship) -> None:
        for (r, c) in ship.positions:
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = r + dr, c + dc
                    if not (0 <= nr < self.SIZE and 0 <= nc < self.SIZE):
                        continue
                    if (nr, nc) in ship.positions:
                        continue
                    cell = self.grid[nr][nc]
                    if cell == "~":
                        self.grid[nr][nc] = "•"
                        self.misses.add((nr, nc))
                    elif cell == "•":
                        self.misses.add((nr, nc))

    def place_ship(self, coord: str, direction: str, size: int) -> Tuple[bool, str]:
        try:
            row, col = parse_coordinate(coord)
        except ValueError as e:
            return False, str(e)

        if direction not in ("h", "v"):
            return False, "Направление должно быть 'h' или 'v'."

        positions = []
        for i in range(size):
            r = row + (i if direction == "v" else 0)
            c = col + (i if direction == "h" else 0)
            if r >= self.SIZE or c >= self.SIZE:
                return False, "Корабль выходит за границы поля."
            if self.grid[r][c] != "~":
                return False, "Место занято другим кораблём."
            positions.append((r, c))

        for r, c in positions:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.SIZE and 0 <= nc < self.SIZE:
                        if self.grid[nr][nc] == "■":
                            return False, "Корабль слишком близко к другому."

        ship = Ship(positions)
        self.ships.append(ship)
        for r, c in positions:
            self.grid[r][c] = "■"  

        return True, ''


    def shoot(self, coord: str) -> str:
        try:
            row, col = parse_coordinate(coord)
        except ValueError:
            return 'error'

        if (row, col) in self.hits or (row, col) in self.misses:
            print(f"\n{COLOR_YELLOW}Вы уже стреляли сюда!{COLOR_RESET}")
            return "repeat"

        for ship in self.ships:
            if (row, col) in ship.positions:
                ship.is_hit((row, col))
                self.hits.add((row, col))
                self.grid[row][col] = "X"

                if ship.is_sunk():
                    self.mark_sunk_area(ship)
                    print(f"\n{COLOR_RED}Корабль потоплен!{COLOR_RESET}")
                    self.ships.remove(ship)
                    return "sink"
                else:
                    print(f"\n{COLOR_YELLOW}Попадание!{COLOR_RESET}")
                    return "hit"

        self.grid[row][col] = "•"
        self.misses.add((row, col))
        print(f"\n{COLOR_CYAN}Мимо!{COLOR_RESET}")
        return "miss"


    def all_ships_sunk(self) -> bool:
        return len(self.ships) == 0


    def display(self, show_ships: bool = True) -> None:
        header = f"     {COLOR_CYAN}" + " ".join([chr(ord("A") + i) for i in range(self.SIZE)]) + f"{COLOR_RESET}"
        print(header)
        print("     " + "-" * (self.SIZE * 2 - 1))

        for i in range(self.SIZE):
            row_str = f"{i+1:2} | "
            for j in range(self.SIZE):
                cell = self.grid[i][j]
                if cell == "X":
                    row_str += f"{COLOR_RED}X{COLOR_RESET} "
                elif cell == "•":
                    row_str += f"{COLOR_YELLOW}•{COLOR_RESET} "
                elif cell == "■":
                    if show_ships and not self.hidden:
                        row_str += f"{COLOR_GREEN}■{COLOR_RESET} "
                    else:
                        row_str += f"{COLOR_CYAN}~{COLOR_RESET} "
                else:
                    row_str += f"{COLOR_CYAN}~{COLOR_RESET} "
            print(row_str)
        print()
