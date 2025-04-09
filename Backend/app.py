# ==========================
# 🌐 Flask Server with InfluxDB Integration
# ==========================

from flask import Flask, request, render_template
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision

# Create Flask app
app = Flask(__name__)

# ==========================
# 🔸 GLOBAL DATA STORAGE (used for live web visualization)
# ==========================
last_data = {
    "timestamp": None,
    "ozone_ppb": None,
    "source": "ESP8266"
}

# ==========================
# 🔹 InfluxDB Configuration
# ==========================
INFLUXDB_URL = "http;..."   # URL of your InfluxDB server (local or remote)
TOKEN = "private api token"  # Your API token
ORG = ""              # Your InfluxDB organization name
BUCKET = ""       # The bucket to store the data in

# Create InfluxDB client and write API
client = InfluxDBClient(url=INFLUXDB_URL, token=TOKEN, org=ORG)
write_api = client.write_api()

# ==========================
# 🔸 ROUTE - Home Page
# ==========================
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", data=last_data)

# ==========================
# 🔸 ROUTE - Data Reception (ESP8266 POSTs here)
# ==========================
@app.route("/", methods=["POST"])
def receive():
    try:
        # Decode incoming raw data
        raw = request.data.decode()
        print("✅ Received:", raw)

        # Expected format: ozone_ppb=81
        if "ozone_ppb=" in raw:
            value = raw.split("=")[1]
            last_data["ozone_ppb"] = value
            last_data["timestamp"] = datetime.now().strftime("%H:%M:%S")

            # Create a point for InfluxDB
            point = Point("ozone_measurements").field("ozone_ppm", float(last_data["ozone_ppb"]))
            write_api.write(bucket=BUCKET, org=ORG, record=point)

        return "", 204  # Respond with success (no content)
    
    except Exception as e:
        print("❌ Error:", e)
        return "Error", 400

# ==========================
# 🔸 LAUNCH FLASK SERVER
# ==========================
if __name__ == "__main__":
    # Run on all interfaces, port 8086 (same as InfluxDB HTTP port)
    app.run(host="0.0.0.0", port=8086)
