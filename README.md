# Spending Database

Welcome to my customer spending database! I designed a database in sqlite3 to track spending. The user logs their purchases by following a set of prompts on the command line, and can view their transaction history by selecting that option on the main menu.

To use the software, first run the program `initialize_database.py` to initialize the database. The three tables will be created and filled with dummy values, which can be removed later. Then, DO NOT run this program again. Instead, run the file `main.py` to query, insert, and edit your database.

I'm working on a way to track my spending that allows me to make a budget and hold myself accountable for it. In the past, I've tried different websites and excel spreadsheets to organize this, but I didn't like how they were formatted and I wanted something more customizable. In the future, I want to create a web application using this database with functionality to visualize spending patterns using software like altair or seaborn, and to design a budget that I can compare to the transaction history and suggest areas of improvement.

[Software Demo (link currently inactive)](http://youtube.link.goes.here)

# Relational Database

I am using a SQLite database and interacting with it in Python. The main user-facing table is the TransactionHistory table, which lists the users transactions, the date they were completed, and the amount spent on the transaction. The Transactions table stores all the types of transactions that can be made; the location they come from, the category of purchase they are (rent, gas, food, etc.), and whether or not that purchase was a necessity. It is connected to the TransactionHistory table via the TransactionID. Likewise, the Subscriptions table connects to the Transactions table via the SubscriptionID, and gives information of whether the purchase is a subscription, and how often it is performed if it is.

# Development Environment

I wrote this program in Python 3.10. I used the sqlite3 and pandas libraries in my development. T install them, type `pip install pandas` and `pip install sqlite3` into your command line.

# Useful Websites

{Make a list of websites that you found helpful in this project}

- [SQLite3 Official Documentation](https://docs.python.org/3.8/library/sqlite3.html)
- [W3Schools SQL Tutorials](https://www.w3schools.com/sql/default.asp)

# Future Work

- Add functionality for editing the database
- Add functionality to add to the Transactions table
- Add different query types user can create (Option to display Subscription status, Transaction Category, etc.)