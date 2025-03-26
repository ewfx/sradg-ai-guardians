import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest

np.random.seed(42)
normal_data = np.random.normal(loc=50, scale=10, size=200) 
anomalous_data = np.random.normal(loc=100, scale=5, size=10) 
data = np.concatenate([normal_data, anomalous_data])
df = pd.DataFrame(data, columns=["value"])

model = IsolationForest(contamination=0.05, random_state=42) # Consider 5% as expeced anomalies
df["anomaly_score"] = model.fit_predict(df[["value"]])

# Identify the anomalies here
df["is_anomaly"] = df["anomaly_score"] == -1 

plt.figure(figsize=(10, 5))
sns.scatterplot(x=df.index, y=df["value"], hue=df["is_anomaly"], palette={False: "blue", True: "red"})
plt.xlabel("Index")
plt.ylabel("Value")
plt.title("Anomaly Detection Using Isolation Forest")
plt.legend(["Normal", "Anomaly"])
plt.grid(True)
plt.show()
print("Detected Anomalies:")
print(df[df["is_anomaly"]])
