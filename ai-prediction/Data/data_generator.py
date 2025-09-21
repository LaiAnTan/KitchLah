import pandas as pd
import numpy as np

MENU = ["burger_fries", "fish_n_chip", "spaghetti", "chicken_chop"]

def generate_synthetic_data(days=60, seed=42):
    np.random.seed(seed)

    # Operating hours: 9am - 9pm
    hours = list(range(9, 22))  # 9 to 21 inclusive
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=days)

    rows = []
    for d in dates:
        dow = d.weekday()  # 0=Mon, 6=Sun
        is_weekend = dow >= 5

        for h in hours:
            # Base demand pattern
            time_factor = 1.0
            if 12 <= h <= 14:  # lunch peak
                time_factor = 1.8
            elif 18 <= h <= 20:  # dinner peak
                time_factor = 2.0
            elif 15 <= h <= 17:  # lull
                time_factor = 0.7

            weekend_factor = 1.3 if is_weekend else 1.0

            for menu in MENU:
                base = {
                    "burger_fries": 8,
                    "fish_n_chip": 6,
                    "spaghetti": 7,
                    "chicken_chop": 5
                }[menu]

                lam = base * time_factor * weekend_factor
                qty = np.random.poisson(lam)

                rows.append({
                    "date": d.date(),
                    "day_of_week": dow,
                    "hour": h,
                    "menu_item": menu,
                    "qty_ordered": qty
                })

    df = pd.DataFrame(rows)
    return df

if __name__ == "__main__":
    df = generate_synthetic_data(days=90)
    print(df.head(20))
    df.to_csv("kitchen_orders_synthetic.csv", index=False)
    print("\n✅ Synthetic dataset saved to kitchen_orders_synthetic.csv")
