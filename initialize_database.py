# %%
import sqlite3
# %% 
# Initialize the database
# DO NOT RUN (will produce errors if tables are already in database)

def initialize_database(con, cur):
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

    # insert dummy data
    transactions_insert = [(1, 1, 'Walmart', 'Food', 1), (2, 1, 'Shell', 'Gas', 1), (3, 1, 'Shell', 'Food', 0)]
    cur.executemany('INSERT INTO Transactions VALUES (?,?,?,?,?)', transactions_insert)

    transaction_history_insert = [(1, 1, '01-01-2023', 50.00), (2, 2, '01-02-2023', 40.65), (3, 3, '01-02-2023', 2.43), (4, 1, '01-05-2023', 30.35), (5, 2, '01-07-2023', 43.22)]
    cur.executemany('INSERT INTO TransactionHistory VALUES (?,?,?,?)', transaction_history_insert)

    con.commit()

def test_database(cur):
    # Test query Subscriptions
    q1 = 'SELECT * FROM Subscriptions'
    cur.execute(q1)
    print(cur.fetchall())

    # Test query Transactions
    q2 = 'SELECT * FROM Transactions'
    cur.execute(q2)
    print(cur.fetchall())

    # Test query TransactionHistory
    q3 = 'SELECT * FROM TransactionHistory'
    cur.execute(q3)
    print(cur.fetchall())
# %%
if __name__ == '__main__':
    con = sqlite3.connect('total_spending.db')
    cur = con.cursor()

    # initialize_database(con, cur)
    test_database(cur)
    con.close()