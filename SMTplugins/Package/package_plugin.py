# SMTplugins/package_plugin.py
# Flask blueprint for the Package Tracker widget

from flask import Blueprint, render_template, jsonify, request
from SMTplugins.Package.packageWidget import packageWidget

package_bp = Blueprint('package', __name__)

def get_blueprint():
    return package_bp

_widget = packageWidget()


@package_bp.route("/widget/packages")
def package_view():
    """Renders the package widget as a standalone HTML fragment."""
    return render_template("package_widget.html", data=_widget.widgetData)


@package_bp.route("/api/packages/data")
def package_data():
    """Returns current package list as JSON."""
    return jsonify(_widget.widgetData)


@package_bp.route("/api/packages/event", methods=["POST"])
def package_event():
    """
    Send a command to the package widget.
    Body (JSON):
      Add:    { "event": "add_package",    "args": { "tracking_number": "...", "carrier": "UPS", "label": "..." } }
      Remove: { "event": "remove_package", "args": { "tracking_number": "..." } }
      Refresh:{ "event": "refresh",        "args": {} }
    """
    body = request.get_json(silent=True) or {}
    event = body.get("event", "")
    args = body.get("args", {})
    _widget.handle_event(event, args)
    return jsonify({"ok": True, "packages": _widget.widgetData["packages"]})