import unittest
import requests
import pandas as pd
import os

# API URL
BASE_URL = "http://localhost:3000"

class TestAnomalyDetectionAPI(unittest.TestCase):

def test_predict_normal_value(self):
"""Test /predict endpoint with a normal value"""
response = requests.post(f"{BASE_URL}/predict", json={"value": 50})
self.assertEqual(response.status_code, 200)
data = response.json()
self.assertIn("is_anomaly", data)
self.assertFalse(data["is_anomaly"], "Expected a normal value but detected an anomaly")

def test_predict_anomalous_value(self):
"""Test /predict endpoint with an anomaly"""
response = requests.post(f"{BASE_URL}/predict", json={"value": 150}) # High value should be an anomaly
self.assertEqual(response.status_code, 200)
data = response.json()
self.assertIn("is_anomaly", data)
self.assertTrue(data["is_anomaly"], "Expected an anomaly but detected as normal")

def test_anomalies_storage(self):
"""Test if anomalies are correctly stored in Excel"""
file_path = "anomalies.xlsx"
if os.path.exists(file_path):
os.remove(file_path) # Delete old file for a fresh test

# Trigger an anomaly
requests.post(f"{BASE_URL}/predict", json={"value": 200})

# Check if the file is created
self.assertTrue(os.path.exists(file_path), "Excel file not created after detecting an anomaly")

# Check file content
df = pd.read_excel(file_path, sheet_name="Anomalies")
self.assertGreater(len(df), 0, "Anomalies Excel file is empty")

def test_get_anomalies(self):
"""Test /anomalies endpoint to retrieve stored anomalies"""
response = requests.get(f"{BASE_URL}/anomalies")
self.assertEqual(response.status_code, 200)
data = response.json()
self.assertIsInstance(data, list, "Anomalies response should be a list")
self.assertGreaterEqual(len(data), 0, "Anomalies list should not be negative")

if __name__ == "__main__":
unittest.main()


Thanks & Regards,
Prasad
Mobile# +919989916106
