from recipes import RECIPES


def normalize_ingredients(ingredients_text):
    if not ingredients_text:
        return []

    return [
        ingredient.strip().lower()
        for ingredient in ingredients_text.split(",")
        if ingredient.strip()
    ]


def recommend_recipes(meal_type="", ingredients_text="", dietary_preference=""):
    requested_ingredients = normalize_ingredients(ingredients_text)
    normalized_meal_type = meal_type.strip().lower()
    normalized_preference = dietary_preference.strip().lower()

    matches = []
    for recipe in RECIPES:
        if normalized_meal_type and recipe["meal_type"] != normalized_meal_type:
            continue

        if normalized_preference and recipe["dietary_preference"] != normalized_preference:
            continue

        recipe_ingredients = {ingredient.lower() for ingredient in recipe["ingredients"]}
        matched_ingredients = [
            ingredient for ingredient in requested_ingredients if ingredient in recipe_ingredients
        ]

        if requested_ingredients and not matched_ingredients:
            continue

        matches.append(
            {
                **recipe,
                "matched_ingredients": matched_ingredients,
                "match_score": len(matched_ingredients),
            }
        )

    return sorted(matches, key=lambda recipe: (-recipe["match_score"], recipe["name"]))


def add_rating(recipe_name, rating, recipes=None):
    recipe_collection = recipes if recipes is not None else RECIPES

    if rating < 1 or rating > 5:
        raise ValueError("Rating must be between 1 and 5.")

    for recipe in recipe_collection:
        if recipe["name"] == recipe_name:
            recipe["ratings"].append(rating)
            recipe["average_rating"] = round(
                sum(recipe["ratings"]) / len(recipe["ratings"]), 2
            )
            return recipe["average_rating"]

    raise ValueError("Recipe not found.")
