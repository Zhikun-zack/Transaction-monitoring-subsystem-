import pandas as pd
from datetime import timedelta
from generate_transactions import generate_transactions

# Load and preprocess data
def load_data(file_path):
    df = pd.read_csv(file_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.sort_values(['user ID', 'timestamp'], inplace=True)
    return df


# Rule 1: Large Transaction Amount (>$10,000)
"""
Arguments:  
df (pd.DataFrame): The transaction dataset containing an 'amount' column.  
 
Returns:  
pd.Series: A boolean Series indicating whether each transaction is flagged under Rule 1.  
"""
def rule_large_amount(df):
    return df['amount'] > 10000


# Rule 2: Unusually High Transaction Amount (>X times user average)
"""
Arguments:
df (pd.DataFrame): The transaction dataset containing at least 'user ID' and 'amount' columns.
x (int or float, optional): The multiplier for determining unusually high transactions. Default is 5.

Returns:
pd.Series: A boolean Series indicating whether each transaction is flagged under Rule 2.
"""
def rule_unusually_high(df, x=5):
    user_means = df.groupby('user ID')['amount'].transform('mean')
    return df['amount'] > x * user_means

# Rule 3: Multiple Transactions in a Short Time Window (N or more in T minutes)
"""
Arguments:
df (pd.DataFrame): The transaction dataset containing at least 'user ID' and 'timestamp' columns.
n (int, optional): The minimum number of transactions required to trigger the rule. Default is 3.
t (int, optional): The time window in minutes within which the transactions must occur. Default is 5.

Returns:
pd.Series: A boolean Series indicating whether each transaction is flagged under Rule 3.
"""
def rule_multiple_transactions(df, n=3, t=5):
    df['rule3'] = False
    for user_id, user_group in df.groupby('user ID'):
        user_trans = user_group.sort_values('timestamp')
        for i in range(len(user_trans)):
            start = user_trans.iloc[i]['timestamp']
            end = start + pd.Timedelta(minutes=t)
            window = user_trans[(user_trans['timestamp'] >= start) & (user_trans['timestamp'] <= end)]
            if len(window) >= n:
                df.loc[window.index, 'rule3'] = True
    return df['rule3']

# Rule 4: Frequent Transactions to the Same Merchant (M or more in T minutes)
"""
Arguments:  
df (pd.DataFrame): The transaction dataset containing 'user ID', 'merchant name', and 'timestamp' columns.  
m (int, optional): The minimum number of transactions to the same merchant required to trigger the rule. Default is 3.  
t (int, optional): The time window in minutes within which the transactions must occur. Default is 60.  

Returns:  
pd.Series: A boolean Series indicating whether each transaction is flagged under Rule 4.  
"""
def rule_frequent_merchant(df, m=3, t=60):
    df['rule4'] = False
    for (user_id, merchant), group in df.groupby(['user ID', 'merchant name']):
        group = group.sort_values('timestamp')
        for i in range(len(group)):
            start = group.iloc[i]['timestamp']
            end = start + pd.Timedelta(minutes=t)
            window = group[(group['timestamp'] >= start) & (group['timestamp'] <= end)]
            if len(window) >= m:
                df.loc[window.index, 'rule4'] = True
    return df['rule4']

# Rule 5: Transaction Amount Rounding (round amounts > 10 * user average)
"""
Arguments:  
df (pd.DataFrame): The transaction dataset containing at least 'user ID' and 'amount' columns.  

Returns:  
pd.Series: A boolean Series indicating whether each transaction is flagged under Rule 5.  
"""
def rule_round_amount(df):
    user_means = df.groupby('user ID')['amount'].transform('mean')
    return (df['amount'] % 100 == 0) & (df['amount'] > 10 * user_means)


# Main function to flag suspicious transactions
"""
Arguments:  
file_path (str): The path to the CSV file containing transaction data.  

Process:  
1. Load transaction data into a DataFrame.  
2. Apply five fraud detection rules to flag suspicious transactions.  
3. Combine rule flags to determine which transactions are suspicious.  
4. Create a new column listing which rules were triggered for each suspicious transaction.  
5. Save the suspicious transactions to a new CSV file.  

Returns:  
pd.DataFrame: A DataFrame containing suspicious transactions with relevant details.  
"""
def flag_suspicious_transactions(file_path):
    df = load_data(file_path)
    
    # Apply rules
    df['rule1'] = rule_large_amount(df)
    df['rule2'] = rule_unusually_high(df, x=5)
    df['rule3'] = rule_multiple_transactions(df, n=3, t=5)
    df['rule4'] = rule_frequent_merchant(df, m=3, t=60)
    df['rule5'] = rule_round_amount(df)
    
    # Combine flags
    rules = ['rule1', 'rule2', 'rule3', 'rule4', 'rule5']
    df['suspicious'] = df[rules].any(axis=1)
    df['triggered_rules'] = df.apply(
        lambda row: [i for i, flag in enumerate(row[rules], 1) if flag], axis=1
    )
    
    # Output suspicious transactions
    suspicious_df = df[['user ID', 'timestamp', 'merchant name', 'amount', 'triggered_rules']]
    suspicious_df.to_csv('suspicious_transactions.csv', index=False)
    return suspicious_df

# Run the subsystem
if __name__ == "__main__":
    text_data_df = generate_transactions(1000)
    text_data_df.to_csv('transactions.csv', index=False)
    flagged_transactions = flag_suspicious_transactions('transactions.csv')
    print("Successfully detect all suspicious transactions!")