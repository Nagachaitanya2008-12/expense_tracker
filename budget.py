from decimal import Decimal, InvalidOperation
from tabulate import tabulate

def set_budget(connection):
    print("\n--- Set Category Budget ---")
    category = input("Enter category: ").strip()
    
    if not category:
        print("Category cannot be empty.")
        return
        
    try:
        amount = Decimal(input("Enter budget amount: ").strip())
        if not amount.is_finite() or amount <= 0:
            print("Amount must be a positive number.")
            return
        amount = amount.quantize(Decimal("0.01"))
    except InvalidOperation:
        print("Please enter a valid amount.")
        return

    cursor = connection.cursor()
    
    cursor.execute("SELECT budget_id FROM budgets WHERE category = %s", (category,))
    existing = cursor.fetchone()
    
    try:
        if existing:
            cursor.execute("UPDATE budgets SET amount = %s WHERE category = %s", (amount, category))
            print(f"Budget updated for {category}!")
        else:
            cursor.execute("INSERT INTO budgets (category, amount) VALUES (%s, %s)", (category, amount))
            print(f"Budget set for {category}!")
        connection.commit()
    except Exception as error:
        connection.rollback()
        print("Could not save budget:", error)
    finally:
        cursor.close()

def view_budgets(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT category, amount FROM budgets")
    budgets = cursor.fetchall()
    
    if not budgets:
        print("No budgets found.")
    else:
        print("\n--- All Budgets ---")
        print(tabulate(budgets, headers=["Category", "Budget Amount"], tablefmt="grid"))
    cursor.close()