query_prompt_txn = '''
# Q: Calculate the average amount of transactions done for currency INR in 2024.
def func():
    df['Transaction_date'] = pd.to_datetime(df['Transaction_date'])
    filtered_df = df[(df['Currency'] == 'INR') & (df['Transaction_date'].dt.year == 2024)]
    summary = filtered_df.groupby(['Transaction_type', 'Currency', 'Transaction_id', 'Benename'])['Amount'] \
                         .mean() \
                         .reset_index(name='Average_Amount')
    
    return summary

# Q: what is the average amount transaction done for year 2024
def func():
    # Further filter DataFrame for transactions in the year 2024
    subdf = df[df['Transaction_date'].dt.year == 2024]
    
    # Calculate the average transaction amount for each transaction type
    findf = subdf.groupby(['Transaction_type', 'Currency'])['Amount'].mean().reset_index(name='mean_txn_amount')
    return findf
# Q: Top 10 transaction with maximum amount
def func():
    # Sort the DataFrame by the 'Amount' column in descending order
    top_transactions = df.sort_values(by='Amount', ascending=False)
    
    # Select the top 10 transactions
    findf = top_transactions.head(10)
    
    return findf
# Q: Details of Failed Transactions
def func():
    failed_df = df[df['Payment_status'] == 'Failed']
    return failed_df[['Transaction_id', 'User_id', 'Amount', 'Currency', 'Description', 'CountryCode', 'Benename']]
    
#Q: Top 10 Transactions by Amount in 2024
def func():
    df_2024 = df[df['Transaction_date'].dt.year == 2024]
    sorted_df = df_2024.sort_values(by='Amount', ascending=False).head(10)
    return sorted_df[['Transaction_id', 'Amount', 'Currency', 'Payment_status', 'CountryCode', 'Benename']]
def func():
    global df  # Assuming df is defined elsewhere as your DataFrame
    if query_type == 'Details of Failed Transactions':
        failed_df = df[df['Payment_status'] == 'Failed']
        return failed_df[['Transaction_id', 'User_id', 'Amount', 'Currency', 'Description', 'CountryCode', 'Benename']]
    elif query_type == 'Top 10 Transactions by Amount in 2024':
        df_2024 = df[df['Transaction_date'].dt.year == 2024]
        sorted_df = df_2024.sort_values(by='Amount', ascending=False).head(10)
        return sorted_df[['Transaction_id', 'Amount', 'Currency', 'Payment_status', 'CountryCode', 'Benename']]
    # Add more elif blocks for other queries
    else:
        return "Query type not supported."

# Q: {question}
'''.strip() + '\n' 