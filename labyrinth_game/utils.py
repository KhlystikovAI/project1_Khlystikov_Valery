# labyrinth_game/utils.py

from labyrinth_game.constants import COMMANDS_HELP, ROOMS
def get_input(prompt: str = "> ") -> str:
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"



def show_help() -> None:
    print("\nДоступные команды:")
    for cmd, desc in COMMANDS_HELP.items():
        print(f"  {cmd:<15} - {desc}")


def describe_current_room(game_state: dict) -> None:
    room_name = game_state["current_room"]
    room_data = ROOMS[room_name]

    print(f"\n== {room_name.upper()} ==")
    print(room_data["description"])

    items = room_data["items"]
    if items:
        print("Заметные предметы:")
        for item in items:
            print(f"- {item}")

    exits = room_data["exits"]
    if exits:
        exits_list = ", ".join(exits.keys())
        print(f"Выходы: {exits_list}")

    if room_data["puzzle"] is not None:
        print('Кажется, здесь есть загадка (используйте команду solve).')


def solve_puzzle(game_state: dict) -> None:
    room_name = game_state["current_room"]
    puzzle = ROOMS[room_name]["puzzle"]

    if puzzle is None:
        print("Загадок здесь нет.")
        return

    question, correct_answer = puzzle
    print(question)
    user_answer = get_input("Ваш ответ: ").strip().lower()
    correct = str(correct_answer).strip().lower()

    if user_answer != correct:
        print("Неверно. Попробуйте снова.")
        return

    print("Верно! Загадка решена.")
    ROOMS[room_name]["puzzle"] = None

    # Награды — простой пример (можешь менять по сюжету)
    if room_name == "trap_room":
        if "treasure_key" not in game_state["player_inventory"]:
            game_state["player_inventory"].append("treasure_key")
            print("Вы нашли особый ключ: treasure_key")
    elif room_name == "library":
        if "hint_note" not in game_state["player_inventory"]:
            game_state["player_inventory"].append("hint_note")
            print("Вы нашли записку с подсказкой: hint_note")


def attempt_open_treasure(game_state: dict) -> None:
    room_name = game_state["current_room"]
    if room_name != "treasure_room":
        print("Здесь нет сокровищ, которые можно открыть.")
        return

    room_items = ROOMS[room_name]["items"]
    if "treasure_chest" not in room_items:
        print("Сундук уже открыт (или его здесь нет).")
        return

    inventory = game_state["player_inventory"]

    # 1) Открытие ключом
    if "treasure_key" in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room_items.remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
        return

    # 2) Попытка открыть кодом (взлом через загадку комнаты)
    answer = get_input("Сундук заперт. Попробовать ввести код? (да/нет) ").strip().lower()
    if answer != "да":
        print("Вы отступаете от сундука.")
        return

    puzzle = ROOMS[room_name]["puzzle"]
    if puzzle is None:
        print("Подсказок нет, а код вы не знаете.")
        return

    _question, correct_code = puzzle
    code = get_input("Введите код: ").strip().lower()
    correct = str(correct_code).strip().lower()

    if code == correct:
        print("Код верный! Замок поддался.")
        ROOMS[room_name]["puzzle"] = None
        room_items.remove("treasure_chest")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
    else:
        print("Неверный код.")
