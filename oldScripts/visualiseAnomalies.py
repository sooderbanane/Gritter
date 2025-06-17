import sqlite3
import pandas as pd
import matplotlib.pyplot as plt


conn = sqlite3.connect('smart_home.db')
df = pd.read_sql_query('SELECT * FROM behavior_log',conn )
conn.close()



df['timestamp'] = pd.to_datetime(df['timestamp'])

df['is_anomaly'] = df['is_anomaly'].astype(int) == 1


plt.figure(figsize=(14, 6))
plt.plot(df['timestamp'], df['fridge_opens'], label='Fridge Opens', color='blue')
plt.scatter(df[df['is_anomaly']]['timestamp'],
            df[df['is_anomaly']]['fridge_opens'],
            color='red', label='Anomaly', zorder=5)

plt.title("Fridge Opens with Anomaly Detection")
plt.xlabel("Time")
plt.ylabel("Number of Opens")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

print("Number of anomalies:", df['is_anomaly'].sum())
