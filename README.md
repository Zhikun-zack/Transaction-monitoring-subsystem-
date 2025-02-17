# Transaction-monitoring-subsystem
This project contains two Python scripts for generating test transaction data and detecting fraudulent transactions based on predefined rules. The system is Dockerized for easy deployment and sharing.

------

## **Files Overview**

### 1. **`generate_transactions.py`**

- **Purpose**: Generates a sample CSV file (`transactions.csv`) with transaction data for testing the fraud detection system.
- **Fields in CSV**:
  - `user ID`: Unique identifier for the user.
  - `timestamp`: Timestamp of the transaction.
  - `merchant name`: Name of the merchant.
  - `amount`: Transaction amount.
- **Fraud Patterns Included**:
  - Large transactions (>$10,000).
  - Rapid successive transactions (multiple transactions within a short time).
  - Frequent transactions to the same merchant.
  - Unusually high transaction amounts.
  - Round transaction amounts.

------

### 2. **`fraud_detection.py`**

- **Purpose**: Detects fraudulent transactions based on the following rules
- **Output**:
  - Generates a CSV file (`suspicious_transactions.csv`) containing flagged transactions and the rules they triggered.

## Rules

#### **Rule 1: Large Transaction Amount**

- **Rule**: Flag transactions above $10,000.
- **Why**: High-value transactions are often targeted by fraudsters for maximum gain.

#### **Rule 2: Unusually High Transaction Amount**

- **Rule**: Flag transactions where the amount is **X times** (default: 5) greater than the user’s average transaction amount.
- **Why**: Fraudsters may attempt to withdraw large sums in a single transaction.

#### **Rule 3: Multiple Transactions in a Short Time Window**

- **Rule**: Flag users who make **N or more** transactions (default: 3) within a short period (default: 5 minutes).
- **Why**: This could indicate automated fraud (e.g., bot-driven attacks).

#### **Rule 4: Frequent Transactions to the Same Merchant**

- **Rule**: Flag users who transact with the same merchant **M or more times** (default: 3) within a short window (default: 1 hour).
- **Why**: This could be an attempt to exploit refund policies or card testing fraud.

#### **Rule 5: Transaction Amount Rounding**

- **Rule**: Flag transactions with round amounts (e.g., 100,200,500) that are significantly higher than the user’s average transaction amount (default: 10 times greater).
- **Why**: Fraudsters often use round numbers for testing or large fraudulent transactions.

------

## **How to Use**

### **Step 1: Clone the Repository**

Clone the project to your local machine:

```
git clone <repository-url>
cd fraud-detection-project
```

------

### **Step 2: Run the project**

1. **Build the Docker Image**:

   ```
   docker build -t fraud-detection-container .
   ```

2. **Run the Container**:

   - To run the fraud detection script:

     ```
     docker run -v $(pwd):/app fraud-detection-container
     ```

   - To run the transaction generation script:

     ```
     docker run -v $(pwd):/app fraud-detection-container python generate_transactions.py
     ```

   The `-v $(pwd):/app` flag mounts the current directory to the `/app` directory in the container, ensuring that input/output files are saved to your local machine.

------

## **Input/Output Files**

### **Input File**

- **`transactions.csv`**:
  - Contains transaction data with the following fields:
    - `user ID`
    - `timestamp`
    - `merchant name`
    - `amount`

### **Output File**

- **`suspicious_transactions.csv`**:
  - Contains flagged transactions with the following fields:
    - `user ID`
    - `timestamp`
    - `merchant name`
    - `amount`
    - `triggered_rules`: List of rules triggered by the transaction (e.g., `[1, 2]` for Rules 1 and 2).

------

## **Customization**

You can customize the rules by modifying the following parameters in `fraud_detection.py`:

- **Rule 2**: Set `x` in `rule_unusually_high(df, x=5)` to adjust the multiplier for unusually high transactions.
- **Rule 3**: Set `n` and `t` in `rule_multiple_transactions(df, n=3, t=5)` to adjust the number of transactions and time window.
- **Rule 4**: Set `m` and `t` in `rule_frequent_merchant(df, m=3, t=60)` to adjust the number of transactions and time window.
- **Rule 5**: Modify the logic in `rule_round_amount(df)` to adjust the rounding threshold.

------

## **Dependencies**

- Python 3.9
- Pandas
- Numpy

All dependencies are listed in `requirements.txt` and will be installed automatically when building the Docker image.

------

## **Contact**

For questions or issues, please contact Zhikun at xiaweiliang94@gmail.com.
