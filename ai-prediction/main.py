import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from kitchen_model import KitchenNN, train_model, prepare_dataset, load_data_from_csv
from recipes import orders_to_ingredients, MENU
from forecast import forecast
from surge_detection import compute_surge, format_surge_for_llm
from datetime import datetime
from bedrock_client import call_bedrock


def run():
    # -------------------- 1) Generate data --------------------
    df = load_data_from_csv('Data/kitchen_orders_synthetic.csv')
    daily_sorted, X, y = prepare_dataset(df)

    # -------------------- 2) Scale features --------------------
    scaler_X = StandardScaler()
    scaler_y = StandardScaler()

    x_scaled = scaler_X.fit_transform(X)
    y_scaled = scaler_y.fit_transform(y)

    # -------------------- 2) Initialize & train model --------------------
    input_dim = X.shape[1]
    output_dim = len(MENU)
    model = KitchenNN(input_dim, output_dim)

    print("Training model...")
    model, scaler_X, scaler_y = train_model(model, x_scaled, y_scaled)
    print("Model training complete.")


    # -------------------- 3) Forecast --------------------
    print("\nForecasting next day (hourly)...")
    pred_day = forecast(model, daily_sorted, scaler_X, scaler_y, horizon="day")
    print(pred_day)
    total_day = pred_day[MENU].sum()

    #print("\nTotal predicted orders for next day:")
    #print(total_day)

    print("\nForecasting next 7 days...")
    pred_week = forecast(model, daily_sorted, scaler_X, scaler_y, horizon="week")
    
    hours_per_day = 12  # 9am-9pm
    pred_week ['day'] = pred_week['step'] // hours_per_day + 1

    daily_totals = pred_week.groupby('day')[MENU].sum().reset_index()
    print("\nDaily totals for the next 7 days:")
    print(daily_totals)

    # -------------------- 4) Convert orders -> ingredients --------------------
    # Aggregate predictions for the day
    total_day = pred_day[MENU].sum().to_dict()
    prep_list_day = orders_to_ingredients(total_day)

    print("\nIngredient prep for next day (grams/counts):")
    for k,v in prep_list_day.items():
        if 'count' in k or 'bun' in k:
            print(f"{k}: {v}")
        else:
            print(f"{k}: {v/1000:.2f} kg")

    # Aggregate predictions for the week
    total_week = pred_week[MENU].sum().to_dict()
    prep_list_week = orders_to_ingredients(total_week)

    print("\nIngredient prep for next 7 days (grams/counts):")
    for k,v in prep_list_week.items():
        if 'count' in k or 'bun' in k:
            print(f"{k}: {v}")
        else:
            print(f"{k}: {v/1000:.2f} kg")

    # -------------------- 4b) Convert daily menu totals -> daily ingredients --------------------
    ingredient_daily = []
    for _, row in daily_totals.iterrows():
        order_dict = row[MENU].to_dict()
        ingredients = orders_to_ingredients(order_dict)

        # convert grams → kg, keep counts as-is
        ingredients_kg = {
            k: (v/1000 if "count" not in k else v)
            for k, v in ingredients.items()
        }
        ingredients_kg["day"] = row["day"]
        ingredient_daily.append(ingredients_kg)

    df_ingredients = pd.DataFrame(ingredient_daily).set_index("day").fillna(0)

    print("\nDaily Ingredient Requirement (kg/count):")
    cols = ["chicken_patty_count", "fries", "bun_count", "lettuce",
        "fish_count", "batter", "pasta", "sauce", "cheese", "chicken_count"]

    print(df_ingredients.reindex(columns=cols, fill_value=0))

    # -------------------- 5) Surge detection --------------------

    # 1. Compute baseline (historical hourly averages)
    baseline_df = daily_sorted.groupby('hour')[MENU].mean().reset_index()
    # print("Baseline data preview:")
    # print(baseline_df.head())

    # print("Forecast data preview:")
    # print(pred_day.head())
    # print(f"Forecast steps: {sorted(pred_day['step'].unique())}")

    # 2. Detect surges
    surge_df = compute_surge(pred_day, baseline_df, threshold=30)
    # print("Surge detection results:")
    # print(surge_df)

    # 3. Format for LLM
    current_hour = datetime.now().hour
    llm_prompt = format_surge_for_llm(surge_df, current_hour=current_hour)
    print("\n--- LLM Prompt ---")
    print(llm_prompt)

    ai_response = None

    # 4. Send to Bedrock (only if surge detected)
    if llm_prompt.strip() != "No surge expected in the upcoming hours. Everything is normal.":
        try:
            from bedrock_client import call_bedrock

            ai_response = call_bedrock(
                f"""You are an assistant for restaurant kitchen staff.
                    Current time: {datetime.now().strftime('%I:%M %p')}.

                    The surge predictions are:
                    {llm_prompt}

                    Write a short, clear instruction for the staff.
                    Avoid technical terms and keep it practical."""
            )

            print("\n--- Bedrock AI Response ---")
            print(ai_response)

            # (Optional) Log to file
            with open("surge_alerts.txt", "a") as f:
                f.write(f"[{datetime.now()}]\n{ai_response}\n\n")

        except Exception as e:
            print("\nBedrock call failed:", str(e))
    else:
        print("\n--- No surge alerts, skipping Bedrock ---")

    return pred_day, daily_totals, df_ingredients, llm_prompt, ai_response



if __name__ == "__main__":
    run()
