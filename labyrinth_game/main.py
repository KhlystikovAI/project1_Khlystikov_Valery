#!/usr/bin/env python3

from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import (
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle,
)


def process_command(game_state: dict, command_line: str) -> None:
    command_line = command_line.strip()
    if not command_line:
        return

    parts = command_line.split()
    command = parts[0].lower()
    arg = " ".join(parts[1:]).strip().lower() if len(parts) > 1 else ""

    match command:
        case "help":
            show_help()
        case "look":
            describe_current_room(game_state)
        case "inventory":
            show_inventory(game_state)
        case "go":
            if not arg:
                print("Укажите направление: go north/south/east/west")
                return
            move_player(game_state, arg)
        case "take":
            if not arg:
                print("Укажите предмет: take <item>")
                return
            take_item(game_state, arg)
        case "use":
            if not arg:
                print("Укажите предмет: use <item>")
                return
            use_item(game_state, arg)
        case "solve":
            # В комнате сокровищ solve пытается открыть сундук (ключом или кодом),
            # иначе — решает загадку комнаты.
            if game_state["current_room"] == "treasure_room":
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case "quit" | "exit":
            print("Выход из игры.")
            game_state["game_over"] = True
        case _:
            print('Неизвестная команда. Введите "help" для списка команд.')


def main() -> None:
    game_state = {
        "player_inventory": [],
        "current_room": "entrance",
        "game_over": False,
        "steps_taken": 0,
    }

    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)
    show_help()

    while not game_state["game_over"]:
        command_line = get_input("> ")
        process_command(game_state, command_line)


if __name__ == "__main__":
    main()
