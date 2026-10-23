from database import create_database, add_transaction, get_transactions
import matplotlib.pyplot as plt


def get_valid_amount(message):
    while True:
        try:
            amount = float(input(message))

            if amount <= 0:
                print("Amount must be greater than zero.")
            else:
                return amount

        except ValueError:
            print("Please enter a valid number.")


def view_balance():
    transactions = get_transactions()

    total_income = sum(
        t[2] for t in transactions
        if t[1] == "income"
    )

    total_expenses = sum(
        t[2] for t in transactions
        if t[1] == "expense"
    )

    print("\n--- Balance Summary ---")
    print(f"Total Income: Rs. {total_income:.2f}")
    print(f"Total Expenses: Rs. {total_expenses:.2f}")
    print(f"Remaining Balance: Rs. {total_income - total_expenses:.2f}")

def monthly_summary():
    transactions = get_transactions()
    month = input("Enter month (YYYY-MM): ")

    monthly = [
        t for t in transactions
        if t[4] and t[4][:7] == month
    ]

    income = sum(t[2] for t in monthly if t[1] == "income")
    expenses = sum(t[2] for t in monthly if t[1] == "expense")

    print(f"\n--- Monthly Summary: {month} ---")
    print(f"Income: Rs. {income:.2f}")
    print(f"Expenses: Rs. {expenses:.2f}")
    print(f"Balance: Rs. {income - expenses:.2f}")

def show_chart():
    transactions = get_transactions()

    income = sum(t[2] for t in transactions if t[1] == "income")
    expenses = sum(t[2] for t in transactions if t[1] == "expense")

    plt.bar(["Income", "Expenses"], [income, expenses])
    plt.title("Income vs Expenses")
    plt.ylabel("Amount (Rs.)")
    plt.tight_layout()
    plt.show()


def main():
    create_database()

    print("Welcome to Personal Expense & Finance Tracker!")
    user_name = input("What is your name? ")
    print(f"Hello, {user_name}! Let's manage your money wisely.")

    while True:
        print("\n--- Personal Finance Tracker ---")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Balance")
        print("4. View Transaction History")
        print("5. Filter by Category")
        print("6. Monthly Summary")
        print("7. Income vs Expense Chart")
        print("8. Exit")

        choice = input("Choose an option (1-8): ")

        if choice == "1":
            amount = get_valid_amount("Enter income amount (Rs.): ")
            description = input("Enter income description: ")

            print("Categories: Salary, Allowance, Freelance, Business, Other")
            category = input("Enter category: ").title()

            add_transaction("income", amount, description, category)
            print("Income saved successfully!")

        elif choice == "2":
            amount = get_valid_amount("Enter expense amount (Rs.): ")
            description = input("Enter expense description: ")

            print("Categories: Food, Travel, Shopping, Bills, Other")
            category = input("Enter category: ").title()

            add_transaction("expense", amount, description, category)
            print("Expense saved successfully!")

        elif choice == "3":
            view_balance()

        elif choice == "4":
            transactions = get_transactions()

            print("\n--- Transaction History ---")

            if not transactions:
                print("No transactions recorded yet.")
            else:
                for transaction in transactions:
                    transaction_id, kind, amount, description, date, category = transaction
                    print(
                        f"ID: {transaction_id} | "
                        f"{kind.title()} | Rs. {amount:.2f} | "
                        f"{description} | Category: {category} |Date: {date}"
                    )
        
        elif choice == "5":
            transactions = get_transactions()
            category = input("Enter category to filter: ").title()

            filtered = [
                t for t in transactions
                if t[5].title() == category
            ]

            print(f"\n--- {category} Transactions ---")

            if not filtered:
                print("No transactions found in this category.")
            else:
                for t in filtered:
                    print(
                        f"{t[1].title()} | Rs. {t[2]:.2f} | "
                        f"{t[3]} | Category: {t[5]}"
                    )

        elif choice == "6":
            monthly_summary()

        elif choice == "7":
            show_chart()

        elif choice == "8":
            print("Thank you for using Personal Finance Tracker!")
            break

        else:
            print("Invalid option. Please choose between 1 and 8.")


if __name__ == "__main__":
    main()