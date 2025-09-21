from flask import Flask, jsonify
from ai_prediction.main import run  # make sure run() is defined in main.py
from routes.alert import alert_bp
from routes.ingredients import ingredients_bp
from routes.restocks import restocks_bp
from routes.bedrock_api import bedrock_bp
from routes.crud import crud_bp

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

app.register_blueprint(alert_bp)
app.register_blueprint(ingredients_bp)
app.register_blueprint(bedrock_bp)
app.register_blueprint(restocks_bp)
app.register_blueprint(crud_bp)

if __name__ == "__main__":
    # Flask’s dev server
    app.run(debug=True, host="0.0.0.0", port=5000)
