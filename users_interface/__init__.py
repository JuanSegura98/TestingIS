import sqlite3

class UserInterface:
    def __init__(self):
      self.require_password = True
      self.use_externalAPI = True

def load_users_test_database():
  # Connect to an existing database or create a new one
  conn = sqlite3.connect('db/users.db')
  # Create table if not exist
  cursor = conn.cursor()
  cursor.execute('''
  DROP TABLE IF EXISTS users
''')
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')
  # Commit the changes
  conn.commit()

  # Create dummy entries
  cursor.execute("INSERT INTO users (name, password) VALUES (?, ?)", ('Juan', 'Segura Nuñez'))
  cursor.execute("INSERT INTO users (name, password) VALUES (?, ?)", ('Rafa', 'Andreu Rosello'))
  cursor.execute("INSERT INTO users (name, password) VALUES (?, ?)", ('Fernando', 'Perez Sancho'))

  # Commit the changes
  conn.commit()



def get_user():
  # Connect to an existing database or create a new one
  try:
    conn = sqlite3.connect('db/users.db')
  except Exception:
    print("Error connecting to database")
    return -1
  # Create table if not exist
  cursor = conn.cursor()
  # Query data from the table
  cursor.execute("SELECT name FROM users")
  rows = cursor.fetchall()

  return rows



def add_user(name, password):
  # Connect to an existing database or create a new one
  try:
    conn = sqlite3.connect('db/users.db')
  except Exception:
    print("Error connecting to database")
    return -1
  # Create table if not exist
  cursor = conn.cursor()
  # Add entry to the table
  cursor.execute("SELECT name FROM users WHERE name = ?", (name,))
  rows = cursor.fetchall()
  if len(rows) == 0:
    if 4 < len(name) < 21:
      if 7 < len(password) < 26:
        cursor.execute("INSERT INTO users (name, password) VALUES (?, ?)", (name, password))
      else:
        print("Invalid password")
    else: 
      print("Invalid name") 
  else:
    print("Name already in use")
  # Commit the changes
  conn.commit()


def remove_user(name, password):
  # Connect to an existing database or create a new one
  try:
    conn = sqlite3.connect('db/users.db')
  except Exception:
    print("Error connecting to database")
    return -1
  # Create table if not exist
  cursor = conn.cursor()
  # Remove entry to the table
  cursor.execute("SELECT name FROM users WHERE name = ?", (name,))
  rows = cursor.fetchall()
  if len(rows) == 1:
    cursor.execute("DELETE FROM users WHERE name = ?", (name,))
  else:
    print("User not found")
  # Commit the changes
  conn.commit()

  # Close the cursor and connection
  cursor.close()
  conn.close()