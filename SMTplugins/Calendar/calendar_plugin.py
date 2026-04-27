# SMTplugins/Calendar/calendar_plugin.py

from flask import Blueprint, render_template, jsonify, request
from SMTplugins.Calendar.calendarWidget import calendarWidget

calendar_bp = Blueprint('calendar', __name__)

_widget = calendarWidget()
_widget.update()

@calendar_bp.route("/widget/calendar")
def calendar_view():
    return render_template("calendar_widget.html", data=_widget.widgetData)

@calendar_bp.route("/api/calendar/data")
def calendar_data():
    return jsonify(_widget.widgetData)

@calendar_bp.route("/api/calendar/event", methods=["POST"])
def calendar_event():
    body = request.get_json(silent=True) or {}
    event = body.get("event", "")
    args = body.get("args", {})
    _widget.handle_event(event, args)
    return jsonify({"ok": True})