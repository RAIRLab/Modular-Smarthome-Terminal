from flask import Flask, render_template
from clock_widget import clockWidget

from flask import Flask
from flask import jsonify
app = Flask(__name__)

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

# def thread():
#     setup()

# def setup():
#     app.run(debug=True)