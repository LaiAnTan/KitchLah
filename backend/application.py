from flask import Flask, jsonify
from ai_prediction.main import run  # make sure run() is defined in main.py
from routes.alert import alert_bp
from routes.ingredients import ingredients_bp
from routes.restocks import restocks_bp
from routes.bedrock_api import bedrock_bp
from routes.crud import crud_bp
from flask_cors import CORS
from utils.database import db
from datetime import datetime, timedelta

application = Flask(__name__)
CORS(application)

def quantities_to_schedule(quantities, start_hour=6):
    schedule = []
    for i, qty in enumerate(quantities):
        hour = (start_hour + i) % 24  # wrap around if > 23
        # format into 12-hour AM/PM
        label = datetime.strptime(str(hour), "%H").strftime("%-I:00 %p")
        schedule.append({"hour": label, "quantity": qty})
    return schedule

@application.route("/forecast", methods=["GET"])
def forecast_endpoint():
    try:
        pred_day, _, _, llm_prompt, ai_response = run()

        # Convert hourly forecast (DataFrame) to dict-of-lists
        result = []
        for col in pred_day.columns[1:]:
            print(col)
            name = db.items.find_one({'name': col})
            if (name is None):
                continue
            quantities = pred_day[col].tolist()
            result.append({
                'menu': name["proper_name"],
                'quantity': sum(quantities),
                'hourlyBreakdown': quantities_to_schedule(quantities)
            })

        # Define dict in the order you want
        # result = {
        #     "hourly_forecast": data,
        #     "llm_prompt": llm_prompt,
        #     "ai_response": ai_response,
        # }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@application.route("/ingredients", methods=["GET"])
def ingredients_endpoint():
    try:
        _, _, df_ingredients, _, _ = run()

        result = {}
        for col in df_ingredients.columns:
            name = db.ingredients.find_one({ "_id": col })["name"]
            result[name] = df_ingredients[col].tolist()

        # result = {col: df_ingredients[col].tolist() for col in df_ingredients.columns}

        # reset_index() so "day" shows up in JSON
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

application.register_blueprint(alert_bp)
application.register_blueprint(ingredients_bp)
application.register_blueprint(bedrock_bp)
application.register_blueprint(restocks_bp)
application.register_blueprint(crud_bp)

if __name__ == "__main__":
    application.run(debug=True, host="0.0.0.0", port=5000)
