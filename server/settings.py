STIFFNESS_MAP = {
    "Banana": 1.0,
    "Ball": 2.0,
    "Cup": 1.5,
    "Glass": 0.5,
    "Mug": 1.0,
    "Bowl": 1.2,
    "Spoon": 5.0,
    "Fork": 5.0,
    "Knife": 8.0,
    "Metal": 10.0,
    "Toy": 2.5,
}
DEFAULT_STIFFNESS = 5.0


def map_stiffness(class_name: str) -> float:
    return STIFFNESS_MAP.get(class_name, DEFAULT_STIFFNESS)
