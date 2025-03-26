from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
app = Flask(__name__)
model = IsolationForest(contamination=0.05, random_state=42)

# Sample Data to Train the initial Model
normal_data = np.random.normal(loc=50, scale=10, size=200)
df = pd.DataFrame(normal_data, columns=["value"])
model.fit(df[["value"]])

@app.route('/predict', methods=['POST'])
def predict():
data = request.json # Receive JSON input
value = float(data["value"]) # Extract value
prediction = model.predict([[value]]) # Predict anomaly
is_anomaly = prediction[0] == -1 # -1 means anomaly

response = {
"value": value,
"is_anomaly": is_anomaly,
"message": "Anomaly detected!" if is_anomaly else "Normal value"
}
return jsonify(response)

if __name__ == '__main__':
app.run(host="0.0.0.0", port=5000, debug=True)
