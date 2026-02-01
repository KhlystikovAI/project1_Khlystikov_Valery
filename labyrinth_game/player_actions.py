# labyrinth_game/player_actions.py

from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room, get_input, random_event, check_steps_limit




def show_inventory(game_state: dict) -> None:
    inventory = game_state["player_inventory"]
    if not inventory:
        print("Инвентарь пуст.")
        return
    print("Ваш инвентарь:")
    for item in inventory:
        print(f"- {item}")


def move_player(game_state: dict, direction: str) -> None:
    current_room = game_state["current_room"]
    room_data = ROOMS[current_room]
    exits = room_data["exits"]

    if direction not in exits:
        print("Нельзя пойти в этом направлении.")
        return

    game_state["current_room"] = exits[direction]
    game_state["steps_taken"] += 1
    random_event(game_state)

    random_event(game_state)
    check_steps_limit(game_state)
    if game_state["game_over"]:
        return

    describe_current_room(game_state)



def take_item(game_state: dict, item_name: str) -> None:
    current_room = game_state["current_room"]
    room_items = ROOMS[current_room]["items"]

    if item_name == "treasure_chest":
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return

    if item_name not in room_items:
        print("Такого предмета здесь нет.")
        return

    game_state["player_inventory"].append(item_name)
    room_items.remove(item_name)
    print(f"Вы подняли: {item_name}")


def use_item(game_state: dict, item_name: str) -> None:
    inventory = game_state["player_inventory"]

    if item_name not in inventory:
        print("У вас нет такого предмета.")
        return

    match item_name:
        case "torch":
            print("Вы поднимаете факел. Вокруг становится светлее.")
        case "sword":
            print("Вы сжимаете меч. Чувствуете уверенность.")
        case "bronze_box":
            print("Вы открываете бронзовую шкатулку...")
            if "rusty_key" not in inventory:
                inventory.append("rusty_key")
                print("Внутри лежал ключ! Вы получили: rusty_key")
            else:
                print("Шкатулка пуста.")
        case _:
            print("Вы не знаете, как использовать этот предмет.")
