import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import StandardScaler
from recipes import MENU

# -------------------- 1) Synthetic dataset --------------------
def load_data_from_csv(file_path='Data/kitchen_orders_synthetic.csv'):
    df = pd.read_csv(file_path, parse_dates=['date'])
    return df

# -------------------- 2) Dataset preprocessing --------------------
def prepare_dataset(df):

    # Filter to operating hours only
    df = df[(df['hour'] >= 9) & (df['hour'] <= 21)]

    # Aggregate to daily-hourly level
    wide = df.pivot_table(index=['date', 'day_of_week', 'hour'],
                          columns='menu_item', values='qty_ordered', fill_value=0).reset_index()
    

    # Ensure all menu items are present
    for m in MENU:
        if m not in wide.columns:
            wide[m] = 0

    # Sort by date and hour (time series order)
    daily_sorted = wide.sort_values(['date', 'hour'])

    hour_per_day = 12 # 9am-9pm
    window = 7 * hour_per_day  # 7 days of hourly data

    # Create rolling features
    for m in MENU:
        daily_sorted[f'{m}_ma7'] = daily_sorted[m].rolling(window=window, min_periods=1).mean()

    X = daily_sorted[['day_of_week', 'hour'] + [f'{m}_ma7' for m in MENU]].values

    y = daily_sorted[MENU].values

    return daily_sorted, X, y

# -------------------- 3) PyTorch Dataset --------------------
class KitchenDataset(Dataset):
    def __init__(self, X, y):
        if hasattr(X, 'values'):
            X = X.values
        if hasattr(y, 'values'):
            y = y.values

        if y.ndim == 1:
            y = y.reshape(-1, 1)

        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32)
    def __len__(self):
        return len(self.X)
    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]

# -------------------- 4) Model --------------------
class KitchenNN(nn.Module):
    def __init__(self, input_dim, output_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64,64),
            nn.ReLU(),
            nn.Linear(64, output_dim)
        )
    def forward(self, x):
        return self.net(x)

# -------------------- 5) Training function --------------------
def train_model(model, X, y, epochs=150, batch_size=8, lr=0.00035):
    
    scaler_x = StandardScaler()
    scaler_y = StandardScaler()
    x_scaled = scaler_x.fit_transform(X)
    y_scaled = scaler_y.fit_transform(y)

    dataset = KitchenDataset(x_scaled, y_scaled)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
   
   
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    
    for epoch in range(epochs):
        for xb, yb in loader:
            optimizer.zero_grad()
            preds = model(xb)
            loss = criterion(preds, yb)
            loss.backward()
            optimizer.step()
        if (epoch+1)%50==0:
            print(f"Epoch {epoch+1}, Loss: {loss.item():.3f}")
    return model, scaler_x, scaler_y
