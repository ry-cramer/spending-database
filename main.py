# %%
import sqlite3
import pandas as pd
# %%
# Functions for inserting into the database

# Inserting new transaction type (Function not accessible in main program right now)
def insert_transaction_type(name, cur):
    id = cur.execute('SELECT TransactionID FROM Transactions ORDER BY TransactionID DESC LIMIT 1').fetchone() + 1
    
    # Fetch SubscriptionID
    sub_type = input('Is this purchase made ONCE, DAILY, WEEKLY, MONTHLY, or YEARLY?')
    if sub_type.lower() == 'once':
        sub_freq = 1
    else: 
        sub_freq = int(input('Do you make this purchase every 1, 2, or 3 days/months/etc.? '))
    sub_id = cur.execute('SELECT SubscriptionID FROM Subscriptions WHERE SubscriptionType = ? AND Frequency = ?')
    
    categories = ['Gas', 'Food', 'Rent', 'Academic', 'Health', 'Hobbies', 'Entertainment', 'Other']
    while True:
        category_num = input('''What category of purchase does this fall under?
            1. Gas
            2. Food
            3. Rent
            4. Academic
            5. Health
            6. Hobbies
            7. Entertainment
            8. Other
            Type the corresponding number: ''')
        try:
            category = categories[category_num - 1]
        except:
            continue
        break
    
    necessity = input('Was this transaction a necessity? y/n: ')
    necessity = 1 if necessity.lower() == 'y' else 0
    
    row = (id, sub_id, name, category, necessity)
    cur.execute('INSERT INTO Transactions VALUES (?,?,?,?,?)', row)
    
# Function for inserting new transaction to TransactionHistory table
def insert_new_transaction(con, cur):
    id = int(pd.read_sql_query('SELECT TransactionHistoryID FROM TransactionHistory ORDER BY TransactionHistoryID DESC LIMIT 1', con)['TransactionHistoryID'][0]) + 1
    name = input('What is the name of this transaction? ')

    # Pulling matching transaction from Transactions table
    names = pd.read_sql_query(f'SELECT * FROM Transactions WHERE Name == "{name}"', con)
    if not names.empty:
        print(names)
        correct = int(input('Which transaction is it? Type the ID number or nothing if none of the transactions match. '))
        try:
            cur.execute(f'SELECT TransactionID FROM Transactions WHERE TransactionID == "{correct}"')
            transaction_id = correct
        except:
            print('This transaction type doesn\'t exist, and the functionality to create it is coming soon. Try again later')
            return
            # transaction_id = insert_transaction_type(name, cur)
    else:
        print('This transaction type doesn\'t exist, and the functionality to create it is coming soon. Try again later')
        return
        # transaction_id = insert_transaction_type(name, cur)

    amount = float(input('How much was it? Type only the number as a floating point number with two decimal places (ex 00.00): '))
    date = input('When did you make this purchase? (format dd-mm-yyyy) ')
    
    row = (id, transaction_id, date, amount)
    cur.execute('INSERT INTO TransactionHistory VALUES (?,?,?,?)', row)
    con.commit()

# %%
# Functions for editing the database
def edit_transaction_history():
    print('Coming Soon...')
# %% 
# Functions for querying the database
def query_transaction_history(con):
    query = '''SELECT Transactions.Name, TransactionHistory.Date, TransactionHistory.Amount 
        FROM TransactionHistory 
        LEFT JOIN Transactions 
        ON TransactionHistory.TransactionID == Transactions.TransactionID
        ORDER BY Date'''
    display_results(query, con)

# %%
def display_results(query, con):
    display = pd.read_sql_query(query, con)
    print(display)
    input('Press Enter to continue')

# %%
# Main cell (runs the interaction program)
def main(con, cur):
    print('Welcome to the transaction database!')
    while True:
        print(
        '''Main Menu:
        1. Insert a new transaction
        2. View transaction history
        3. Edit transaction history
        4. Exit transaction database''')
        menu_selection = input('Enter the number corresponding to your menu selection: ')

        if menu_selection == '1':
            insert_new_transaction(con, cur)
        elif menu_selection == '2':
            query_transaction_history(con)
        elif menu_selection == '3':
            edit_transaction_history(con, cur)
        elif menu_selection == '4':
            break
        else:
            print('Invalid input. Please try again.')

    print('Thank you for using the transaction database')
# %%
if __name__ == '__main__':
    con = sqlite3.connect('total_spending.db')
    cur = con.cursor()
    main(con, cur)
    con.close()
# %%
