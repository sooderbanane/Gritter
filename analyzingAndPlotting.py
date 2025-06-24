import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

# 1. Setup
data_dir = "testData"
combined_df = pd.DataFrame()

# 2. Load and process each CSV
for file in os.listdir(data_dir):
    if file.endswith(".csv"):
        filepath = os.path.join(data_dir, file)
        sensor_name = file.replace(".csv", "")

        # Load data
        df = pd.read_csv(filepath, parse_dates=['timestamp'])
        print("data loaded" + df)

        # Find data column
        value_col = [col for col in df.columns if col.lower() != 'timestamp']
        if not value_col:
            raise ValueError(f"No data column in {file}")
        value_col = value_col[0]
        df.rename(columns={value_col: 'value'}, inplace=True)

        # Anomaly detection
        model = IsolationForest(contamination=0.02, random_state=42)
        df['anomaly'] = model.fit_predict(df[['value']]) == -1
        print("anomaly detected" + df)

        # Label columns for merging
        df.rename(columns={'value': f'{sensor_name}_value', 'anomaly': f'{sensor_name}_anomaly'}, inplace=True)

        # Merge into combined dataframe
        if combined_df.empty:
            combined_df = df
        else:
            combined_df = pd.merge(combined_df, df, on='timestamp', how='outer')

# 3. Add night/day info
combined_df['timestamp'] = pd.to_datetime(combined_df['timestamp'])
combined_df.sort_values('timestamp', inplace=True)
combined_df['hour'] = combined_df['timestamp'].dt.hour
combined_df['is_night'] = combined_df['hour'].apply(lambda h: 1 if h < 6 or h > 22 else 0)
print (combined_df)
# 4. Plot
plt.figure(figsize=(16, 8))


# Night shading
for i in range(len(combined_df) - 1):
    if combined_df.iloc[i]['is_night']:
        plt.axvspan(combined_df.iloc[i]['timestamp'], combined_df.iloc[i + 1]['timestamp'], color='gray', alpha=0.1)

sensor_colors = {
    "fridge": "blue",
    "stove": "green",
    "motion": "orange",
    "combined_sensors": "purple",
}


# Sensor lines + anomalies
for col in combined_df.columns:
    if col.endswith('_value'):
        sensor = col.replace('_value', '')
        color = sensor_colors.get(sensor, None)
        plt.plot(combined_df['timestamp'], combined_df[col], label=sensor.capitalize(), color=color)
        if f'{sensor}_anomaly' in combined_df.columns:
            anomalies = combined_df[combined_df[f'{sensor}_anomaly']]
            plt.scatter(anomalies['timestamp'], anomalies[col], marker='x', s=60, label=f"{sensor.capitalize()} Anomaly", color=color)

# Final plot formatting
plt.title("Smart Home Sensors – Multi-Line Anomaly Detection with Night Shading")
plt.xlabel("Time")
plt.ylabel("Sensor Values")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("sensor_plot.png", dpi=300)
plt.show()
