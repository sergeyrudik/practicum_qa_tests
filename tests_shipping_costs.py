import pytest
from shipping_costs import calculate_shipping_cost


@pytest.mark.parametrize(
    "distance, dimensions, fragile, busy_factor, expected",
    [
        # Тесты для расстояния
        (31, "small", False, "normal", 400.0),  # >30 км, small
        (30, "small", False, "normal", 400.0),  # 30 км, small
        (11, "small", False, "normal", 400.0),  # >10 км, small
        (10, "small", False, "normal", 400.0),  # 10 км, small
        (3, "small", False, "normal", 400.0),  # >2 км, small
        (2, "small", False, "normal", 400.0),  # 2 км, small
        (1, "small", False, "normal", 400.0),  # 1 км, small, минимальная стоимость

        # Тесты для размеров
        (10, "big", False, "normal", 400.0),  # 10 км, big
        (10, "small", False, "normal", 400.0),  # 10 км, small
        (2, "big", False, "normal", 400.0),  # 2 км, big
        (2, "small", False, "normal", 400.0),  # 2 км, small
        (1, "big", False, "normal", 400.0),  # 1 км, big, минимальная стоимость

        # Тесты для хрупких грузов
        (10, "small", True, "normal", 500.0),  # 10 км, small, fragile
        (5, "big", True, "normal", 600.0),  # 5 км, big, fragile
    ]
)
def test_basic_cost(distance, dimensions, fragile, busy_factor, expected):
    result = calculate_shipping_cost(distance, dimensions, fragile, busy_factor)
    assert result == expected


@pytest.mark.parametrize(
    "distance, dimensions, fragile, busy_factor, expected",
    [
        (10, "small", False, "very_high", 400.0),  # (100 + 100) * 1.6
        (10, "small", False, "high", 400.0),  # (100 + 100) * 1.4
        (10, "small", False, "elevated", 400.0),  # (100 + 100) * 1.2
        (10, "small", False, "normal", 400.0),  # Без коэффициента

        # Проверка минимальной стоимости для всех комбинаций
        (1, "small", False, "normal", 400.0),
        (1, "big", False, "normal", 400.0),
        (1, "small", True, "normal", 450.0),  # (50 + 100) + 300
        (1, "big", True, "normal", 550.0),  # (50 + 200) + 300

        # Проверка комбинаций всех параметров
        (31, "big", False, "very_high", 800.0),  # 300 + 200 (big)
        (31, "small", False, "high", 560.0),  # 300 + 100 * 1.4
        (5, "big", True, "elevated", 720.0),  # (100 + 200 + 300) * 1.2
        (2, "small", False, "normal", 400.0),  # 50 + 100 (small)
        (2, "big", True, "elevated", 660.0),  # (50 + 200 + 300) * 1.2
    ]
)
def test_advanced_cost(distance, dimensions, fragile, busy_factor, expected):
    result = calculate_shipping_cost(distance, dimensions, fragile, busy_factor)
    assert result == expected


def test_fragile_restriction():
    with pytest.raises(ValueError, match="Fragile items cannot be shipped more than 30 km."):
        calculate_shipping_cost(31, "small", True, "normal")

