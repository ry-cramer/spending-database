# %%
import sqlite3
import pandas as pd

con = sqlite3.connect('total_spending.db')
cur = con.cursor()

# %% 
# Initialize the database
# DO NOT RUN MORE THAN ONCE (will produce errors if tables are already in database)
cur.execute('''CREATE TABLE Subscriptions (
    SubscriptionID INTEGER PRIMARY KEY,
    SubscriptionType TEXT NOT NULL,
    Frequency INTEGER NOT NULL)''')

subscription_types = ['once', 'daily', 'weekly', 'monthly', 'yearly']
frequencies = [1, 2, 3]

def insert_subscriptions(subscription_types, frequencies):
    n = 0
    rows = []
    for i in subscription_types:
        for j in frequencies:
            new_row = (n, i, j)
            rows.append(new_row)
            n += 1

    return rows

cur.executemany('INSERT INTO Subscriptions VALUES (?,?,?)', insert_subscriptions(subscription_types, frequencies))

# Test query
q1 = 'SELECT * FROM Subscriptions'

cur.execute(q1)
print(cur.fetchall())

# Create the rest of the database
cur.execute('''CREATE TABLE Transactions (
    TransactionID INTEGER PRIMARY KEY,
    SubscriptionID INTEGER NOT NULL,
    Name TEXT NOT NULL,
    Category TEXT NOT NULL,
    Necessity INTEGER NOT NULL,
    FOREIGN KEY (SubscriptionID) REFERENCES Subscriptions(SubscriptionID)
    )''')

cur.execute('''CREATE TABLE TransactionHistory (
    TransactionHistoryID INTEGER PRIMARY KEY,
    TransactionID INTEGER NOT NULL,
    Date TEXT NOT NULL,
    Amount REAL NOT NULL,
    FOREIGN KEY (TransactionID) REFERENCES Transactions(TransactionID)
    )''')

# %%
# Functions for inserting into the database
def insert_transaction_type(id, name):
    
    pass

def insert_new_transaction():
    id = int(input('Enter a unique id number (must be an integer): '))
    name = input('What is the name of this transaction? ')
    names = pd.read_sql_query('SELECT Name FROM Transactions', con)
    if name in names:
        correct = input('Which transaction is it? Type the ID number or nothing if none of the transactions match. ')
        if correct in names:
            pass
            # transaction_id = # correct row id num
    else:
        transaction_id = insert_transaction_type(id, name)
    amount = float(input('How much was it? Type only the number as a floating point number with two decimal places (ex 00.00): '))
    date = input('When did you make this purchase? (format dd/mm/yyyy) ')
    row = (id, transaction_id, amount, date)
    cur.execute('INSERT INTO TransactionHistory VALUES (?,?,?,?)', row)

# %%
# Functions for editing the database
def edit_transaction_history():
    pass
# %% 
# Functions for querying the database
def query_transaction_history():
    pass

# %%
def display_results(query):
    display = pd.read_sql_query(query, con)
    print(display)

# %%
# Main cell (runs the interaction program)
def main():
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
            insert_new_transaction()
        elif menu_selection == '2':
            query_transaction_history()
        elif menu_selection == '3':
            edit_transaction_history()
        elif menu_selection == '4':
            break
        else:
            print('Invalid input. Please try again.')

    print('Thank you for using the transaction database')

if __name__ == 'main':
    main()