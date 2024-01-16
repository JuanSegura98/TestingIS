import sqlite3
from datetime import datetime

class InventoryInterface:
    def __init__(self):
      self.require_password = True
      self.use_externalAPI = True

def load_inventory_test_database():
  # Connect to an existing database or create a new one
  conn = sqlite3.connect('db/inventory.db')
  # Create table if not exist
  cursor = conn.cursor()
  cursor.execute('''
  DROP TABLE IF EXISTS inventory
''')
  cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        quantity INTEGER,
        added TEXT NOT NULL,
        modified TEXT NOT NULL,
        tags TEXT
    )
''')
  # Commit the changes
  conn.commit()

  # Create dummy entries
  fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  cursor.execute("INSERT INTO inventory (name, quantity, added, modified, tags) VALUES (?, ?, ?, ?, ?)", ('Manzana', 3,'2022-03-19 19:37:42','2023-12-28 13:08:20',['Fruta']))
  cursor.execute("INSERT INTO inventory (name, quantity, added, modified, tags) VALUES (?, ?, ?, ?, ?)", ('Pollo', 1,'2020-09-30 14:04:10','2023-12-28 13:08:20',[]))
  cursor.execute("INSERT INTO inventory (name, quantity, added, modified, tags) VALUES (?, ?, ?, ?, ?)", ('Queso', 2,'2020-09-30 14:04:10','2023-11-16 10:17:58',['Lacteo']))
  cursor.execute("INSERT INTO inventory (name, quantity, added, modified, tags) VALUES (?, ?, ?, ?, ?)", ('Huevo', 6,'2020-09-30 14:04:10','2024-01-08 12:31:59',[]))
  cursor.execute("INSERT INTO inventory (name, quantity, added, modified, tags) VALUES (?, ?, ?, ?, ?)", ('Tomate', 4,'2023-12-28 13:08:20','2024-01-08 12:31:59',['Verdura']))
  cursor.execute("INSERT INTO inventory (name, quantity, added, modified, tags) VALUES (?, ?, ?, ?, ?)", ('Leche', 2,fecha_actual,fecha_actual,['Lacteo', 'Bebida']))

  # Commit the changes
  conn.commit()

def get_inventory():
    # Connect to an existing database or create a new one
    try:
        conn = sqlite3.connect('db/inventory.db')
    except Exception:
        print("Error connecting to database")
        return -1
    # Create table if not exist
    cursor = conn.cursor()
    
    # Query data from the table
    cursor.execute("SELECT * FROM inventory")
    rows = cursor.fetchall()

    return rows

def edit_inventory(name, new_name, new_quantity, new_tags, delete_tags=None):
    # Connect to an existing database or create a new one
    try:
        conn = sqlite3.connect('db/inventory.db')
    except Exception:
        print("Error connecting to database")
        return -1
    # Create table if not exist
    cursor = conn.cursor()

    if delete_tags is None:
        delete_tags = []

    # Get the existing tags of the element
    cursor.execute("SELECT tags FROM inventory WHERE name=?", (name,))
    result = cursor.fetchone()

    if result:
        current_tags = result[0].split(', ')
        current_tags = [tag for tag in current_tags if tag not in delete_tags]

        # Add new tags
        current_tags.extend(new_tags)

        # Update the element in the database
        cursor.execute("UPDATE inventory SET name=?, quantity=?, modified=?, tags=? WHERE name=?",
                        (new_name, new_quantity, datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        ', '.join(current_tags), name))
        conn.commit()
        print(f"Elemento '{name}' editado con éxito.")
    else:
        print(f"Elemento '{name}' no encontrado en el inventario.")

def order_inventory(criterion):
    # Connect to an existing database or create a new one
    try:
        conn = sqlite3.connect('db/inventory.db')
    except Exception:
        print("Error connecting to database")
        return -1
    # Create table if not exist
    cursor = conn.cursor()
    
    if criterion == "NINGUNO":
        cursor.execute("SELECT * FROM inventory")
    else:
        cursor.execute(f"SELECT * FROM inventory ORDER BY {criterion.lower()}")

def filter_inventory(criterion, condition):
    # Connect to an existing database or create a new one
    try:
        conn = sqlite3.connect('db/inventory.db')
    except Exception:
        print("Error connecting to database")
        return -1
    # Create table if not exist
    cursor = conn.cursor()
    if criterion == "NINGUNO":
        cursor.execute("SELECT * FROM inventory")
    else:
        if criterion.lower() in ['name', 'tags']:
            cursor.execute(f"SELECT * FROM inventory WHERE {criterion.lower()} LIKE ?", (f"%{condition}%",))
        elif criterion.lower() in ['added', 'modified']:
            cursor.execute(f"SELECT * FROM inventory WHERE {criterion.lower()} = ?", (condition,))
