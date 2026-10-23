import tkinter as tk
from tkinter import messagebox, ttk
from database import create_database, add_transaction, get_transactions, delete_transaction, update_transaction
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Create the main application window
root = tk.Tk()
root.title("Personal Expense & Finance Tracker")
root.geometry("1000x850")
root.configure(bg="#F3F6FB")
root.minsize(900, 650)

# Scrollable main area
main_canvas = tk.Canvas(root, bg="#F3F6FB", highlightthickness=0)
main_scrollbar = ttk.Scrollbar(root, orient="vertical", command=main_canvas.yview)

content_frame = tk.Frame(main_canvas, bg="#F3F6FB")

content_frame.bind(
    "<Configure>",
    lambda event: main_canvas.configure(
        scrollregion=main_canvas.bbox("all")
    )
)

canvas_window = main_canvas.create_window(
    (0, 0), window=content_frame, anchor="nw"
)

main_canvas.bind(
    "<Configure>",
    lambda event: main_canvas.itemconfigure(
        canvas_window, width=event.width
    )
)
main_canvas.configure(yscrollcommand=main_scrollbar.set)

main_scrollbar.pack(side="right", fill="y")
main_canvas.pack(side="left", fill="both", expand=True)
def scroll_with_mousewheel(event):
    main_canvas.yview_scroll(
        int(-1 * (event.delta / 120)), "units"
    )

main_canvas.bind_all("<MouseWheel>", scroll_with_mousewheel)

# Main heading
heading = tk.Label(
    content_frame,
    text="Personal Finance Tracker",
    font=("Arial", 24, "bold"),
    bg="#F3F6FB",
    fg="#243447"
)
heading.pack(pady=(20, 5))

subtitle = tk.Label(
    content_frame,
    text="Manage your money wisely!",
    font=("Arial", 12),
    bg="#F3F6FB",
    fg="#526579"
)
subtitle.pack(pady=(0, 20))

# Dashboard cards container
cards_frame = tk.Frame(content_frame, bg="#F4F6F9")
cards_frame.pack(fill="x", padx=20)


def create_card(parent, title, amount, color):
    card = tk.Frame(
        parent,
        bg="white",
        highlightbackground="#DCE2EA",
        highlightthickness=1,
        padx=18,
        pady=20
    )

    tk.Label(
        card,
        text=title,
        font=("Arial", 10),
        bg="white",
        fg="#526579"
    ).pack(pady=(0, 10))

    value_label = tk.Label(
        card,
        text=amount,
        font=("Arial", 18, "bold"),
        bg="white",
        fg=color
    )
    value_label.pack()

    return card, value_label


# Create database and read saved transactions
create_database()

income_card, income_value = create_card(
    cards_frame, "Total Income", "Rs. 0.00", "#16834A"
)
expense_card, expense_value = create_card(
    cards_frame, "Total Expenses", "Rs. 0.00", "#D64545"
)
balance_card, balance_value = create_card(
    cards_frame, "Remaining Balance", "Rs. 0.00", "#245BB5"
)

income_card.grid(row=0, column=0, padx=6, sticky="nsew")
expense_card.grid(row=0, column=1, padx=6, sticky="nsew")
balance_card.grid(row=0, column=2, padx=6, sticky="nsew")

for column in range(3):
    cards_frame.columnconfigure(column, weight=1)

# Monthly Income vs Expense Chart
chart_frame = tk.Frame(content_frame, bg="white")
chart_frame.pack(fill="x", padx=25, pady=(15, 10))

chart_heading = tk.Label(
    chart_frame,
    text="Monthly Income vs Expenses",
    font=("Arial", 14, "bold"),
    bg="white",
    fg="#243447"
)
chart_heading.pack(pady=(10, 0))

chart_figure = Figure(figsize=(7, 1.5), dpi=100)
chart_axes = chart_figure.add_subplot(111)

chart_canvas = FigureCanvasTkAgg(
    chart_figure,
    master=chart_frame
)
chart_canvas.get_tk_widget().pack(fill="both", expand=True)

# Update monthly income and expense chart
def refresh_monthly_chart():
    transactions = get_transactions()
    monthly_totals = {}

    for _, kind, amount, _, transaction_date, _ in transactions:
        month = str(transaction_date)[:7]

        if len(month) != 7 or month[4] != "-":
            continue

        if month not in monthly_totals:
            monthly_totals[month] = {
                "income": 0.0,
                "expense": 0.0
            }

        if kind.lower() in ("income", "expense"):
            monthly_totals[month][kind.lower()] += float(amount)

    chart_axes.clear()

    months = sorted(monthly_totals.keys())
    incomes = [
        monthly_totals[month]["income"] for month in months
    ]
    expenses = [
        monthly_totals[month]["expense"] for month in months
    ]

    if months:
        positions = list(range(len(months)))
        bar_width = 0.35

        chart_axes.bar(
            [p - bar_width / 2 for p in positions],
            incomes,
            bar_width,
            label="Income",
            color="#16834A"
        )
        chart_axes.bar(
            [p + bar_width / 2 for p in positions],
            expenses,
            bar_width,
            label="Expenses",
            color="#D64545"
        )

        chart_axes.set_xticks(positions)
        chart_axes.set_xticklabels(months, rotation=30, ha="right")
        chart_axes.legend()
        chart_axes.set_ylabel("Amount (Rs.)")
        chart_axes.grid(axis="y", alpha=0.2)
    else:
        chart_axes.text(
            0.5, 0.5,
            "Add transactions to see your monthly chart",
            ha="center",
            va="center",
            transform=chart_axes.transAxes
        )
        chart_axes.set_xticks([])
        chart_axes.set_yticks([])

    chart_figure.tight_layout()
    chart_canvas.draw()

# Refresh dashboard from the database
def refresh_dashboard():
    transactions = get_transactions()

    total_income = sum(
        amount for _, kind, amount, _, _, _ in transactions
        if kind == "income"
    )

    total_expenses = sum(
        amount for _, kind, amount, _, _, _ in transactions
        if kind == "expense"
    )

    balance = total_income - total_expenses

    income_value.config(text=f"Rs. {total_income:,.2f}")
    expense_value.config(text=f"Rs. {total_expenses:,.2f}")
    balance_value.config(text=f"Rs. {balance:,.2f}")

    refresh_transaction_history()
    refresh_monthly_chart()

# Input form
form = tk.Frame(content_frame, bg="white", padx=20, pady=15)
form.pack(fill="x", padx=25, pady=25)

tk.Label(
    form, text="Add a Transaction",
    font=("Arial", 15, "bold"),
    bg="white", fg="#243447"
).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

tk.Label(form, text="Amount (Rs.):", bg="white").grid(
    row=1, column=0, sticky="w", pady=6
)
amount_entry = tk.Entry(form, font=("Arial", 11), width=30)
amount_entry.grid(row=1, column=1, sticky="w", pady=6)

tk.Label(form, text="Description:", bg="white").grid(
    row=2, column=0, sticky="w", pady=6
)
description_entry = tk.Entry(form, font=("Arial", 11), width=30)
description_entry.grid(row=2, column=1, sticky="w", pady=6)
tk.Label(form, text="Category:", bg="white").grid(
    row=3, column=0, sticky="w", pady=6
)

category_entry = ttk.Combobox(
    form,
    values=(
        "Food",
        "Transport",
        "Shopping",
        "Bills",
        "Salary",
        "Education",
        "Entertainment",
        "Health",
        "Other"
    ),
    state="readonly",
    width=27
)
category_entry.set("Other")
category_entry.grid(row=3, column=1, sticky="w", pady=6)


# Save transaction and update dashboard
def save_transaction(transaction_type):
    try:
        amount = float(amount_entry.get())

        if amount <= 0:
            messagebox.showerror(
                "Invalid Amount",
                "Please enter an amount greater than zero."
            )
            return

    except ValueError:
        messagebox.showerror(
            "Invalid Amount",
            "Please enter a valid number."
        )
        return

    description = description_entry.get().strip()

    if not description:
        messagebox.showerror(
            "Missing Description",
            "Please enter a description."
        )
        return

    category = category_entry.get()

    add_transaction(transaction_type, amount, description, category)
    refresh_dashboard()

    amount_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    category_entry.set("Other")

    messagebox.showinfo(
        "Success",
        f"{transaction_type.title()} saved successfully!"
    )


# Action buttons
buttons_frame = tk.Frame(content_frame, bg="#F4F6F9")
buttons_frame.pack(pady=(0, 15))

tk.Button(
    buttons_frame,
    text="Add Income",
    command=lambda: save_transaction("income"),
    bg="#16834A",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=20,
    pady=8
).grid(row=0, column=0, padx=10)

tk.Button(
    buttons_frame,
    text="Add Expense",
    command=lambda: save_transaction("expense"),
    bg="#D64545",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=20,
    pady=8
).grid(row=0, column=1, padx=10)
# Search and filter controls
search_frame = tk.Frame(content_frame, bg="#F3F6FB")
search_frame.pack(fill="x", padx=25, pady=(0, 12))

tk.Label(
    search_frame,
    text="Search Description:",
    bg="#F3F6FB",
    fg="#243447",
    font=("Arial", 10, "bold")
).pack(side="left", padx=(0, 8))

search_entry = tk.Entry(search_frame, font=("Arial", 11), width=25)
search_entry.pack(side="left", padx=5)

tk.Label(
    search_frame,
    text="Type:",
    bg="#F3F6FB",
    fg="#243447",
    font=("Arial", 10, "bold")
).pack(side="left", padx=(12, 5))

filter_choice = ttk.Combobox(
    search_frame,
    values=("All Transactions", "Income", "Expense"),
    state="readonly",
    width=18
)
filter_choice.set("All Transactions")
filter_choice.pack(side="left", padx=5)
search_button = ttk.Button(
    search_frame,
    text="Search",
    command=lambda: apply_filters()
)
search_button.pack(side="left", padx=8)

reset_button = ttk.Button(
    search_frame,
    text="Reset",
    command=lambda: reset_filters()
)
reset_button.pack(side="left", padx=5)


# Display transactions saved in SQLite
# Transaction history section
history_heading = tk.Label(
    content_frame,
    text="Transaction History",
    font=("Arial", 15, "bold"),
    bg="#F3F6FB",
    fg="#243447"
)
history_heading.pack(pady=(5, 10))

# Create the transaction table
table_frame = tk.Frame(content_frame)
table_frame.pack(fill="both", expand=True, padx=25, pady=(0, 15))

columns = ("ID", "Type", "Amount", "Description", "Date", "Category")

transaction_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=8
)
# Style the transaction table
table_style = ttk.Style()
table_style.theme_use("clam")

table_style.configure(
    "Treeview",
    background="white",
    foreground="#243447",
    rowheight=32,
    fieldbackground="white",
    font=("Arial", 10)
)

table_style.configure(
    "Treeview.Heading",
    background="#243447",
    foreground="white",
    font=("Arial", 10, "bold"),
    padding=8
)

table_style.map(
    "Treeview",
    background=[("selected", "#245BB5")],
    foreground=[("selected", "white")]
)

transaction_table.heading("ID", text="ID")
transaction_table.heading("Type", text="Transaction Type")
transaction_table.heading("Amount", text="Amount (Rs.)")
transaction_table.heading("Description", text="Description")
transaction_table.heading("Date", text="Date & Time")
transaction_table.heading("Category", text="category")

transaction_table.column("ID", width=50, anchor="center")
transaction_table.column("Type", width=140, anchor="center")
transaction_table.column("Amount", width=150, anchor="e")
transaction_table.column("Description", width=300, anchor="w")
transaction_table.column("Date", width=170, anchor="center")
transaction_table.column("Category", width=130, anchor="center")

# Add a scrollbar
scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=transaction_table.yview
)
transaction_table.configure(yscrollcommand=scrollbar.set)

transaction_table.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


# Load saved transactions into the table
def refresh_transaction_history():
    for item in transaction_table.get_children():
        transaction_table.delete(item)

    transactions = get_transactions()

    for transaction in transactions:
        transaction_id, kind, amount, description, transaction_date, category = transaction

        transaction_table.insert(
            "",
            "end",
            values=(
                transaction_id,
                kind.title(),
                f"₹{float(amount):.2f}",
                description,
                transaction_date,
                category
            )
        )


def apply_filters():
    search_text = search_entry.get().strip().lower()
    selected_type = filter_choice.get()

    for item in transaction_table.get_children():
        transaction_table.delete(item)

    transactions = get_transactions()

    for transaction in transactions:
        transaction_id, kind, amount, description, transaction_date, category = transaction

        # Filter by transaction type
        if (
            selected_type != "All Transactions"
            and kind.lower() != selected_type.lower()
        ):
            continue

        # Search in description and category
        if (
            search_text
            and search_text not in description.lower()
            and search_text not in category.lower()
        ):
            continue

        transaction_table.insert(
            "",
            "end",
            values=(
                transaction_id,
                kind.title(),
                f"₹{float(amount):.2f}",
                description,
                transaction_date,
                category
            )
        )


def reset_filters():
    search_entry.delete(0, "end")
    filter_choice.set("All Transactions")
    refresh_transaction_history()

def delete_selected_transaction():
    selected_item = transaction_table.selection()

    if not selected_item:
        messagebox.showwarning(
            "No Selection",
            "Please select a transaction to delete."
        )
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this transaction?"
    )

    if confirm:
        transaction_id = transaction_table.item(
            selected_item[0], "values"
        )[0]

        delete_transaction(int(transaction_id))
        refresh_dashboard()

        messagebox.showinfo(
            "Deleted",
            "Transaction deleted successfully!"
        )

def edit_selected_transaction():
    selected_item = transaction_table.selection()

    if not selected_item:
        messagebox.showwarning(
            "No Selection",
            "Please select a transaction to edit."
        )
        return

    values = transaction_table.item(selected_item[0], "values")

    transaction_id = int(values[0])
    current_type = values[1].lower()
    current_amount = values[2].replace("₹", "").replace(",", "").strip()
    current_description = values[3]
    current_category = values[5]

    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Transaction")
    edit_window.geometry("420x450")
    edit_window.configure(bg="#F3F6FB")
    edit_window.resizable(False, False)

    tk.Label(
        edit_window,
        text="Edit Transaction",
        font=("Arial", 16, "bold"),
        bg="#F3F6FB",
        fg="#243447"
    ).pack(pady=15)

    tk.Label(edit_window, text="Type:", bg="#F3F6FB").pack()
    type_choice = ttk.Combobox(
        edit_window,
        values=("income", "expense"),
        state="readonly"
    )
    type_choice.set(current_type)
    type_choice.pack(pady=5)

    tk.Label(edit_window, text="Amount (Rs.):", bg="#F3F6FB").pack()
    amount_input = tk.Entry(edit_window)
    amount_input.insert(0, current_amount)
    amount_input.pack(pady=5)

    tk.Label(edit_window, text="Category:", bg="#F3F6FB").pack()

    edit_category = ttk.Combobox(
        edit_window,
        values=(
            "Food",
            "Transport",
            "Shopping",
            "Bills",
            "Salary",
            "Education",
            "Entertainment",
            "Health",
            "Other"
    ),
    state="readonly"
    )
    edit_category.set(current_category)
    edit_category.pack(pady=5)

    tk.Label(edit_window, text="Description:", bg="#F3F6FB").pack()
    description_input = tk.Entry(edit_window)
    description_input.insert(0, current_description)
    description_input.pack(pady=5)

    def save_changes():
        try:
            new_amount = float(amount_input.get())

            if new_amount <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Amount",
                "Enter an amount greater than zero.",
                parent=edit_window
            )
            return

        new_description = description_input.get().strip()

        if not new_description:
            messagebox.showerror(
                "Missing Description",
                "Please enter a description.",
                parent=edit_window
            )
            return

        update_transaction(
            transaction_id,
            type_choice.get(),
            new_amount,
            new_description,
            edit_category.get()
        )

        refresh_dashboard()
        edit_window.destroy()

        messagebox.showinfo(
            "Updated",
            "Transaction updated successfully!"
        )

    ttk.Button(
        edit_window,
        text="Save Changes",
        command=save_changes
    ).pack(pady=15)

# Frame for transaction action buttons
action_frame = tk.Frame(content_frame, bg="#F3F6FB")
action_frame.pack(fill="x", pady=10)

delete_button = ttk.Button(
    action_frame,
    text="Delete Selected Transaction",
    command=delete_selected_transaction
)
delete_button.pack(side="left", padx=10, expand=True)

edit_button = ttk.Button(
    action_frame,
    text="Edit Selected Transaction",
    command=edit_selected_transaction
)
edit_button.pack(side="left", padx=10, expand=True)
# Load actual totals when the app opens
refresh_dashboard()

root.mainloop()