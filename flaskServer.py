# flaskServer.py
# Responsible for running the internal flask server that handles displaying the UI to the user

from flask import Flask
import time

app = Flask(__name__)

@app.route("/")
def clientHome():
    return "<center><h1>Hello This is the placeholder for the <b>index.html</b></h1></center>" #render_template("clientHome.html")

# Slated for removal-- starting through start.py now
if __name__ == '__main__':
    app.run(debug=True)

def thread():
    setup()
    run()

def setup():
    app.run(debug=True)

def run():
    print("Flask server running...")
    time.sleep(5)