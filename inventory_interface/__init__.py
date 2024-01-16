import sqlite3
import json
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
        tags TEXT,
        flag INTEGER
    )
''')
  # Commit the changes
  conn.commit()

  # Create dummy entries
  fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  cursor.execute("INSERT INTO inventory (name, quantity, added, modified, tags, flag) VALUES (?, ?, ?, ?, ?, ?)", ('Manzana', 3,'2022-03-19 19:37:42','2023-12-28 13:08:20',json.dumps(['Fruta']), 1))
  cursor.execute("INSERT INTO inventory (name, quantity, added, modified, tags, flag) VALUES (?, ?, ?, ?, ?, ?)", ('Pollo', 1,'2020-09-30 14:04:10','2023-12-28 13:08:20',json.dumps([]), 1))
  cursor.execute("INSERT INTO inventory (name, quantity, added, modified, tags, flag) VALUES (?, ?, ?, ?, ?, ?)", ('Queso', 2,'2020-09-30 14:04:10','2023-11-16 10:17:58',json.dumps(['Lacteo']), 1))
  cursor.execute("INSERT INTO inventory (name, quantity, added, modified, tags, flag) VALUES (?, ?, ?, ?, ?, ?)", ('Huevo', 6,'2020-09-30 14:04:10','2024-01-08 12:31:59',json.dumps([]), 1))
  cursor.execute("INSERT INTO inventory (name, quantity, added, modified, tags, flag) VALUES (?, ?, ?, ?, ?, ?)", ('Tomate', 4,'2023-12-28 13:08:20','2024-01-08 12:31:59',json.dumps(['Verdura']), 1))
  cursor.execute("INSERT INTO inventory (name, quantity, added, modified, tags, flag) VALUES (?, ?, ?, ?, ?, ?)", ('Leche', 2,fecha_actual,fecha_actual,json.dumps(['Lacteo', 'Bebida']), 1))

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
    cursor.execute("SELECT * FROM inventory WHERE flag = 1")
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
        current_tags = json.loads(result[0]) if result[0] else []
        current_tags = [tag for tag in current_tags if tag not in delete_tags]

        # Add new tags
        current_tags.extend(new_tags)

        # Update the element in the database
        cursor.execute("UPDATE inventory SET name=?, quantity=?, modified=?, tags=? WHERE name=?",
                        (new_name, new_quantity, datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        json.dumps(current_tags), name))
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
    # Muestra los resultados
    ordered = cursor.fetchall()
    for i in range(1, 7):
        cursor.execute("UPDATE inventory SET id=? WHERE id=?",(i+10, i))
    for i in range(1, 7):
        cursor.execute("UPDATE inventory SET id=? WHERE name=?",(i, ordered[i-1][1]))
    conn.commit()


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
        cursor.execute(f"SELECT * FROM inventory WHERE {criterion.lower()} LIKE ?", ('%' + condition + '%',))
    result = cursor.fetchall()
    for i in range(1, 7):
        if i not in [row[0] for row in result]:
            cursor.execute("UPDATE inventory SET flag=? WHERE id=?",(0, i))
    for row in result:
        cursor.execute("UPDATE inventory SET flag=? WHERE id=?", (1, row[0]))
    conn.commit()  # Asegúrate de realizar commit después de las actualizaciones
