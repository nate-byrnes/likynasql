import sqlite3
import random
import string

def random_string(length):
    return ''.join(random.choices(string.ascii_letters, k=length)) 

def create_database():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    # List all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()

    # Delete all rows from each table
    for table_name in tables:
        cursor.execute(f"DELETE FROM {table_name[0]}")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_table(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name varchar(15) NOT NULL,
            last_name varchar(15) NOT NULL,
            address varchar(25) NOT NULL,
            city varchar(25) NOT NULL
        )
        ''')
    
    conn.commit()
    conn.close()

def insert_data():
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()

    for i in range(100):
        first_name = random_string(10)
        last_name = random_string(10)
        address = random_string(20)
        city = random_string(15)

        cursor.execute('''
            INSERT INTO test_table (first_name, last_name, address, city)
            VALUES (?, ?, ?, ?)
        ''', (first_name, last_name, address, city))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
    insert_data()
    
