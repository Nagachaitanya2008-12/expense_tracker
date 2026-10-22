from tabulate import tabulate

def category_summary(connection):
    cursor = connection.cursor()
    query = """
        SELECT category, SUM(amount) as total_spent 
        FROM expenses 
        GROUP BY category 
        ORDER BY total_spent DESC
    """
    cursor.execute(query)
    summary = cursor.fetchall()
    
    if not summary:
        print("No expenses to analyze.")
    else:
        print("\n--- Expenses by Category ---")
        print(tabulate(summary, headers=["Category", "Total Spent"], tablefmt="grid"))
    cursor.close()

def budget_vs_expenses(connection):
    cursor = connection.cursor()
    query = """
        SELECT b.category, b.amount as budget_amount, COALESCE(SUM(e.amount), 0) as total_spent, 
               (b.amount - COALESCE(SUM(e.amount), 0)) as remaining
        FROM budgets b
        LEFT JOIN expenses e ON b.category = e.category
        GROUP BY b.category, b.amount
    """
    cursor.execute(query)
    data = cursor.fetchall()
    
    if not data:
        print("No budget data available to compare.")
    else:
        print("\n--- Budget vs Expenses ---")
        print(tabulate(data, headers=["Category", "Budget", "Spent", "Remaining"], tablefmt="grid"))
    cursor.close()