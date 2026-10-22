from decimal import Decimal, InvalidOperation
from datetime import datetime
from tabulate import tabulate


def add_expense(connection):
    print("\n--- Add New Expense ---")

    expense_name = input("Enter expense name: ").strip()
    category = input("Enter category: ").strip()

    if not expense_name or not category:
        print("Name and category cannot be empty.")
        return

    try:
        amount = Decimal(input("Enter amount: ").strip())

        if not amount.is_finite() or amount <= 0:
            print("Amount must be a positive number.")
            return

        amount = amount.quantize(Decimal("0.01"))

    except InvalidOperation:
        print("Please enter a valid amount, such as 45.50.")
        return

    date_text = input("Enter date (YYYY-MM-DD): ").strip()

    try:
        expense_date = datetime.strptime(
            date_text, "%Y-%m-%d"
        ).date()
    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        return

    cursor = connection.cursor()

    query = """
        INSERT INTO expenses
        (expense_name, category, amount, expense_date)
        VALUES (%s, %s, %s, %s)
    """

    values = (
        expense_name,
        category,
        amount,
        expense_date
    )

    try:
        cursor.execute(query, values)
        connection.commit()
        print("Expense added successfully!")

    except Exception as error:
        connection.rollback()
        print("Could not save expense:", error)

    finally:
        cursor.close()

def view_expenses(connection):
    print("\n--- View Expenses ---")
    cursor = connection.cursor()

    query = "SELECT * from expenses"
    cursor.execute(query)

    expenses = cursor.fetchall()

    if not expenses:
        print("No expenses found.")
    else:
         headers = [
            "ID",
            "Expense Name",
            "Category",
            "Amount",
            "Date"
        ]

    print("\n--- All Expenses ---")
    print(tabulate(expenses,headers=headers,tablefmt="grid"))
    cursor.close()
def search_expenses(connection):
    print("\n--- Search Expenses ---")
    cursor = connection.cursor()

    search_term = input("Enter search term (name or category): ").strip()

    query = """
        SELECT * FROM expenses
        WHERE expense_name LIKE %s OR category LIKE %s
    """

    values = (f"%{search_term}%", f"%{search_term}%")
    cursor.execute(query, values)

    expenses = cursor.fetchall()

    if not expenses:
        print("No matching expenses found.")
    else:
        headers = [
            "ID",
            "Expense Name",
            "Category",
            "Amount",
            "Date"
        ]
        print("\n--- Search Results ---")
        print(tabulate(expenses, headers=headers, tablefmt="grid"))

    cursor.close()
def update_expense(connection):
    cursor = connection.cursor()

    try:
        expense_id = int(input("Enter the Expense ID to update: "))
        cursor.execute(
            "SELECT * FROM expenses WHERE expense_id = %s",
            (expense_id,)
        )
        expense = cursor.fetchone()

        if expense is None:
            print("Expense not found!")
            return

        print("\nCurrent expense details:")
        print(expense)

        print("\nWhat would you like to update?")
        print("1. Expense Name")
        print("2. Category")
        print("3. Amount")
        print("4. Date")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            value = input("Enter new expense name: ").strip()
            if not value:
                print("Expense name cannot be empty.")
                return
            column = "expense_name"

        elif choice == "2":
            value = input("Enter new category: ").strip()
            if not value:
                print("Category cannot be empty.")
                return
            column = "category"

        elif choice == "3":
            from decimal import Decimal, InvalidOperation

            try:
                value = Decimal(input("Enter new amount: ").strip())
                if not value.is_finite() or value <= 0:
                    print("Amount must be greater than zero.")
                    return
                value = value.quantize(Decimal("0.01"))
            except InvalidOperation:
                print("Please enter a valid amount.")
                return

            column = "amount"

        elif choice == "4":
            from datetime import datetime

            date_text = input("Enter new date (YYYY-MM-DD): ").strip()

            try:
                value = datetime.strptime(
                    date_text, "%Y-%m-%d"
                ).date()
            except ValueError:
                print("Invalid date. Use YYYY-MM-DD.")
                return

            column = "expense_date"

        else:
            print("Invalid choice.")
            return

        query = f"UPDATE expenses SET {column} = %s WHERE expense_id = %s"
        cursor.execute(query, (value, expense_id))
        connection.commit()

        print("Expense updated successfully!")

    except ValueError:
        print("Please enter a valid numeric Expense ID.")

    except Exception as error:
        connection.rollback()
        print("Could not update expense:", error)

    finally:
        cursor.close()
def delete_expense(connection):
    cursor = connection.cursor()

    try:
        expense_id = int(input("Enter the Expense ID to delete: "))
        cursor.execute(
            "SELECT * FROM expenses WHERE expense_id = %s",
            (expense_id,)
        )
        expense = cursor.fetchone()

        if expense is None:
            print("Expense not found!")
            return

        confirm = input(
            f"Are you sure you want to delete expense ID {expense_id}? (y/n): "
        ).strip().lower()

        if confirm == "y":
            cursor.execute(
                "DELETE FROM expenses WHERE expense_id = %s",
                (expense_id,)
            )
            connection.commit()
            print("Expense deleted successfully!")
        else:
            print("Deletion cancelled.")

    except ValueError:
        print("Please enter a valid numeric Expense ID.")

    except Exception as error:
        connection.rollback()
        print("Could not delete expense:", error)

    finally:
        cursor.close()