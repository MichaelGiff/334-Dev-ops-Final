import re
from copy import deepcopy

from recipes import RECIPES


INGREDIENT_ALIASES = {
    "bell peppers": "bell pepper",
    "bell pepper": "bell pepper",
    "black beans": "black bean",
    "black bean": "black bean",
    "chickpeas": "chickpea",
    "chickpea": "chickpea",
    "eggs": "egg",
    "egg": "egg",
    "noodles": "noodle",
    "noodle": "noodle",
    "oats": "oat",
    "oatmeal": "oat",
    "tomatoes": "tomato",
    "tomato": "tomato",
    "veggies": "vegetable",
    "vegetables": "vegetable",
}

DIETARY_COMPATIBILITY = {
    "vegan": {"vegan"},
    "vegetarian": {"vegetarian", "vegan"},
    "high-protein": {"high-protein"},
    "gluten-free": {"gluten-free"},
}


def _normalize_text(value):
    return " ".join(value.strip().lower().split())


def _canonical_ingredient(ingredient):
    normalized = _normalize_text(ingredient)
    return INGREDIENT_ALIASES.get(normalized, normalized)


def normalize_ingredients(ingredients_text):
    if not ingredients_text:
        return []

    parts = re.split(r",|;|\n|\s+and\s+", ingredients_text)
    normalized = []
    seen = set()
    for part in parts:
        ingredient = _canonical_ingredient(part)
        if ingredient and ingredient not in seen:
            normalized.append(ingredient)
            seen.add(ingredient)

    return normalized


def _recipe_ingredient_index(recipe):
    return {
        _canonical_ingredient(ingredient): ingredient
        for ingredient in recipe["ingredients"]
    }


def _matches_dietary_preference(recipe_preference, requested_preference):
    if not requested_preference:
        return True

    compatible_preferences = DIETARY_COMPATIBILITY.get(
        requested_preference,
        {requested_preference},
    )
    return recipe_preference in compatible_preferences


def recommend_recipes(meal_type="", ingredients_text="", dietary_preference="", limit=5):
    requested_ingredients = normalize_ingredients(ingredients_text)
    normalized_meal_type = _normalize_text(meal_type)
    normalized_preference = _normalize_text(dietary_preference)

    matches = []
    for recipe in RECIPES:
        if normalized_meal_type and recipe["meal_type"] != normalized_meal_type:
            continue

        if not _matches_dietary_preference(
            recipe["dietary_preference"],
            normalized_preference,
        ):
            continue

        ingredient_index = _recipe_ingredient_index(recipe)
        matched_ingredients = [
            ingredient_index[ingredient]
            for ingredient in requested_ingredients
            if ingredient in ingredient_index
        ]
        missing_ingredients = [
            ingredient
            for ingredient in recipe["ingredients"]
            if _canonical_ingredient(ingredient) not in requested_ingredients
        ]

        if requested_ingredients and not matched_ingredients:
            continue

        match_score = len(matched_ingredients)
        coverage = (
            round(match_score / len(requested_ingredients), 2)
            if requested_ingredients
            else 0
        )
        recommendation_score = (
            (match_score * 10)
            - len(missing_ingredients)
            + float(recipe["average_rating"])
        )

        recipe_result = deepcopy(recipe)
        recipe_result.update(
            {
                "matched_ingredients": matched_ingredients,
                "missing_ingredients": missing_ingredients,
                "match_score": match_score,
                "ingredient_coverage": coverage,
                "recommendation_score": round(recommendation_score, 2),
            }
        )
        matches.append(recipe_result)

    ranked_matches = sorted(
        matches,
        key=lambda recipe: (
            -recipe["match_score"],
            len(recipe["missing_ingredients"]),
            -recipe["average_rating"],
            recipe["name"],
        ),
    )

    return ranked_matches[:limit] if limit else ranked_matches


def add_rating(recipe_name, rating, recipes=None):
    recipe_collection = recipes if recipes is not None else RECIPES

    try:
        normalized_rating = int(rating)
    except (TypeError, ValueError) as exc:
        raise ValueError("Rating must be a whole number between 1 and 5.") from exc

    if normalized_rating < 1 or normalized_rating > 5:
        raise ValueError("Rating must be between 1 and 5.")

    for recipe in recipe_collection:
        if recipe["name"] == recipe_name:
            recipe["ratings"].append(normalized_rating)
            recipe["average_rating"] = round(
                sum(recipe["ratings"]) / len(recipe["ratings"]),
                2,
            )
            return recipe["average_rating"]

    raise ValueError("Recipe not found.")
