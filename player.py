from __future__ import annotations
from board import Board
from utils import COLOR_RED, COLOR_GREEN, COLOR_YELLOW, COLOR_RESET, clear_screen, show_message, ext


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.board = Board()
        self.enemy_view = Board(hidden=True)

    def print_commands(self) -> None:
        print("Формат ввода:")
        print("\n  <клетка> <горизонтально(h)/вертикально(v)> <длина корабля> — разместить корабль заданной длины (пример A1 h 4)")
        print("  done — закончить, если все корабли поставлены")
        print("  exit / quit — выйти из игры\n")

    def place_ships(self) -> None:
        fleet = {4: 1, 3: 2, 2: 3, 1: 4}
        need_clear = True 

        while True:
            if need_clear:
                clear_screen()
            else:
                need_clear = True

            print(f"\nИгрок: {self.name}\n")
            self.print_commands()
            self.board.display(show_ships=True)

            remaining = sum(fleet.values())
            if remaining == 0:
                print("Все корабли расставлены! Введите 'done', чтобы закончить.")
            else:
                print("Осталось кораблей:\n")
                for size, count in fleet.items():
                    if count > 0:
                        print(f"  {count} × корабль(ей) длиной {size}")

            command = input("\n> ").strip().lower()

            if command in ("exit", "quit"):
                ext()
                continue

            if remaining == 0 and command.lower() != 'done':
                show_message('Введите команду done!', COLOR_RED)
                continue

            elif command == "done":
                if sum(fleet.values()) == 0:
                    clear_screen()
                    print(f"\n{COLOR_GREEN}Расстановка завершена!\n{COLOR_RESET}")
                    self.board.display(show_ships=True)
                    input("Нажмите Enter для продолжения...")
                    clear_screen()
                    break
                else:
                    show_message("\nЕщё не все корабли расставлены!\n", COLOR_YELLOW)
                    clear_screen()
                    continue

            else:
                parts = command.split()
                if len(parts) != 3:
                    show_message("Формат ввода: A1 h 3", COLOR_RED)
                    clear_screen()
                    need_clear = False
                    continue

                coord, direction, size_str = parts
                try:
                    size = int(size_str)
                except ValueError:
                    show_message("Размер корабля должен быть числом.", COLOR_RED)
                    clear_screen()
                    need_clear = False
                    continue

                if size not in fleet or fleet[size] == 0:
                    show_message("Нет кораблей такого размера для размещения.", COLOR_RED)
                    clear_screen()
                    need_clear = False
                    continue

                placed, error = self.board.place_ship(coord, direction, size)
                if placed:
                    fleet[size] -= 1
                    show_message(f"Корабль длиной {size} размещён!", COLOR_GREEN)
                    clear_screen()
                else:
                    show_message(error, COLOR_RED)
                    clear_screen()
                    need_clear = False



    def make_move(self, opponent: Player) -> bool:
        while True:
            clear_screen()
            print(f"\nХод игрока: {self.name}\n")
            print("Ваше поле:\n")
            self.board.display(show_ships=True)
            print("Поле противника:\n")
            opponent.board.display(show_ships=False)

            coord = input("Введите координату для выстрела (например, B4)\n\n").strip().upper()

            result = opponent.board.shoot(coord)

            if result == "error":
                show_message("Неверная координата!", COLOR_RED)
                continue

            elif result == "repeat":
                input("\nНажмите Enter, чтобы выбрать другую клетку.")
                continue

            elif result == "hit":
                input("\nСделайте ещё один выстрел.\n")
                return True

            elif result == "sink":
                input("\nСделайте ещё один выстрел.\n")
                return True

            elif result == "miss":
                input("\nХод переходит к противнику.\n")
                return False