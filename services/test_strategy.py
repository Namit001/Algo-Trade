import pandas as pd
import numpy as np

# Import the functions
from services.strategy import apply_strategy

# Create a dummy dataset
np.random.seed(42)  # For reproducibility
data_length = 50
prices = np.random.uniform(low=100, high=200, size=data_length)

# Create a DataFrame
test_data = pd.DataFrame({
    "price": prices,
})

# Apply the strategy
processed_data = apply_strategy(test_data)

# Display the results
print(processed_data[["price", "signals", "macd_line", "signal_line","unrealised_gain_loss", "cumulative_pnl"]])
