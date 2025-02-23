import sqlite3

DB_FILE = 'database.db'

def create_table():
    """Create a table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            year TEXT NOT NULL,
            section TEXT NOT NULL,
            dept TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_user(code, name, year, section, dept, role):
    """Insert a new user into the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (code, name, year, section, dept, role) VALUES (?, ?, ?, ?, ?, ?)',
                       (code, name, year, section, dept, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:  # Handles duplicate card codes
        return False
    finally:
        conn.close()

def get_user_by_code(code):
    """Check if a user with the given RFID code exists."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE code = ?', (code,))
    user = cursor.fetchone()
    conn.close()
    return user

# Run table creation at import
create_table()