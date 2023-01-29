'''
Main file (Run this file to interact with the database)
Functions:
    display_results(query, con)
        Displays query results to the console
        Arguments:
            query: SQL formatted query to the total_spending database
            con: Connection object to the total_spending database
    insert_transaction_type(name, cur)
        Inserts a new transaction type to the Transactions table
        Arguments:
            name: The name of the transaction to be inserted (will be inserted under Name column in Transactions table)
            cur: Cursor object to execute SQL commands
    insert_new_transaction(con, cur)
        Inserts a new transaction to the TransactionHistory table
        Arguments:
            con: Connection object to the total_spending database
            cur: Cursor object to execute SQL commands
    edit_menu(con, cur)
        Base for editing the database. Chooses whether to edit or delete a selected row in the database
        Arguments:
            con: Connection object to the total_spending database
            cur: Cursor object to execute SQL commands
    edit_entry(table, table_id, to_edit, con, cur)
        Edits a value in a row in the database
        Arguments:
            table: Name of the table to be edited
            table_id: Name of the ID column of the table
            to_edit: ID number of row to be edited
            con: Connection object to the total_spending database
            cur: Cursor object to execute SQL commands
    delete_entry(table, table_id, to_delete, con, cur)
        Deletes a selected row in the database
        Arguments:
            table: Name of the table to be edited
            table_id: Name of the ID column of the table
            to_edit: ID number of row to be deleted
            con: Connection object to the total_spending database
            cur: Cursor object to execute SQL commands
    query_transaction_history(con)
        Creates a query for the main user view of the database, and outputs the result to the console
        Arguments:
            con: Connection object to the total_spending database
    main(con, cur)
        Main program loop
        Arguments:
            con: Connection object to the total_spending database
            cur: Cursor object to execute SQL commands
'''

import sqlite3
import pandas as pd

################## Function to display queries to console #########################
def display_results(query, con):
    display = pd.read_sql_query(query, con)
    print(display)

################# Functions for inserting into the database #########################

# Inserting new transaction type (Function not accessible in main program right now)
def insert_transaction_type(name, cur):
    id = cur.execute('SELECT TransactionID FROM Transactions ORDER BY TransactionID DESC LIMIT 1').fetchone() + 1
    
    # Fetch SubscriptionID (INC)
    sub_type = input('Is this purchase made ONCE, DAILY, WEEKLY, MONTHLY, or YEARLY?')
    if sub_type.lower() == 'once':
        sub_freq = 1
    else: 
        sub_freq = int(input('Do you make this purchase every 1, 2, or 3 days/months/etc.? '))
    # sub_id = cur.execute('SELECT SubscriptionID FROM Subscriptions WHERE SubscriptionType = ? AND Frequency = ?')
    
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

######################## Functions for editing the database ##################################
def edit_menu(con, cur):
    # Select table to edit
    tables = ['TransactionHistory', 'Transactions', 'Subscriptions']
    try:
        type_code = int(input('Which table do you want to edit? \n1. TransactionHistory \n2. Transactions \n3. Subscriptions \n'))
    except:
        print('Error: Please enter the number on the menu that corresponds to the table you want to edit.')
        return
    
    table = tables[type_code - 1]
    query_1 = f'SELECT * FROM {table}'
    display_results(query_1, con)

    # Select row to edit
    while True:
        try:
            to_edit = int(input(f'Which selection would you like to edit? Type the table ID number that you\'d like to select '))
            if table != 'TransactionHistory':
                table_id = table[:-1] + 'ID'
            else:
                table_id = table + 'ID'
            query_2 = f'SELECT * FROM {table} WHERE {table_id} = {to_edit}'
            cur.execute(query_2)
        except:
            print('Error: invalid selection')
            continue
        break
    
    display_results(query_2, con)

    # Choose whether to delete or edit. Can also exit at this stage if needed
    action = input('How do you want to handle this entry? \n1. Edit \n2. Delete \n3. Cancel\n')
    if action == '1':
        edit_entry(table, table_id, to_edit, con, cur)
    elif action == '2':
        delete_entry(table, table_id, to_edit, con, cur)
    elif action == '3':
        return
    else:
        print('Invalid input. Returning to main menu...')

def edit_entry(table, table_id, to_edit, con, cur):
    # Choose part of row to edit
    while True:
        column_to_edit = input('Which column would you like to change? ')
        try:
            pd.read_sql_query(f'SELECT {column_to_edit} FROM {table}', con)
        except:
            print('Error: invalid input')
            continue
        break
    
    # Edits chosen item
    while True:
        new_input = input('What would you like to change this value to? ')
        try:
            dtype = pd.read_sql_query(f'SELECT name, type FROM pragma_table_info(\'{table}\') WHERE name == \'{column_to_edit}\'', con)['type'][0]
            if dtype == 'INTEGER':
                new_input = int(new_input)
                cur.execute(f'UPDATE {table} SET {column_to_edit} == {new_input} WHERE {table_id} == {to_edit}')
            elif dtype == 'REAL':
                new_input = float(new_input)
                cur.execute(f'UPDATE {table} SET {column_to_edit} == {new_input} WHERE {table_id} == {to_edit}')
            else:
                cur.execute(f'UPDATE {table} SET {column_to_edit} == \'{new_input}\' WHERE {table_id} == {to_edit}')
        except:
            print('Error: invalid input')
            continue
        break

    con.commit()

def delete_entry(table, table_id, to_delete, con, cur):
    cur.execute(f'DELETE FROM {table} WHERE {table_id} == {to_delete}')
    con.commit()

############################ Functions for querying the database ##############################
def query_transaction_history(con):
    query = '''SELECT Transactions.Name, Transactions.Category, TransactionHistory.Date, TransactionHistory.Amount, Transactions.Necessity
        FROM TransactionHistory 
        LEFT JOIN Transactions 
        ON TransactionHistory.TransactionID == Transactions.TransactionID
        ORDER BY Date'''
    display_results(query, con)
    input('Press Enter to continue')

############################# Main cell (runs the interaction program) ##################################
def main(con, cur):
    print('Welcome to the transaction database!')
    while True:
        print(
        '''Main Menu:
        1. Insert a new transaction
        2. View transaction history
        3. Edit transaction database
        4. Exit transaction database''')
        menu_selection = input('Enter the number corresponding to your menu selection: ')

        if menu_selection == '1':
            insert_new_transaction(con, cur)
        elif menu_selection == '2':
            query_transaction_history(con)
        elif menu_selection == '3':
            edit_menu(con, cur)
        elif menu_selection == '4':
            break
        else:
            print('Invalid input. Please try again.')

    print('Thank you for using the transaction database')

if __name__ == '__main__':
    con = sqlite3.connect('total_spending.db')
    cur = con.cursor()
    main(con, cur)
    con.close()