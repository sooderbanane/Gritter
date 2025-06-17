import os
import pandas as pd
from sklearn.ensemble import IsolationForest

data_dir = "testData"
combined_df = None

for file in os.listdir(data_dir):
    if file.endswith(".csv"):
        sensor_name = file.replace("_sensor.csv", "")
        df = pd.read_csv(os.path.join(data_dir, file), parse_dates=['timestamp'])

        # Find the data column
        value_candidates = [col for col in df.columns if col.lower() != 'timestamp']
        if not value_candidates:
            raise ValueError(f"No data column in {file}")
        value_col = value_candidates[0]

        df.rename(columns={value_col: f"{sensor_name}_value"}, inplace=True)

        # Anomaly detection
        model = IsolationForest(contamination=0.02, random_state=42)
        df[f'{sensor_name}_anomaly'] = model.fit_predict(df[[f'{sensor_name}_value']]) == -1

        # Merge into combined_df
        if combined_df is None:
            combined_df = df
        else:
            combined_df = pd.merge(combined_df, df, on="timestamp")

# Add time features
combined_df['hour'] = combined_df['timestamp'].dt.hour
combined_df['is_night'] = combined_df['hour'].apply(lambda h: 1 if h < 6 or h > 22 else 0)

# Save
combined_df.to_csv("output.csv", index=False)
print("✅ Analysis complete. Saved to output.csv")
