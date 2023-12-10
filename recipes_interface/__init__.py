import sqlite3

class RecipesWindow:
    def __init__(self):
      self.require_password = True
      self.use_externalAPI = True

def load_test_database():
  # Connect to an existing database or create a new one
  conn = sqlite3.connect('db/recipes.db')
  # Create table if not exist
  cursor = conn.cursor()
  cursor.execute('''
  DROP TABLE IF EXISTS recipes
''')
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        favourite INTEGER NOT NULL
    )
''')
  # Commit the changes
  conn.commit()

  # Create dummy entries
  cursor.execute("INSERT INTO recipes (name, description, favourite) VALUES (?, ?, ?)", ('Pizza', 'Example of a pizza recipe', 0))
  cursor.execute("INSERT INTO recipes (name, description, favourite) VALUES (?, ?, ?)", ('Macarroni', 'Example of macarroni recipe', 0))

  # Commit the changes
  conn.commit()



def get_recipes():
  # Connect to an existing database or create a new one
  try:
    conn = sqlite3.connect('db/recipes.db')
  except Exception:
    print("Error connecting to database")
    return -1
  # Create table if not exist
  cursor = conn.cursor()
  # Query data from the table
  cursor.execute("SELECT * FROM recipes")
  rows = cursor.fetchall()

  return rows

def get_favourite_recipes():
  # Connect to an existing database or create a new one
  try:
    conn = sqlite3.connect('db/recipes.db')
  except Exception:
    print("Error connecting to database")
    return -1
  # Create table if not exist
  cursor = conn.cursor()
  # Query data from the table
  cursor.execute("SELECT * FROM recipes WHERE favourite = 1")
  rows = cursor.fetchall()

  return rows

def add_favourites(name):
  # Connect to an existing database or create a new one
  try:
    conn = sqlite3.connect('db/recipes.db')
  except Exception:
    print("Error connecting to database")
    return -1
  # Create table if not exist
  cursor = conn.cursor()
  # Query data from the table

  cursor.execute("UPDATE recipes SET favourite = ? WHERE name = ?", (1, name))
  # Commit the changes
  conn.commit()

  # Close the cursor and connection
  cursor.close()
  conn.close()