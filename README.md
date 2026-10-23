Personal Expense & Finance Tracker

A personal finance application built with Python to record income and expenses, manage transactions, and track monthly finances through a graphical user interface.

Features

- Add income and expenses with categories
- View the current account balance
- View transaction history
- Filter transactions by category
- Generate monthly income and expense summaries
- Visualize income versus expenses using a bar chart
- Interactive graphical user interface built with Tkinter
- Store transaction records using an SQLite database

Technologies Used

- Python – Application logic
- Tkinter – Graphical user interface
- SQLite – Database management
- Matplotlib – Data visualization
- Git and GitHub – Version control and project hosting

Getting Started

Prerequisites

- Python 3 installed on your computer
- pip package manager

Installation

1. Clone this repository:
   
   git clone https://github.com/Sharonhoney05/personal-expense-finance-tracker.git

2. Navigate to the project directory:
   
   cd personal-expense-finance-tracker

3. Install the required dependency:
   
   py -m pip install -r requirements.txt

Run the Application

To launch the graphical application:

py gui.py

To run the terminal-based version instead:

py main.py

The SQLite database is initialized by the application when needed.

Project Structure

personal-expense-finance-tracker/
├── main.py
├── gui.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
└── screenshots/
    ├── main-window.png
    ├── transactions.png
    └── income-expenses-chart.png

The SQLite database file is generated locally and is excluded from version control.

Screenshots

Main Application Window

"Main Finance Tracker Window" (screenshots/main-window.png)

Transaction History

"Transaction History" (screenshots/transactions.png)

Income vs. Expenses Chart

"Income vs Expenses Chart" (screenshots/income-expenses-chart.png)

Learning Outcomes

- Python application development
- Database operations using SQLite
- Building graphical interfaces with Tkinter
- Data visualization using Matplotlib
- Version control and repository management using Git and GitHub

Future Improvements

- Export transactions to CSV
- Add date-range filtering
- Introduce budget tracking and spending limits
- Enhance financial charts and reports

Author

F K Sharon

GitHub: "Sharonhoney05" (https://github.com/Sharonhoney05)