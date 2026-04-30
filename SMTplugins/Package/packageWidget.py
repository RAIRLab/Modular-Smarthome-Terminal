# packageWidget.py
# Tracks package deliveries by polling carrier tracking APIs or scraping status.
# Supports manual entry + (stubbed) carrier auto-lookup for UPS, FedEx, USPS.

from widget import Widget
from datetime import datetime
import json
import os

# Path to persist packages between restarts
_DATA_FILE = "package_data.json"

class packageWidget(Widget):

    def __init__(self):
        self._preferences = self.widgetDefaultPreferences
        self._packages = self._load_packages()

    # ── Widget contract ─────────────────────────────────────────────────────

    @property
    def widgetName(self):
        return "Package Tracker"

    @property
    def widgetID(self):
        return "easha:packagewidget"

    @property
    def widgetHTML(self):
        return "package_widget.html"

    @property
    def widgetData(self):
        return {"packages": self._packages}

    @property
    def widgetPreferences(self):
        return self._preferences

    @widgetPreferences.setter
    def widgetPreferences(self, value):
        self._preferences = value

    @property
    def widgetDefaultPreferences(self):
        return {
            "show_delivered": True,    # Keep delivered packages visible
            "max_visible": 5           # Cap on how many to show at once
        }

    @property
    def updateTimer(self):
        # Poll every 30 minutes
        return 1_800_000

    # ── Runtime ─────────────────────────────────────────────────────────────

    def update(self):
        """Refresh tracking status for all non-delivered packages."""
        for pkg in self._packages:
            if pkg["status"] != "Delivered":
                self._refresh_package(pkg)
        self._save_packages()
        print(f"[packageWidget] Updated {len(self._packages)} package(s)")

    def handle_event(self, event, args):
        """
        Supported events:
          - "add_package"    : args = {"tracking_number": "...", "carrier": "UPS|FedEx|USPS|Amazon", "label": "..."}
          - "remove_package" : args = {"tracking_number": "..."}
          - "refresh"        : args = {} — force-refresh all packages now
        """
        if event == "add_package":
            self._add_package(
                tracking_number=args.get("tracking_number", "").strip(),
                carrier=args.get("carrier", "Unknown"),
                label=args.get("label", "Package")
            )
        elif event == "remove_package":
            self._remove_package(args.get("tracking_number", ""))
        elif event == "refresh":
            self.update()
        else:
            print(f"[packageWidget] Unhandled event: {event} args={args}")

    # ── Internal helpers ─────────────────────────────────────────────────────

    def _add_package(self, tracking_number, carrier, label):
        if not tracking_number:
            print("[packageWidget] add_package: missing tracking number")
            return
        # Avoid duplicates
        if any(p["tracking_number"] == tracking_number for p in self._packages):
            print(f"[packageWidget] Package {tracking_number} already tracked")
            return
        pkg = {
            "tracking_number": tracking_number,
            "carrier": carrier,
            "label": label,
            "status": "Pending",
            "last_update": "—",
            "eta": "Unknown",
            "added_on": datetime.now().strftime("%Y-%m-%d")
        }
        self._refresh_package(pkg)
        self._packages.append(pkg)
        self._save_packages()
        print(f"[packageWidget] Added package '{label}' ({tracking_number})")

    def _remove_package(self, tracking_number):
        before = len(self._packages)
        self._packages = [p for p in self._packages if p["tracking_number"] != tracking_number]
        if len(self._packages) < before:
            self._save_packages()
            print(f"[packageWidget] Removed package {tracking_number}")

    def _refresh_package(self, pkg):
        """
        Stub carrier lookup. Replace each block with a real API call.

        UPS:   https://developer.ups.com/api/reference/tracking
        FedEx: https://developer.fedex.com/api/en-us/catalog/tracking
        USPS:  https://www.usps.com/business/web-tools-apis/track-and-confirm-api.htm
        Amazon: scrape or use Arrival Alerts email parsing
        """
        carrier = pkg.get("carrier", "").upper()
        tracking = pkg.get("tracking_number", "")

        try:
            if carrier == "UPS":
                status, eta = self._lookup_ups(tracking)
            elif carrier == "FEDEX":
                status, eta = self._lookup_fedex(tracking)
            elif carrier == "USPS":
                status, eta = self._lookup_usps(tracking)
            else:
                # Unknown carrier — leave as-is
                return

            pkg["status"] = status
            pkg["eta"] = eta
            pkg["last_update"] = datetime.now().strftime("%b %d, %H:%M")

        except Exception as e:
            print(f"[packageWidget] Lookup failed for {tracking}: {e}")

    # ── Carrier stubs (replace with real API calls) ──────────────────────────

    def _lookup_ups(self, tracking_number):
        """
        TODO: Call UPS Tracking API v1.
        Requires: UPS_CLIENT_ID and UPS_CLIENT_SECRET env vars.
        Returns: (status_str, eta_str)
        """
        raise NotImplementedError("UPS API not yet configured. Set UPS_CLIENT_ID + UPS_CLIENT_SECRET.")

    def _lookup_fedex(self, tracking_number):
        """
        TODO: Call FedEx Track API v1.
        Requires: FEDEX_API_KEY and FEDEX_SECRET_KEY env vars.
        Returns: (status_str, eta_str)
        """
        raise NotImplementedError("FedEx API not yet configured. Set FEDEX_API_KEY + FEDEX_SECRET_KEY.")

    def _lookup_usps(self, tracking_number):
        """
        TODO: Call USPS Web Tools Track & Confirm API.
        Requires: USPS_USER_ID env var.
        Returns: (status_str, eta_str)
        """
        raise NotImplementedError("USPS API not yet configured. Set USPS_USER_ID.")

    # ── Persistence ──────────────────────────────────────────────────────────

    def _load_packages(self):
        if os.path.exists(_DATA_FILE):
            try:
                with open(_DATA_FILE, "r") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[packageWidget] Failed to load package data: {e}")
        # Demo data so the widget isn't empty on first run
        return [
            {
                "tracking_number": "1Z999AA10123456784",
                "carrier": "UPS",
                "label": "New Headphones",
                "status": "In Transit",
                "last_update": "Today, 09:14",
                "eta": "Tomorrow",
                "added_on": datetime.now().strftime("%Y-%m-%d")
            },
            {
                "tracking_number": "9400111899223397987318",
                "carrier": "USPS",
                "label": "Textbook",
                "status": "Out for Delivery",
                "last_update": "Today, 07:30",
                "eta": "Today",
                "added_on": datetime.now().strftime("%Y-%m-%d")
            }
        ]

    def _save_packages(self):
        try:
            with open(_DATA_FILE, "w") as f:
                json.dump(self._packages, f, indent=2)
        except Exception as e:
            print(f"[packageWidget] Failed to save package data: {e}")