
import json
import sqlite3
from pathlib import Path

import pandas as pd

DATA_DIR = Path(".")
EXPORT_DIR = DATA_DIR / "exports"
EXPORT_DIR.mkdir(exist_ok=True)

csv_files = sorted(DATA_DIR.glob("*.csv"))

if not csv_files:
    raise RuntimeError("No CSV files found.")

# Export all project CSV datasets to JSON.
for csv_file in csv_files:
    df = pd.read_csv(csv_file)
    records = df.where(pd.notna(df), None).to_dict(orient="records")

    json_path = EXPORT_DIR / f"{csv_file.stem}.json"

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=2, default=str)

    print(f"JSON exported: {json_path}")

# Create a portable SQLite database from the CSV datasets.
db_path = EXPORT_DIR / "marketing_attribution.db"

with sqlite3.connect(db_path) as connection:
    for csv_file in csv_files:
        table_name = csv_file.stem
        df = pd.read_csv(csv_file)
        df.to_sql(table_name, connection, if_exists="replace", index=False)
        print(f"SQL table created: {table_name}")

# Export the SQLite database schema as SQL.
with sqlite3.connect(db_path) as connection:
    schema = connection.execute("""
        SELECT sql
        FROM sqlite_master
        WHERE type = 'table'
        AND sql IS NOT NULL
        ORDER BY name
    """).fetchall()

    sql_path = EXPORT_DIR / "schema.sql"

    with open(sql_path, "w", encoding="utf-8") as file:
        file.write("-- Marketing Attribution database schema\n\n")
        for statement, in schema:
            file.write(statement + ";\n\n")

print("\nAll JSON and SQL exports completed!")
