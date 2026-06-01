_GOAL_ADJUSTMENT = {
    "похудеть": -300,
    "поддержать вес": 0,
    "набрать массу": +300,
}


def calculate_kbzhu(
    height: float, weight: float, age: int, gender: str, goal: str
) -> dict:
    if gender == "мужской":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    calories = bmr * 1.55 + _GOAL_ADJUSTMENT.get(goal, 0)

    protein = weight * 2.0
    fat = (calories * 0.25) / 9
    carbs = (calories - protein * 4 - fat * 9) / 4

    return {
        "calories": round(calories),
        "protein": round(protein),
        "fat": round(fat),
        "carbs": round(carbs),
    }
