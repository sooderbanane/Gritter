import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("output.csv", parse_dates=['timestamp'])

plt.figure(figsize=(16, 8))

# Night shading
for i in range(len(df) - 1):
    if df.iloc[i]['is_night']:
        plt.axvspan(df.iloc[i]['timestamp'], df.iloc[i + 1]['timestamp'], color='gray', alpha=0.1)

# Plot values and anomalies
for col in df.columns:
    if col.endswith("_value"):
        sensor = col.replace("_value", "")
        plt.plot(df['timestamp'], df[col], label=sensor.capitalize())
        anomaly_col = f"{sensor}_anomaly"
        if anomaly_col in df.columns:
            anomalies = df[df[anomaly_col]]
            plt.scatter(anomalies['timestamp'], anomalies[col], marker='x', s=60, label=f"{sensor.capitalize()} Anomaly")

plt.title("Smart Home Sensor Patterns with Anomaly Detection and Night Shading")
plt.xlabel("Time")
plt.ylabel("Sensor Values")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("sensor_plot.png", dpi=300)
plt.show()
