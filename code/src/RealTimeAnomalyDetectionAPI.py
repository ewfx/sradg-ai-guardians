from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import datetime
import os

app = Flask(__name__)

model = IsolationForest(contamination=0.05, random_state=42)

# Train the Model with Normal Data
normal_data = np.random.normal(loc=50, scale=10, size=200)
df = pd.DataFrame(normal_data, columns=["value"])
model.fit(df[["value"]])

# Define Excel File Path
EXCEL_FILE = "anomalies.xlsx"

@app.route('/predict', methods=['POST'])
def predict():
data = request.json
value = float(data["value"])
prediction = model.predict([[value]])
is_anomaly = prediction[0] == -1

response = {
"As of Date": date,
"is_anomaly": is_anomaly,
"message": "Anomaly detected!" if is_anomaly else "Normal value"
}

# Append anomaly to Excel if detected
if is_anomaly:
new_data = pd.DataFrame([[date, response["Company"], response["Account"], response["AU"], response["Currency"], response["PrimaryAccount"], 
                         response["SecondaryAccount"], response["GLBalance"], response["IHUBBalance"], response["Comments"], is_anomaly ]], 
                        columns=["As of Date", "Company", "Account", "AU", "Currency", "PrimaryAccount", "SecondaryAccount", 
                                 "GLBalance", "IHUB Balance", "Comments", "Anomaly"])

# If file exists, append without headers
if os.path.exists(EXCEL_FILE):
with pd.ExcelWriter(EXCEL_FILE, mode='a', if_sheet_exists='overlay', engine='openpyxl') as writer:
new_data.to_excel(writer, sheet_name="Anomalies", index=False, header=False, startrow=writer.sheets["Anomalies"].max_row)
else:
# Create new file with headers
new_data.to_excel(EXCEL_FILE, sheet_name="Anomalies", index=False)

return jsonify(response)

@app.route('/anomalies', methods=['GET'])
def get_anomalies():
if os.path.exists(EXCEL_FILE):
df = pd.read_excel(EXCEL_FILE, sheet_name="Anomalies")
return jsonify(df.to_dict(orient="records"))
else:
return jsonify({"message": "No anomalies detected yet."})

if __name__ == '__main__':
app.run(host="0.0.0.0", port=5000, debug=True)
