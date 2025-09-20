import pandas as pd
import torch
import numpy as np
from recipes import MENU

def forecast(model, daily_sorted, scaler_X, scaler_y, horizon="day"):
    model.eval()
    preds = []

    # Copy history
    history = daily_sorted.copy()

    # Steps
    steps = 12 if horizon == "day" else 12*7

    for step in range(steps):
        # Use last row of history as features
        last_row = history.iloc[[-1]].copy()
        FEATURE_COLS = [c for c in last_row.columns if c not in MENU and not np.issubdtype(last_row[c].dtype, np.datetime64)]

        print("Feature columns during training:", FEATURE_COLS)

        # Scale features
        x_scaled = scaler_X.transform(last_row[FEATURE_COLS].values)

        x_raw = last_row[FEATURE_COLS].values
        print(f"Raw input range: {x_raw.min()} to {x_raw.max()}")
        # print(f"Scaler mean: {scaler_X.mean_}")
        # print(f"Scaler standard deviation: {scaler_X.scale_}")

        # Check if model weights are reasonable
        for name, param in model.named_parameters():
            print(f"{name}: mean={param.mean().item():.6f}, std={param.std().item():.6f}")

        # Predict
        with torch.no_grad():
            y_scaled = model(torch.tensor(x_scaled, dtype=torch.float32))
        y_pred = scaler_y.inverse_transform(y_scaled.numpy())[0]

        # Save predictions
        preds.append([step] + y_pred.tolist())

        # Prepare new row for history
        new_row = last_row.copy()
        for i, m in enumerate(MENU):
            last_7 = history[m].tail(7)
            new_row[f"{m}_ma7"] = pd.concat([last_7, pd.Series([y_pred[i]])]).mean()

        # Advance hour/day
        new_hour = (last_row["hour"].values[0] + 1)
        new_day_of_week = last_row["day_of_week"].values[0]
        if new_hour > 20:
            new_hour = 9
            new_day_of_week = (new_day_of_week + 1) % 7
        new_row["hour"] = new_hour
        new_row["day_of_week"] = new_day_of_week

       # Append to history for next step
        history = pd.concat([history, new_row], ignore_index=True)

    # Convert predictions to DataFrame
    pred_df = pd.DataFrame(preds, columns=["step"] + MENU)
    pred_df[MENU] = pred_df[MENU].clip(lower=0).round().astype(int)
    return pred_df
