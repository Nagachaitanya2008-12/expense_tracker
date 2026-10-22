import mysql.connector
import expenses
import budget
import analysis

def main():
    # Remember to put your real MySQL password below
    db_config = {
        "host": "localhost",
        "user": "root",
        "password": "pothireddy2008", 
        "database": "expense_tracker"
    }

    try:
        connection = mysql.connector.connect(**db_config)
        
        while True:
            print("\n=== Expense Tracker Menu ===")
            print("1. Add Expense")
            print("2. View Expenses")
            print("3. Search Expenses")
            print("4. Update Expense")
            print("5. Delete Expense")
            print("6. Set/Update Budget")
            print("7. View Budgets")
            print("8. Category Summary")
            print("9. Budget vs Expenses")
            print("0. Exit")
            
            choice = input("Select an option (0-9): ").strip()
            
            if choice == "1":
                expenses.add_expense(connection)
            elif choice == "2":
                expenses.view_expenses(connection)
            elif choice == "3":
                expenses.search_expenses(connection)
            elif choice == "4":
                expenses.update_expense(connection)
            elif choice == "5":
                expenses.delete_expense(connection)
            elif choice == "6":
                budget.set_budget(connection)
            elif choice == "7":
                budget.view_budgets(connection)
            elif choice == "8":
                analysis.category_summary(connection)
            elif choice == "9":
                analysis.budget_vs_expenses(connection)
            elif choice == "0":
                print("Exiting Expense Tracker. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
                
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    main()