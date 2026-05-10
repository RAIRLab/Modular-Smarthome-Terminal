# start.py
# Responsible for starting the thread manager and performing basic setup actions, such as
# checking for and initializing the settings file
# Also serves as the entry point for the program

from threading import Thread
import time
import sql
import flaskServer
import plugins
import atexit

# Starting script
def start():
    # Perform setup operations
    setup()

    # Initialize the threads
    sqlThread = Thread(target=sql.thread)
    sqlThread.daemon = True
    pluginsThread = Thread(target=plugins.thread)
    pluginsThread.daemon = True

    # Start the threads
    sqlThread.start()
    pluginsThread.start()
    flaskServer.run_flask()

# Perform setup operations
def setup():
    load_preferences()

# Load the preferences file or, if the preferences file is outdated, update it
def load_preferences():
    print("Preferences loading...")

# Start the program
if __name__ == '__main__':
    start()