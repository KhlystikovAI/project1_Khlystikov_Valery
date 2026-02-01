# labyrinth_game/utils.py

import math

from labyrinth_game.constants import ROOMS


def get_input(prompt: str = "> ") -> str:
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def pseudo_random(seed: int, modulo: int) -> int:
    if modulo <= 0:
        return 0

    x = math.sin(seed * 12.9898) * 43758.5453
    frac = x - math.floor(x)
    return int(math.floor(frac * modulo))

def random_event(game_state: dict) -> None:
    steps = game_state.get("steps_taken", 0)

    # 10% шанс события
    if pseudo_random(steps, 10) != 0:
        return

    event_type = pseudo_random(steps + 7, 3)  # 0..2
    room_name = game_state.get("current_room", "")
    inventory = game_state.get("player_inventory", [])

    match event_type:
        case 0:
            # Находка
            print("Случайное событие: вы нашли на полу монетку!")
            room_items = ROOMS[room_name]["items"]
            if "coin" not in room_items:
                room_items.append("coin")

        case 1:
            # Испуг
            print("Случайное событие: вы слышите шорох в темноте...")
            if "sword" in inventory:
                print("Вы сжимаете меч — существо отступает.")

        case _:
            # Ловушка
            if room_name == "trap_room" and "torch" not in inventory:
                print("Случайное событие: без света здесь слишком опасно!")
                trigger_trap(game_state)

def pseudo_random(seed: int, modulo: int) -> int:
    if modulo <= 0:
        return 0

    x = math.sin(seed * 12.9898) * 43758.5453
    frac = x - math.floor(x)
    return int(math.floor(frac * modulo))


def trigger_trap(game_state: dict) -> None:
    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state.get("player_inventory", [])
    steps = game_state.get("steps_taken", 0)

    if inventory:
        idx = pseudo_random(steps, len(inventory))
        lost_item = inventory.pop(idx)
        print(f"Вы потеряли предмет: {lost_item}")
        return

    # Инвентарь пуст
    roll = pseudo_random(steps + 1, 10)  # 0..9
    if roll < 3:
        print("Ловушка сработала слишком сильно. Вы проиграли.")
        game_state["game_over"] = True
    else:
        print("Вы чудом уцелели и выбрались из ловушки.")


def show_help(commands: dict[str, str]) -> None:
    print("\nДоступные команды:")
    for cmd, desc in commands.items():
        left = (cmd + " " * 16)[:16]  # слева 16 символов, лишнее обрезаем
        print(f"  {left} {desc}")
        

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

NUMBER_ALIASES = {
    "0": {"ноль"},
    "1": {"один"},
    "2": {"два"},
    "3": {"три"},
    "4": {"четыре"},
    "5": {"пять"},
    "6": {"шесть"},
    "7": {"семь"},
    "8": {"восемь"},
    "9": {"девять"},
    "10": {"десять"},
}

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

    # Альтернативные варианты ответа
    accepted_answers = {correct}

    if correct in NUMBER_ALIASES:
        accepted_answers |= NUMBER_ALIASES[correct]

    if user_answer not in accepted_answers:
        print("Неверно. Попробуйте снова.")
        if room_name == "trap_room":
            trigger_trap(game_state)
        return

    print("Верно! Загадка решена.")
    ROOMS[room_name]["puzzle"] = None

    # Награды зависят от комнаты
    inventory = game_state["player_inventory"]

    match room_name:
        case "trap_room":
            if "treasure_key" not in inventory:
                inventory.append("treasure_key")
                print("Награда: вы нашли особый ключ: treasure_key")
        case "library":
            if "hint_note" not in inventory:
                inventory.append("hint_note")
                print("Награда: вы нашли записку с подсказкой: hint_note")
        case "hall":
            if "coin" not in inventory:
                inventory.append("coin")
                print("Награда: вы получили монету: coin")



def check_steps_limit(game_state: dict) -> None:
    max_steps = game_state.get("max_steps", 25)
    steps = game_state.get("steps_taken", 0)

    if steps < max_steps:
        return

    print("Вы слишком долго блуждали по лабиринту. Силы покидают вас...")
    game_state["game_over"] = True

def show_status(game_state: dict) -> None:
    room = game_state.get("current_room", "unknown")
    steps = game_state.get("steps_taken", 0)
    max_steps = game_state.get("max_steps", 25)
    remaining = max_steps - steps
    inventory_count = len(game_state.get("player_inventory", []))

    print("\n== STATUS ==")
    print(f"Комната: {room}")
    print(f"Шаги: {steps}/{max_steps} (осталось: {remaining})")
    print(f"Предметов в инвентаре: {inventory_count}")



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

    # 2) Открыть кодом
    answer = get_input(
        "Сундук заперт. Попробовать ввести код? (да/нет) "
        ).strip().lower()
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
