# analyze_orders.py
import numpy as np
import pandas as pd
from recipes import MENU  # make sure this contains your menu items list

def main():
    # -------------------- 1) Load dataset --------------------
    df = pd.read_csv("Data/kitchen_orders_synthetic.csv", parse_dates=["date"])
    
    # Pivot the data to get a column for each menu item
    df_pivot = df.pivot_table(index=["date", "day_of_week", "hour"],
                              columns="menu_item",
                              values="qty_ordered",
                              aggfunc=np.sum).fillna(0).reset_index()

    # -------------------- 2) Overall average orders --------------------
    avg_orders = df_pivot[MENU].mean()
    print("Average orders per menu item (overall):")
    print(avg_orders)
    print("\n--------------------------\n")
    
    # -------------------- 3) Average orders per hour --------------------
    avg_hourly = df_pivot.groupby("hour")[MENU].mean()
    print("Average orders per menu item (per hour):")
    print(avg_hourly)
    print("\n--------------------------\n")
    
    # -------------------- 4) Average orders per day of week --------------------
    avg_weekday = df_pivot.groupby("day_of_week")[MENU].mean()
    print("Average orders per menu item (per day of week):")
    print(avg_weekday)
    print("\n--------------------------\n")
    

if __name__ == "__main__":
    main()
