from copy import deepcopy

import pytest

from recommender import add_rating, normalize_ingredients, recommend_recipes
from recipes import RECIPES


def test_normalize_ingredients_splits_and_lowercases_values():
    assert normalize_ingredients(" Eggs, tomato ,Spinach ") == ["eggs", "tomato", "spinach"]


def test_recommend_recipes_filters_by_meal_type():
    recipes = recommend_recipes(meal_type="breakfast")

    assert recipes
    assert all(recipe["meal_type"] == "breakfast" for recipe in recipes)


def test_recommend_recipes_filters_by_dietary_preference():
    recipes = recommend_recipes(dietary_preference="vegan")

    assert recipes
    assert all(recipe["dietary_preference"] == "vegan" for recipe in recipes)


def test_recommend_recipes_sorts_by_number_of_matched_ingredients():
    recipes = recommend_recipes(ingredients_text="broccoli, soy sauce, carrot")

    assert recipes[0]["name"] == "Tofu Stir Fry"
    assert recipes[0]["match_score"] == 3


def test_recommend_recipes_returns_empty_when_no_ingredient_matches():
    recipes = recommend_recipes(ingredients_text="salmon, dill")

    assert recipes == []


def test_add_rating_updates_average_rating():
    recipe_copy = deepcopy(RECIPES)

    average_rating = add_rating("Veggie Omelet", 3, recipe_copy)

    assert average_rating == 4.0
    assert recipe_copy[0]["ratings"][-1] == 3


def test_add_rating_rejects_invalid_rating():
    with pytest.raises(ValueError, match="between 1 and 5"):
        add_rating("Veggie Omelet", 6, deepcopy(RECIPES))


def test_add_rating_raises_when_recipe_is_missing():
    with pytest.raises(ValueError, match="Recipe not found"):
        add_rating("Missing Recipe", 4, deepcopy(RECIPES))
