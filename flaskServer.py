from flask import Flask, render_template, request, jsonify
import os
import sys
import json
import importlib

'''from SMTplugins.pluginImports import *
from SMTplugins.Calendar.calendar_plugin import calendar_bp
from SMTplugins.Package.package_plugin import package_bp
'''
from flask import Flask, render_template
from flask import Flask
from flask import jsonify
import os
import json

app = Flask(__name__)



#######PLUGINS#######
# IMPORTANT - Every bp file must have a function called get_blueprint() that returns the blueprint to be registered
# ALSO!!!! FOR SOME REASON YOU CANT USE FROM X IMPORT Y. ONLY USE "IMPORT Y" WHEN MAKING WIDGETS
# Recursive function that searches for all .py files in the filepath, including all subfolders in the path
def deep_search_for_module_blueprints(filepath):
    returnList = []
    specList = []

    for filename in os.listdir(filepath):
        current_filepath = filepath + "\\" + filename

        # If we found a directory, recursively search it for plugins
        if os.path.isdir(current_filepath) and filename != "__pycache__":
            recur_returnList, recur_specList = deep_search_for_module_blueprints(current_filepath)
            returnList.extend(recur_returnList)
            specList.extend(recur_specList)

        # If we found a module, lazily import it
        elif filename.endswith('.py'):
            print("Importing " + current_filepath)

            module_name = filename[:-3]
            spec = importlib.util.spec_from_file_location(module_name, (current_filepath))
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module_name
            returnList.append(module)
            specList.append(spec)

    return returnList, specList

# Retrieve our potential blueprints and specs
potential_bps, specList = deep_search_for_module_blueprints(os.getcwd() + "\\SMTplugins")

# Actually perform the code executions in our imported modules
for i in range(0, len(potential_bps)):
    specList[i].loader.exec_module(potential_bps[i])

for potential_bp in potential_bps:
    bp_call = getattr(potential_bp, "get_blueprint", None)
    if bp_call != None:
        app.register_blueprint(bp_call())


#allows for easier starting of flask from start file
def run_flask():
    app.run(debug=True, port=5000, use_reloader=False)



@app.route("/")
def clientHome():
    # This could be from a database for now its json layout_client.json
    DATA_FILE = "layout_client.json"
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)

    # Passes the list of widgets to the template
    return render_template('index.html', widgets=data['widgets'])
    #return render_template("index.html")

@app.route("/settings")
def settings():
    return render_template("settingspage.html")

# Slated for removal-- starting through start.py now
if __name__ == '__main__':
    app.run(debug=True)



@app.route("/api/layout", methods=["GET"])
def get_layout():
    with open("layout_client.json", "r") as file:
        layout = json.load(file)
    return jsonify(layout)


@app.route("/api/layout", methods=["POST"])
def save_layout():
    new_layout = request.json

    with open("layout_client.json", "w") as file:
        json.dump(new_layout, file, indent=4)

    return jsonify({"message": "Layout saved"})


@app.route("/api/layout/default", methods=["POST"])
def reset_layout():
    with open("default_layout_client.json", "r") as file:
        default_layout = json.load(file)

    with open("layout_client.json", "w") as file:
        json.dump(default_layout, file, indent=4)

    return jsonify(default_layout)


if __name__ == '__main__':
    app.run(debug=True)
