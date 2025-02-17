# Transaction-monitoring-subsystem
Fraud Detection System Documentation
This project contains two Python scripts for generating test transaction data and detecting fraudulent transactions based on predefined rules. The system is Dockerized for easy deployment and sharing.

Files Overview
1. generate_transactions.py
Purpose: Generates a sample CSV file (transactions.csv) with transaction data for testing the fraud detection system.

Fields in CSV:

user ID: Unique identifier for the user.

timestamp: Timestamp of the transaction.

merchant name: Name of the merchant.

amount: Transaction amount.

Fraud Patterns Included:

Large transactions (>$10,000).

Rapid successive transactions (multiple transactions within a short time).

Frequent transactions to the same merchant.

Unusually high transaction amounts.

Round transaction amounts.

2. fraud_detection.py
Purpose: Detects fraudulent transactions based on the following rules:

Rule 1: Large Transaction Amount
Rule: Flag transactions above $10,000.

Why: High-value transactions are often targeted by fraudsters for maximum gain.

Rule 2: Unusually High Transaction Amount
Rule: Flag transactions where the amount is X times (default: 5) greater than the user’s average transaction amount.

Why: Fraudsters may attempt to withdraw large sums in a single transaction.

Rule 3: Multiple Transactions in a Short Time Window
Rule: Flag users who make N or more transactions (default: 3) within a short period (default: 5 minutes).

Why: This could indicate automated fraud (e.g., bot-driven attacks).

Rule 4: Frequent Transactions to the Same Merchant
Rule: Flag users who transact with the same merchant M or more times (default: 3) within a short window (default: 1 hour).

Why: This could be an attempt to exploit refund policies or card testing fraud.

Rule 5: Transaction Amount Rounding
Rule: Flag transactions with round amounts (e.g., 
100
,
100,200) that are significantly higher than the user’s average transaction amount (default: 10 times greater).

Why: Fraudsters often use round numbers for testing or large fraudulent transactions.

Output:

Generates a CSV file (suspicious_transactions.csv) containing flagged transactions and the rules they triggered.

