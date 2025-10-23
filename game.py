from utils import COLOR_RESET, COLOR_GREEN, clear_screen
from player import Player
import time


class Game:
    def __init__(self) -> None:
        clear_screen()
        print()
        print("\nДобро пожаловать в игру МОРСКОЙ БОЙ!")
        self.setup_players()

    def setup_players(self) -> None:
        name1 = input("\nВведите имя первого игрока: ").strip() or "Игрок 1"
        name2 = input("\nВведите имя второго игрока: ").strip() or "Игрок 2"

        self.player1 = Player(name1)
        self.player2 = Player(name2)
        self.current_player = self.player1

        self.player1.place_ships()
        self.player2.place_ships()

    def play_loop(self) -> None:
        print("\nИгра началась! Первый ход делает", self.current_player.name)
        input("\nНажмите Enter, чтобы начать...")

        while True:
            clear_screen()
            opponent = self.player2 if self.current_player == self.player1 else self.player1

            continue_turn = self.current_player.make_move(opponent)
            if self.check_winner():
                break

            if not continue_turn:
                self.switch_turn()


    def switch_turn(self) -> None:
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1

    def start(self) -> None:
        self.play_loop()
        print("\nСпасибо за игру!\n")


    def check_winner(self) -> None:
        clear_screen()
        if self.player1.board.all_ships_sunk():
            print(f"{COLOR_GREEN}Все корабли потоплены!")
            time.sleep(1) # <- задержка для прикольного вывода
            print(f"\n{COLOR_GREEN}Победитель: {self.player2.name}!{COLOR_RESET}")
            return True

        if self.player2.board.all_ships_sunk():
            print(f"{COLOR_GREEN}Все корабли потоплены!")
            time.sleep(1)   # <- и тут
            print(f"\n{COLOR_GREEN}Победитель: {self.player1.name}!{COLOR_RESET}")
            return True

        return False