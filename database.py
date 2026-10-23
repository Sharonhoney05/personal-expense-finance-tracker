import sqlite3
from datetime import datetime
import csv


def create_database():
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_type TEXT NOT NULL,
            amount REAL NOT NULL CHECK(amount > 0),
            description TEXT,
            transaction_date TEXT,
            category TEXT DEFAULT 'Other'
        )
    """)

    # Add the date column to an existing database if needed
    cursor.execute("PRAGMA table_info(transactions)")
    columns = [column[1] for column in cursor.fetchall()]

    if "category" not in columns:
        cursor.execute(
            "ALTER TABLE transactions ADD COLUMN category TEXT DEFAULT 'Other'"
        )

    if "transaction_date" not in columns:
        cursor.execute(
            "ALTER TABLE transactions ADD COLUMN transaction_date TEXT"
        )

    # Fill dates for older transactions that don't have one
    cursor.execute("""
        UPDATE transactions
        SET transaction_date = ?
        WHERE transaction_date IS NULL
    """, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))

    connection.commit()
    connection.close()


def add_transaction(transaction_type, amount, description="", category="Other"):
    transaction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    connection = sqlite3.connect("finance.db")

    try:
        connection.execute("""
            INSERT INTO transactions
            (transaction_type, amount, description, transaction_date, category)
            VALUES (?, ?, ?, ?, ?)
        """, (
            transaction_type,
            amount,
            description,
            transaction_date,
            category
        ))

        connection.commit()

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_transactions():
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, transaction_type, amount, description,
               transaction_date, category
        FROM transactions
        ORDER BY id
    """)

    transactions = cursor.fetchall()
    connection.close()

    return transactions

def delete_transaction(transaction_id):
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM transactions WHERE id = ?",
        (transaction_id,)
    )

    connection.commit()
    connection.close()

def update_transaction(transaction_id, transaction_type, amount, description, category="Other"):
    connection = sqlite3.connect("finance.db")
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE transactions
        SET transaction_type = ?, amount = ?, description = ?, category = ?
        WHERE id = ?
    """, (transaction_type, amount, description, category, transaction_id))

    connection.commit()
    connection.close()
    
def export_transactions_to_csv(filename):
    transactions = get_transactions()

    with open(filename, "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)

        writer.writerow([
            "ID",
            "Type",
            "Amount",
            "Description",
            "Date",
            "Category"
        ])

        writer.writerows(transactions)

if __name__ == "__main__":
    create_database()
    print("Database is ready!")