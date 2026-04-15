from copy import deepcopy

from recipes import RECIPES


def normalize_ingredients(ingredients_text):
 
  #  Convert a comma-separated ingredient string into a clean lowercase list.

    if not ingredients_text.strip():
        return []

    return [
        item.strip().lower()
        for item in ingredients_text.split(",")
        if item.strip()
    ]


def recommend_recipes(meal_type="", ingredients_text="", dietary_preference=""):

  #  Filter recipes by meal type, dietary preference, and ingredient matches.
  #  Recipes with ingredient matches are sorted by highest match count first.
  
    normalized_ingredients = normalize_ingredients(ingredients_text)
    results = []

    for recipe in RECIPES:
        if meal_type and recipe["meal_type"] != meal_type:
            continue

        if dietary_preference and recipe["dietary_preference"] != dietary_preference:
            continue

        recipe_ingredients = [ingredient.lower() for ingredient in recipe["ingredients"]]

        match_score = 0
        if normalized_ingredients:
            match_score = sum(
                1 for ingredient in normalized_ingredients if ingredient in recipe_ingredients
            )
            if match_score == 0:
                continue

        recipe_copy = deepcopy(recipe)
        recipe_copy["match_score"] = match_score
        recipe_copy["average_rating"] = (
            sum(recipe["ratings"]) / len(recipe["ratings"]) if recipe["ratings"] else 0
        )
        results.append(recipe_copy)

    if normalized_ingredients:
        results.sort(key=lambda recipe: recipe["match_score"], reverse=True)

    return results


def add_rating(recipe_name, rating, recipes=None):

  #  Add a rating to a recipe and return the updated average rating.
  
    if rating < 1 or rating > 5:
        raise ValueError("Rating must be between 1 and 5")

    if recipes is None:
        recipes = RECIPES

    for recipe in recipes:
        if recipe["name"] == recipe_name:
            recipe["ratings"].append(rating)
            return sum(recipe["ratings"]) / len(recipe["ratings"])

    raise ValueError("Recipe not found")