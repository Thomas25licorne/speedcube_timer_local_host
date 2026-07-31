import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name="solves.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            
            # 1. Create the NEW master sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_name TEXT PRIMARY KEY,
                    puzzle_type TEXT NOT NULL
                )
            """)
            
            # 2. Populate default sessions if the table is completely empty
            cursor.execute("SELECT COUNT(*) FROM sessions")
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO sessions (session_name, puzzle_type) VALUES ('3x3', '3x3')")
                cursor.execute("INSERT INTO sessions (session_name, puzzle_type) VALUES ('4x4', '4x4')")
            
            # 3. Existing solves table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS solves (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_name TEXT NOT NULL,
                    scramble TEXT NOT NULL,
                    solve_time REAL NOT NULL,
                    date TEXT NOT NULL
                )
            """)
                
            conn.commit()

    # --- NEW: Methods to handle the sessions table ---
    def add_session(self, session_name, puzzle_type):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO sessions (session_name, puzzle_type)
                VALUES (?, ?)
            """, (session_name, puzzle_type))
            conn.commit()

    def get_all_sessions(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT session_name, puzzle_type FROM sessions ORDER BY session_name")
            return cursor.fetchall()

    # --- Existing Solve Methods ---
    def save_solve(self, session_name, scramble, solve_time):
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO solves (session_name, scramble, solve_time, date)
                VALUES (?, ?, ?, ?)
            """, (session_name, scramble, solve_time, date_str))
            conn.commit()

    def get_all_solves(self, session_name):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, solve_time, scramble, date 
                FROM solves 
                WHERE session_name = ? 
                ORDER BY id ASC
            """, (session_name,))
            return cursor.fetchall()
        
    def delete_solve_by_id(self, solve_id):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM solves WHERE id = ?", (solve_id,))
            conn.commit()
            print(f"Solve ID {solve_id} has been permanently deleted.")