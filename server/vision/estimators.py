from server.settings import map_stiffness


def estimate_stiffness(class_name: str) -> float:
    """
    Возвращает оценку жесткости объекта по его классу.
    """
    # TODO: Заменить табличные данные на динамику
    return map_stiffness(class_name)
