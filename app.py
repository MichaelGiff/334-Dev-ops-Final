from flask import Flask, jsonify, render_template, request

from recommender import add_rating, recommend_recipes


app = Flask(__name__)


def _form_data_from_request():
    return {
        "meal_type": request.form.get("meal_type", "").strip(),
        "ingredients": request.form.get("ingredients", "").strip(),
        "dietary_preference": request.form.get("dietary_preference", "").strip(),
    }


def _recommendations_for(form_data):
    return recommend_recipes(
        meal_type=form_data["meal_type"],
        ingredients_text=form_data["ingredients"],
        dietary_preference=form_data["dietary_preference"],
    )


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "recipe-recommender"})


@app.route("/", methods=["GET", "POST"])
def index():
    recommendations = []
    form_data = {"meal_type": "", "ingredients": "", "dietary_preference": ""}
    status_message = ""

    if request.method == "POST":
        form_data = _form_data_from_request()
        recommendations = _recommendations_for(form_data)

    return render_template(
        "index.html",
        recommendations=recommendations,
        form_data=form_data,
        status_message=status_message,
    )


@app.post("/rate")
def rate_recipe():
    form_data = _form_data_from_request()
    recipe_name = request.form.get("recipe_name", "").strip()
    rating = request.form.get("rating", "").strip()
    status_code = 200

    try:
        average_rating = add_rating(recipe_name, rating)
        status_message = f"Saved {rating}/5 for {recipe_name}. New average: {average_rating}/5."
    except ValueError as error:
        status_message = str(error)
        status_code = 400

    return (
        render_template(
            "index.html",
            recommendations=_recommendations_for(form_data),
            form_data=form_data,
            status_message=status_message,
        ),
        status_code,
    )


if __name__ == "__main__":
    app.run(debug=True)
