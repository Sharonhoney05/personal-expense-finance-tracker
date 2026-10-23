Personal Expense & Finance Tracker

A desktop application built with Python to manage personal income and expenses, track balances, visualize monthly financial activity, and export transactions to CSV.

Features

- Dashboard: View total income, total expenses, and current balance.
- Transaction Management: Add, edit, and delete income and expense transactions.
- Transaction History: View recorded transactions with details such as type, amount, description, date, and category.
- Search and Filter: Search transactions and filter them by category or transaction type.
- Monthly Financial Chart: Visualize income versus expenses using a chart powered by Matplotlib.
- CSV Export: Export transaction records to a CSV file for use in spreadsheet applications such as Microsoft Excel.
- SQLite Database: Store transaction data locally.
- Input Validation: Reject invalid transaction amounts, including zero and negative values.
- Automated Testing: Test database operations using pytest.
- Continuous Integration: Automatically run tests through GitHub Actions when changes are pushed or pull requests are opened.

Technologies Used

- Python
- Tkinter — graphical user interface
- SQLite — local database
- Matplotlib — financial chart visualization
- CSV — transaction data export
- pytest — automated testing
- Git and GitHub — version control and project hosting
- GitHub Actions — continuous integration

Project Structure

Personal Finance Tracker/
├── gui.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
├── tests/
│   └── test_database.py
├── screenshots/
│   ├── main-window.png
│   ├── transactions.png
│   └── income-expenses-chart.png
└── .github/
    └── workflows/
        └── python-tests.yml

Installation and Setup

1. Clone the repository

git clone https://github.com/Sharonhoney05/personal-expense-finance-tracker.git

2. Navigate to the project folder

cd personal-expense-finance-tracker

3. Install dependencies

Make sure Python is installed, then run:

py -m pip install -r requirements.txt

4. Run the application

py gui.py

The application uses SQLite to store transactions locally.

Running Automated Tests

Install pytest if it is not already installed:

py -m pip install pytest

Run the tests:

py -m pytest -v

The test suite covers database creation, adding and retrieving transactions, updating and deleting transactions, and rejecting non-positive transaction amounts.

Screenshots

Main Dashboard

"Main Dashboard" (screenshots/main-window.png)

Transaction History

"Transaction History" (screenshots/transactions.png)

Monthly Income vs Expenses

"Income and Expenses Chart" (screenshots/income-expenses-chart.png)

What I Learned

- Building a desktop GUI with Python and Tkinter.
- Connecting a Python application to an SQLite database.
- Implementing CRUD operations: Create, Read, Update, and Delete.
- Validating user input and handling errors.
- Searching, filtering, and categorizing transaction data.
- Visualizing financial information with Matplotlib.
- Exporting structured data to CSV.
- Writing automated database tests with pytest.
- Using Git and GitHub for version control.
- Configuring GitHub Actions for continuous integration.

Future Improvements

- Add date-range filtering and more detailed financial reports.
- Add monthly budgets and savings goals.
- Improve the dashboard with additional financial visualizations.
- Add optional transaction import from CSV.

Author

F K Sharon

GitHub: "Sharonhoney05" (https://github.com/Sharonhoney05)

---

This project was developed as a hands-on learning project to strengthen Python programming, database management, testing, and software development skills.