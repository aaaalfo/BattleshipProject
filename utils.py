import os
import sys
from typing import Tuple

COLOR_BLUE = "\033[94m"
COLOR_GREEN = "\033[92m"
COLOR_RED = "\033[91m"
COLOR_YELLOW = "\033[93m"
COLOR_CYAN = "\033[96m"
COLOR_RESET = "\033[0m"


def parse_coordinate(coord: str) -> Tuple[int, int]:
    coord = coord.strip().upper()

    if len(coord) < 2 or len(coord) > 3:
        raise ValueError("Неверный формат координаты. Пример: A1, J10")

    letter = coord[0]
    number = coord[1:]

    if not letter.isalpha() or not number.isdigit():
        raise ValueError("Неверный формат координаты. Пример: A1, J10")

    row = int(number) - 1  
    col = ord(letter) - ord('A')         

    if not (0 <= col < 10 and 0 <= row < 10):
        raise ValueError("Координата вне поля 10x10")
    return row, col

def clear_screen() -> None:
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()
    os.system('cls' if os.name == 'nt' else 'clear')

def show_message(message="", color=COLOR_YELLOW) -> None:
    print(f"\n{color}{message}{COLOR_RESET}")
    input("\nНажмите Enter, чтобы продолжить...")

def ext() -> None:
    confirm = input("\nВы уверены, что хотите выйти? (y/n): ").strip().lower()
    if confirm == "y":
        clear_screen()
        print("\nВы вышли из игры. До встречи, капитан!\n")
        sys.exit(0)
