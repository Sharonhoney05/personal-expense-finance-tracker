Personal Expense & Finance Tracker

A personal finance application built with Python to record income and expenses, manage transactions, and track monthly finances through a graphical interface.

Features

- Add income and expenses with categories
- View current balance
- View transaction history
- Filter transactions by category
- Generate monthly income and expense summaries
- Visualize income versus expenses using a chart
- Graphical user interface built with Tkinter
- Store transaction records using SQLite

Technologies Used

- Python
- Tkinter
- SQLite
- Matplotlib
- Git and GitHub

How to Run

1. Install Python 3.

2. Install the required dependency:
   
   py -m pip install -r requirements.txt

3. Run the graphical application:
   
   py gui.py
   
   Alternatively, run the terminal-based version:
   
   py main.py

Project Structure

Personal Finance Tracker/
├── main.py
├── gui.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
└── finance.db  # Generated automatically when the database is initialized

Learning Outcomes

- Python programming and application development
- Database operations using SQLite
- Building graphical interfaces with Tkinter
- Data visualization using Matplotlib
- Version control using Git and GitHub

Future Improvements

- Export transactions to CSV
- Add date-range filters and budget tracking
- Improve charts and financial reports