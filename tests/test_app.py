from copy import deepcopy

import pytest

from app import app
from recipes import RECIPES


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    return app.test_client()


def test_health_endpoint_returns_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_home_page_loads(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Recipe Recommender" in response.data


def test_recommendation_form_returns_matching_recipe(client):
    response = client.post(
        "/",
        data={
            "meal_type": "dinner",
            "ingredients": "tofu, broccoli, soy sauce",
            "dietary_preference": "vegan",
        },
    )

    assert response.status_code == 200
    assert b"Tofu Stir Fry" in response.data
    assert b"3 ingredient matches" in response.data


def test_rating_route_updates_recipe_and_rerenders_results(client):
    original_recipes = deepcopy(RECIPES)

    try:
        response = client.post(
            "/rate",
            data={
                "recipe_name": "Veggie Omelet",
                "rating": "5",
                "meal_type": "breakfast",
                "ingredients": "egg, spinach",
                "dietary_preference": "vegetarian",
            },
        )

        assert response.status_code == 200
        assert b"Saved 5/5 for Veggie Omelet" in response.data
        assert b"Veggie Omelet" in response.data
    finally:
        RECIPES[:] = original_recipes
