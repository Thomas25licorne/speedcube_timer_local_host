import sys
from database import DatabaseManager

def main():
    # Check if the user provided exactly one argument (the ID)
    if len(sys.argv) != 2:
        print("Usage Error: You must provide the unique ID of the solve you want to delete.")
        print("Example Input: python3 delete_solve.py 42")
        return
    
    try:
        solve_id = int(sys.argv[1])
    except ValueError:
        print("Error: The exact ID must be a valid number.")
        print("Example Input: python3 delete_solve.py 42")
        return

    # Initialize the database manager and delete the ID
    db = DatabaseManager()
    db.delete_solve_by_id(solve_id)

if __name__ == "__main__":
    main()