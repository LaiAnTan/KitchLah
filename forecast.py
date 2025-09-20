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


        # Extract and validate features
        x_raw = last_row[FEATURE_COLS].values
        
        # Check for invalid values in moving averages and fix them
        for i, col in enumerate(FEATURE_COLS):
            if col.endswith('_ma7') and x_raw[0][i] < 0:
                # Replace negative moving averages with recent positive average
                menu_item = col.replace('_ma7', '')
                recent_values = history[menu_item].tail(14)
                positive_values = recent_values[recent_values > 0]
                if len(positive_values) > 0:
                    x_raw[0][i] = positive_values.mean()
                else:
                    x_raw[0][i] = 1.0  # Fallback minimum


        # Scale features
        x_scaled = scaler_X.transform(x_raw)


        # Predict
        with torch.no_grad():
            y_scaled = model(torch.tensor(x_scaled, dtype=torch.float32))
        y_pred = scaler_y.inverse_transform(y_scaled.numpy())[0]
        
        # Ensure predictions are non-negative
        y_pred = np.maximum(y_pred, 0)
        
        # If all predictions are very small, use historical averages
        if np.max(y_pred) < 0.1:
            current_hour = last_row["hour"].values[0]
            current_day = last_row["day_of_week"].values[0]
            
            # Get historical data for same hour and day
            same_conditions = history[
                (history["hour"] == current_hour) & 
                (history["day_of_week"] == current_day)
            ]
            
            if len(same_conditions) > 0:
                for i, m in enumerate(MENU):
                    hist_avg = same_conditions[m].mean()
                    if hist_avg > 0:
                        y_pred[i] = max(hist_avg, 1.0)
                    else:
                        y_pred[i] = 1.0
            else:
                # Use overall averages as fallback
                for i, m in enumerate(MENU):
                    hist_avg = history[m].mean()
                    y_pred[i] = max(hist_avg, 1.0)

        # Save predictions
        preds.append([step] + y_pred.tolist())

        # Prepare new row for history
        new_row = last_row.copy()
        
        # Update menu item values with predictions
        for i, m in enumerate(MENU):
            new_row[m] = y_pred[i]
        
        # Update moving averages carefully
        for i, m in enumerate(MENU):
            # Get last 6 values (not 7, since we'll add the new prediction)
            last_6 = history[m].tail(6)
            # Calculate new 7-day moving average
            all_7_values = pd.concat([last_6, pd.Series([y_pred[i]])])
            new_ma = all_7_values.mean()
            
            # Ensure moving average doesn't become too small
            new_ma = max(new_ma, 0.5)
            new_row[f"{m}_ma7"] = new_ma

        # Advance hour/day
        new_hour = (last_row["hour"].values[0] + 1)
        new_day_of_week = last_row["day_of_week"].values[0]
        if new_hour > 20:
            new_hour = 9
            new_day_of_week = (new_day_of_week + 1) % 7
        new_row["hour"] = new_hour
        new_row["day_of_week"] = new_day_of_week

        # Advance date if needed (optional, for completeness)
        if new_hour == 9 and step > 0:  # New day started
            current_date = pd.to_datetime(last_row["date"].values[0])
            new_date = current_date + pd.Timedelta(days=1)
            new_row["date"] = new_date

       # Append to history for next step
        history = pd.concat([history, new_row], ignore_index=True)

    # Convert predictions to DataFrame
    pred_df = pd.DataFrame(preds, columns=["step"] + MENU)
    pred_df[MENU] = pred_df[MENU].clip(lower=0).round().astype(int)
    return pred_df