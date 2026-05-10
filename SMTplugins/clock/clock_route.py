from SMTplugins.clock.clock_widget import clockWidget
from flask import jsonify, Blueprint

clock_bp = Blueprint('clock', __name__)

def get_blueprint():
    return clock_bp

@clock_bp.route("/time")
def get_time():
    clock = clockWidget()
    current_time = clock.update()
    return jsonify({"time": current_time})

