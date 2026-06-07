import mysql.connector
import subprocess
import os
from dotenv import load_dotenv


# LOAD ENV

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DB_NAME = "football_portugal"


# RESET DATABASE

print("Resetting database...")

conn = mysql.connector.connect(
    host=DB_HOST,
    user="root",
    password=DB_PASSWORD
)

cursor = conn.cursor()

cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")
cursor.execute(f"CREATE DATABASE {DB_NAME}")

cursor.close()
conn.close()

print("Database recreated successfully")


# FETCH DATA

print("Running fetch_data.py...")
subprocess.run(["python", "fetch_data.py"], check=True)


# 3. LOAD DATA (REPLACE)

print("Running database.py...")
subprocess.run(["python", "database.py"], check=True)


# CONNECT TO DB

print("Applying SQL scripts...")

conn = mysql.connector.connect(
    host=DB_HOST,
    user="root",
    password=DB_PASSWORD,
    database=DB_NAME
)

# BUFFERED CURSOR (IMPORTANT FOR MULTIPLE QUERIES)
cursor = conn.cursor(buffered=True)


# FUNCTION TO RUN SQL FILES

def run_sql_file(filename):
    with open(filename, "r", encoding="utf-8") as f:
        sql_script = f.read()

    statements = sql_script.split(";")

    for stmt in statements:
        stmt = stmt.strip()

        if not stmt:
            continue

        # IGNORE SELECTS (debug queries)
        if stmt.upper().startswith("SELECT"):
            print(f"Skipping SELECT:\n{stmt}\n")
            continue

        try:
            cursor.execute(stmt)

        except Exception as e:
            print(f"\nError executing:\n{stmt}\n\nError: {e}\n")


# RUN SCHEMA (PK + FK)

print("Running schema (PK + FK)...")
run_sql_file("sql-schema.sql")


# RUN CLEANUP QUERIES

print("\nRunning cleanup queries...")
run_sql_file("sql-cleanup.sql")


# FINAL COMMIT

conn.commit()

cursor.close()
conn.close()

print("\nPipeline completed successfully")