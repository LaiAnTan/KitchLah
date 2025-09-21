import pandas as pd
from recipes import MENU
from datetime import datetime

def compute_surge(pred_df, baseline_df, threshold=30):
    """
    Detect surge in forecasted orders compared to baseline.

    Args:
        pred_df (pd.DataFrame): Forecasted orders, columns include MENU and 'step'
        baseline_df (pd.DataFrame): Baseline orders, same MENU columns, 1 row per hour
        threshold (float): % increase to trigger surge

    Returns:
        pd.DataFrame: Surge alerts with 'hour', 'menu_item', 'forecasted', 'baseline', 'pct_increase'
    """
    surge_alerts = []

    for step in pred_df['step'].unique():
        # Convert step to actual hour (assuming forecast starts from hour 9)
        actual_hour = (step + 9) % 24
        if actual_hour > 20:  # Reset to 9 for next day
            actual_hour = 9 + (actual_hour - 21)
            
        for item in MENU:
            # Get forecasted value
            forecasted = pred_df.loc[pred_df['step'] == step, item].values[0]
            
            # Get baseline value - check if this hour exists in baseline
            baseline_row = baseline_df.loc[baseline_df['hour'] == actual_hour, item]  # Fixed: 'hour' not 'step'
            
            if len(baseline_row) == 0:
                # If no baseline data for this hour, use overall average
                baseline = baseline_df[item].mean()
                print(f"Warning: No baseline data for hour {actual_hour}, using overall average: {baseline:.2f}")
            else:
                baseline = baseline_row.values[0]

            # Avoid division by zero; if baseline = 0, treat as 100% surge if forecast > 0
            if baseline == 0 or pd.isna(baseline):
                if forecasted > 0:
                    pct_increase = 100.0
                else:
                    pct_increase = 0.0
                baseline = 0  # Set to 0 for display
            else:
                pct_increase = (forecasted - baseline) / baseline * 100

            if pct_increase >= threshold:
                surge_alerts.append({
                    "hour": actual_hour,
                    "step": step,
                    "menu_item": item,
                    "forecasted": forecasted,
                    "baseline": round(baseline, 2),
                    "pct_increase": round(pct_increase, 2)
                })

    return pd.DataFrame(surge_alerts)

def format_surge_for_llm(surge_df, current_hour=None):
    """
    Convert surge alerts DataFrame into a human-readable prompt for LLM,
    with friendly time labels like '5 PM'.

    Args:
        surge_df (pd.DataFrame): Output from compute_surge()
        current_hour (int): Current hour in 24-hour format. If None, assume current system hour.

    Returns:
        str: Human-readable alert text
    """

    if current_hour is None:
        current_hour = datetime.now().hour

    surge_df = surge_df[surge_df['hour'] > current_hour]

    if surge_df.empty:
        return "No surge expected in the upcoming hours. Everything is normal."

    next_hour = surge_df['hour'].min()
    next_surge = surge_df[surge_df['hour'] == next_hour]

    alerts = []
    for _, row in next_surge.iterrows():
        hour_label = f"{row['hour'] % 12 or 12} {'AM' if row['hour'] < 12 else 'PM'}"
        alerts.append(
            f"At {hour_label}, '{row['menu_item']}' orders are expected to increase by "
            f"{row['pct_increase']:.1f}%. Consider preparing extra stock or pre-cooking."
        )

    return "\n".join(alerts)
