from flask import Flask, render_template
from clock_widget import clockWidget
###################################################
from temperature_sensor_widget import tempSensorWidget
import os
import json
###################################################
from flask import Flask
from flask import jsonify
app = Flask(__name__)


###################################################

DATA_FILE = "sensor_data.json"
@app.route("/temperature")
def get_temp():
    current_val = "NAN "
    
    # Check if the file exists before trying to read it
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                current_val = str(data.get("temperature"))
        except Exception as e:
            print(f"Error reading JSON file: {e}")

    # Pass the value to Widget Subsystem
    temp_widget = tempSensorWidget()
    temp_widget.updateTemp(current_val) 
    return jsonify({"temp": temp_widget.update()})

    #FOR HOME ASSISTANT UNTESTED
    # try:
    #     # Synchronously pull the latest RETAINED message from the broker
    #     # timeout=1 ensures the webpage doesn't hang if the broker is down
    #     msg = subscribe.simple("home/pi/sensor", hostname="127.0.0.1", timeout=1)
    #     payload = json.loads(msg.payload.decode())
    #     val = str(payload.get("temperature", "0"))
    # except Exception:
    #     val = "0" # Fallback if broker is unreachable
###################################################

#allows for easier starting of flask from start file
def run_flask():
    app.run(debug=True, port=5000, use_reloader=False)

@app.route("/time")
def get_time():
    clock = clockWidget()
    current_time = clock.update()
    return jsonify({"time": current_time})

@app.route("/")
def clientHome():
    clock = clockWidget()
    current_time = clock.update()
    return render_template("index.html", time=current_time)
  
@app.route("/settings")
def settings():
    return render_template("settingspage.html")

# Slated for removal-- starting through start.py now
if __name__ == '__main__':
    app.run(debug=True)
