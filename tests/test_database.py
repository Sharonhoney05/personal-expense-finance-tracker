import sqlite3

import pytest

import database


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    """Use a separate temporary database for each test."""
    db_path = tmp_path / "test_finance.db"

    real_connect = sqlite3.connect

    def connect_to_test_db(*args, **kwargs):
        return real_connect(str(db_path))

    monkeypatch.setattr(database.sqlite3, "connect", connect_to_test_db)
    database.create_database()

    return db_path


def test_create_database(test_db):
    """The transactions table should be created."""
    with sqlite3.connect(test_db) as connection:
        result = connection.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type = 'table' AND name = 'transactions'"
        ).fetchone()

    assert result is not None


def test_add_and_get_transaction(test_db):
    """A saved transaction should be returned with its details."""
    database.add_transaction(
        "Income", 21000, "Salary", "Work"
    )

    transactions = database.get_transactions()

    assert len(transactions) == 1
    assert transactions[0][1] == "Income"
    assert transactions[0][2] == 21000
    assert transactions[0][3] == "Salary"
    assert transactions[0][5] == "Work"


def test_delete_transaction(test_db):
    """Deleting a transaction should remove it."""
    database.add_transaction("Expense", 250, "Groceries", "Food")
    transaction_id = database.get_transactions()[0][0]

    database.delete_transaction(transaction_id)

    assert database.get_transactions() == []


def test_update_transaction(test_db):
    """Updating a transaction should save its new details."""
    database.add_transaction("Expense", 250, "Groceries", "Food")
    transaction_id = database.get_transactions()[0][0]

    database.update_transaction(
        transaction_id, "Expense", 300, "Shopping", "Personal"
    )

    transaction = database.get_transactions()[0]

    assert transaction[2] == 300
    assert transaction[3] == "Shopping"
    assert transaction[5] == "Personal"


def test_reject_non_positive_amount(test_db):
    """The database should reject zero and negative amounts."""
    with pytest.raises(sqlite3.IntegrityError):
        database.add_transaction("Expense", 0, "Invalid", "Other")

    with pytest.raises(sqlite3.IntegrityError):
        database.add_transaction("Expense", -10, "Invalid", "Other")

    assert database.get_transactions() == []