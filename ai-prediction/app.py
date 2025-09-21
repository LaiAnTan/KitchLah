from flask import Flask, jsonify
from main import run  # make sure run() is defined in main.py

app = Flask(__name__)

@app.route("/forecast", methods=["GET"])
def forecast_endpoint():
    try:
        pred_day, _, _, llm_prompt, ai_response = run()

        # Convert hourly forecast (DataFrame) to dict-of-lists
        hourly_forecast = {col: pred_day[col].tolist() for col in pred_day.columns}

        # Define dict in the order you want
        result = {
            "hourly_forecast": hourly_forecast,
            "llm_prompt": llm_prompt,
            "ai_response": ai_response,
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/ingredients", methods=["GET"])
def ingredients_endpoint():
    try:
        _, _, df_ingredients, _, _ = run()

        result = {col: df_ingredients[col].tolist() for col in df_ingredients.columns}

        # reset_index() so "day" shows up in JSON
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Flask’s dev server
    app.run(debug=True, host="0.0.0.0", port=5000)
