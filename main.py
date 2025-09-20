import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from kitchen_model import KitchenNN, train_model, prepare_dataset, load_data_from_csv
from recipes import orders_to_ingredients, MENU
from forecast import forecast
from surge_detection import compute_surge, format_surge_for_llm
from datetime import datetime

def run():
    # -------------------- 1) Generate data --------------------
    df = load_data_from_csv('Data/kitchen_orders_synthetic.csv')
    daily_sorted, X, y = prepare_dataset(df)
    print("\n--- daily_sorted head ---")
    print(daily_sorted.head())

    print("\n--- daily_sorted columns ---")
    print(daily_sorted.columns.tolist())


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

    print("\nTotal predicted orders for next day:")
    print(total_day)

    print("\nForecasting next 7 days (hourly)...")
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

    # -------------------- 5) Surge detection --------------------

    # 1. Compute baseline (could be historical average or previous day)
    baseline_df = daily_sorted.groupby('hour')[MENU].mean().reset_index()
    print("Baseline data preview:")
    print(baseline_df.head())
    print(f"Baseline hours available: {sorted(baseline_df['hour'].unique())}")

    print("Forecast data preview:")
    print(pred_day.head())
    print(f"Forecast steps: {sorted(pred_day['step'].unique())}")

    # 2. Detect surges
    surge_df = compute_surge(pred_day, baseline_df, threshold=30)

    print("Surge detection results:")
    print(surge_df)

    # 3. Format for LLM
    current_hour = datetime.now().hour
    llm_prompt = format_surge_for_llm(surge_df, current_hour=current_hour)
    print(llm_prompt)

if __name__ == "__main__":
    run()