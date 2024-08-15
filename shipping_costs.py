def calculate_shipping_cost(
        distance: int,
        dimensions: str,
        fragile: bool,
        busy_factor: str
) -> float:
    shipping_cost = 0.0

    # Хрупкие грузы нельзя возить на расстояние более 30 км
    if fragile and distance > 30:
        raise ValueError("Fragile items cannot be shipped more than 30 km.")

    # Расчет стоимости в зависимости от расстояния
    if distance > 30:
        shipping_cost = 300
    elif distance > 10:
        shipping_cost = 200
    elif distance > 2:
        shipping_cost = 100
    else:
        shipping_cost = 50

    # Добавление стоимости в зависимости от габаритов
    if dimensions == "big":
        shipping_cost += 200
    elif dimensions == "small":
        shipping_cost += 100

    # Учет хрупкости груза
    if fragile:
        shipping_cost += 300

    # Учет загруженности службы доставки
    if busy_factor == "very_high":
        shipping_cost *= 1.6
    elif busy_factor == "high":
        shipping_cost *= 1.4
    elif busy_factor == "elevated":
        shipping_cost *= 1.2
    elif busy_factor == "normal":
        shipping_cost *= 1

    # Проверка минимальной суммы доставки
    return max(400.0, shipping_cost)
