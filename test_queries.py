import sqlite3
import pandas as pd

con = sqlite3.connect('total_spending.db')
cur = con.cursor()

# Insert test queries here
table = 'TransactionHistory'
column_to_edit = 'Date'
dtype = pd.read_sql_query(f'SELECT name, type FROM pragma_table_info("TransactionHistory") WHERE name == \'Date\'', con)['type'][0]
print(dtype)

con.close()