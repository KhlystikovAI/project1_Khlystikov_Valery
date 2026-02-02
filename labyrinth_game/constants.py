# labyrinth_game/constants.py

ROOMS: dict[str, dict] = {
    "entrance": {
        "description": (
            "Вы в темном входе лабиринта. Стены покрыты мхом. "
            "На полу лежит старый факел."
        ),
        "exits": {"north": "hall", "east": "trap_room"},
        "items": ["torch"],
        "puzzle": None,
    },
    "hall": {
        "description": (
            "Большой зал с эхом. По центру стоит пьедестал с запечатанным сундуком."
        ),
        "exits": {"south": "entrance", "west": "library", "north": "treasure_room"},
        "items": [],
        "puzzle": (
            'На пьедестале надпись: "Назовите число, которое идет после девяти". '
            "Введите ответ цифрой или словом.",
            "10",
        ),
    },
    "trap_room": {
        "description": (
            'Комната с хитрой плиточной поломкой. На стене видна надпись: '
            '"Осторожно — ловушка".'
        ),
        "exits": {"west": "entrance"},
        "items": ["rusty_key"],
        "puzzle": (
            'Система плит активна. Чтобы пройти, назовите слово "шаг" три раза подряд '
            '(введите "шаг шаг шаг")',
            "шаг шаг шаг",
        ),
    },
    "library": {
        "description": (
            "Пыльная библиотека. На полках старые свитки. Где-то здесь может быть ключ "
            "от сокровищницы."
        ),
        "exits": {"east": "hall", "north": "armory"},
        "items": ["ancient_book"],
        "puzzle": ('В одном свитке загадка: "Что растет, когда его съедают?"', "дырка"),
    },
    "armory": {
        "description": (
            "Старая оружейная комната. На стене висит меч, рядом — небольшая бронзовая "
            "шкатулка."
        ),
        "exits": {"south": "library"},
        "items": ["sword", "bronze_box"],
        "puzzle": None,
    },
    "treasure_room": {
        "description": (
            "Комната сокровищ. На столе большой сундук. Дверь позади захлопнулась. "
            "Сундук выглядит очень прочным."
        ),
        "exits": {"south": "hall"},
        "items": ["treasure_chest"],
        "puzzle": ("Дверь защищена кодом. Подсказка: 2*5 = ?", "10"),
    },
}

COMMANDS = {
    "go <dir>": "перейти в направлении (north/south/east/west)",
    "north": "перейти на север (также south/east/west)",
    "look": "осмотреть текущую комнату",
    "take <item>": "поднять предмет",
    "use <item>": "использовать предмет из инвентаря",
    "inventory": "показать инвентарь",
    "status": "показать статус игрока",
    "solve": "решить загадку или открыть сундук",
    "help": "показать это сообщение",
    "quit": "выйти из игры",
}
# случайные события
EVENT_ROLL_MODULO = 10          # вероятность события: 1/EVENT_ROLL_MODULO
EVENT_TYPES_COUNT = 3

# ловушки
TRAP_DEATH_THRESHOLD = 3        # roll < 3 -> game over
TRAP_DAMAGE_MODULO = 10

# лимит шагов
DEFAULT_MAX_STEPS = 25

