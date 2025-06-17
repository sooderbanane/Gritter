
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to the SQLite database
conn = sqlite3.connect('smart_home.db')

# Load data from the database table into a DataFrame
df = pd.read_sql_query("SELECT * FROM behavior_log", conn)
conn.close()

# DEBUG: See what's actually in the database
print("Columns in the database:")
print(df.columns)
print("Preview of the first few rows:")
print(df.head())
