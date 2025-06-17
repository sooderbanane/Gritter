# Import required libraries
import pandas as pd                  # For data handling
import numpy as np                   # For numerical operations
from sklearn.ensemble import IsolationForest  # For anomaly detection
import sqlite3                       # For storing data in SQLite database


csv_import = "Smart_Home_Behavior_Data.csv"
data = pd.read_csv(csv_import, parse_dates=['timestamp'])

data['hour'] = data['timestamp'].dt.hour
data['is_night'] = data['timestamp'].dt.hour.apply(lambda h: 1 if h < 6 or h > 22 else 0)

features = data[['fridge_opens', 'motion_night', 'stove_uses', 'is_night']]

model = IsolationForest(contamination=0.02, random_state=42)
data['anomaly'] = model.fit_predict(features)
data['is_anomaly'] = data['anomaly'] == -1

conn = sqlite3.connect('smart_home.db')
data.to_sql('behavior_log', conn, if_exists='replace', index=False)  # Save to a table named 'behavior_log'
conn.commit()                                  # Save changes
conn.close()    


print("Analysis complete. Data with anomaly flags saved to smart_home.db in table 'behavior_log'.")
