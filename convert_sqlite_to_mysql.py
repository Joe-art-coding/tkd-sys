import sqlite3
import mysql.connector

sqlite_db = 'db.sqlite3'

mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root123',
    'database': 'taekwondo_db'
}

tables_to_exclude = ['sqlite_sequence', 'django_migrations']

print("=" * 50)
print("IMPORT ALL TABLES (WITH DISABLE FK CHECKS)")
print("=" * 50)

# Connect to SQLite
sqlite_conn = sqlite3.connect(sqlite_db)
sqlite_cursor = sqlite_conn.cursor()

# Get all tables
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
all_tables = [row[0] for row in sqlite_cursor.fetchall() if row[0] not in tables_to_exclude]

print(f"\n📋 Tables to import: {len(all_tables)}")

# Connect to MySQL
mysql_conn = mysql.connector.connect(**mysql_config)
mysql_cursor = mysql_conn.cursor()

# Disable foreign key checks
mysql_cursor.execute("SET FOREIGN_KEY_CHECKS=0")
print("\n✓ Foreign key checks disabled")

for table in all_tables:
    print(f"\n📋 Processing {table}...")
    
    try:
        # Get data from SQLite
        sqlite_cursor.execute(f"SELECT * FROM {table}")
        rows = sqlite_cursor.fetchall()
        
        if not rows:
            print(f"   No data in {table}")
            continue
        
        # Get column names
        sqlite_cursor.execute(f"PRAGMA table_info({table})")
        columns = [col[1] for col in sqlite_cursor.fetchall()]
        
        # Escape reserved keywords (like 'key')
        escaped_columns = [f"`{col}`" if col == 'key' else col for col in columns]
        
        # Clear existing data in MySQL
        try:
            mysql_cursor.execute(f"DELETE FROM {table}")
        except:
            print(f"   Table {table} may not exist, skipping")
            continue
        
        # Insert data
        placeholders = ','.join(['%s'] * len(columns))
        columns_str = ','.join(escaped_columns)
        insert_sql = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
        
        inserted = 0
        for row in rows:
            try:
                mysql_cursor.execute(insert_sql, row)
                inserted += 1
            except Exception as e:
                print(f"   Error inserting row: {e}")
        
        mysql_conn.commit()
        print(f"   ✓ Inserted {inserted} rows")
        
    except Exception as e:
        print(f"   ✗ Error: {e}")

# Re-enable foreign key checks
mysql_cursor.execute("SET FOREIGN_KEY_CHECKS=1")
print("\n✓ Foreign key checks re-enabled")

sqlite_conn.close()
mysql_conn.close()

print("\n" + "=" * 50)
print("✅ IMPORT COMPLETED!")
print("=" * 50)