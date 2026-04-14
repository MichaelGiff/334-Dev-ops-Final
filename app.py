from flask import Flask, render_template, request

from recommender import recommend_recipes


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    recommendations = []
    form_data = {"meal_type": "", "ingredients": "", "dietary_preference": ""}

    if request.method == "POST":
        form_data = {
            "meal_type": request.form.get("meal_type", "").strip(),
            "ingredients": request.form.get("ingredients", "").strip(),
            "dietary_preference": request.form.get("dietary_preference", "").strip(),
        }
        recommendations = recommend_recipes(
            meal_type=form_data["meal_type"],
            ingredients_text=form_data["ingredients"],
            dietary_preference=form_data["dietary_preference"],
        )

    return render_template(
        "index.html",
        recommendations=recommendations,
        form_data=form_data,
    )


if __name__ == "__main__":
    app.run(debug=True)
