import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate sample data
def generate_transactions(num_rows=1000):
    np.random.seed(42)
    user_ids = np.random.randint(1, 101, num_rows)  # 100 unique users
    timestamps = [datetime.now() - timedelta(minutes=np.random.randint(1, 1440)) for _ in range(num_rows)]
    merchants = np.random.choice(['Store A', 'Store B', 'Store C', 'Store D', 'Store E', 'Store F', 'Store G'], num_rows)
    amounts = np.round(np.random.exponential(100, num_rows), 2)  # Exponential distribution for realistic amounts

    # Create DataFrame
    df = pd.DataFrame({
        'user ID': user_ids,
        'timestamp': timestamps,
        'merchant name': merchants,
        'amount': amounts
    })

    # Add some fraudulent patterns
    df.loc[0:10, 'amount'] = 15000  # Large transactions (Rule 1)
    df.loc[10:20, 'timestamp'] = [df.loc[10, 'timestamp'] + timedelta(minutes=i) for i in range(11)]  # Multiple transactions in short time (Rule 3)
    df.loc[20:30, 'merchant name'] = 'Store A'  # Frequent transactions to same merchant (Rule 4)
    df.loc[30:40, 'amount'] = df.loc[30:40, 'amount'] * 10  # Unusually high transaction amount (Rule 2)
    df.loc[40:50, 'amount'] = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100]  # Round amounts (Rule 5)

    return df

# Save to CSV
df = generate_transactions(1000)
df.to_csv('transactions.csv', index=False)
print("Sample CSV file 'transactions.csv' generated successfully!")