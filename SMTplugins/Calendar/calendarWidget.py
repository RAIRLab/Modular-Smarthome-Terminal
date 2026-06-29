# calendarWidget.py
# Displays a monthly calendar with Google Calendar event integration (optional)
# Falls back to a static calendar view if no credentials are provided

from widget import Widget
from datetime import datetime, date, timedelta
import calendar
import json
import os
import time

class calendarWidget(Widget):

    def __init__(self):
        self._preferences = self.widgetDefaultPreferences
        self.file = "calendar_events.json"

        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                self._events = json.load(f)
        else:
            self._events = {}

        self.current_date = date.today()
        self.state_file = "calendar_state.json"

    # -------- METADATA --------
    @property
    def widgetName(self):
        return "Calendar Widget"

    @property
    def widgetID(self):
        return "easha:calendarwidget"

    @property
    def widgetHTML(self):
        return "calendar_widget.html"

    # -------- MAIN DATA --------
    @property
    def widgetData(self):
        today = date.today()
        year = self.current_date.year
        month = self.current_date.month

        cal = calendar.Calendar(firstweekday=6)
        weeks = cal.monthdatescalendar(year, month)

        weeks_data = []
        for week in weeks:
            days = []
            for d in week:
                days.append({
                    "day": d.day,
                    "in_month": d.month == month,
                    "is_today": d == today,
                    "date_str": d.isoformat(),
                    "events": self._events.get(d.isoformat(), [])
                })
            weeks_data.append(days)

        return {
            "month_name": self.current_date.strftime("%B"),
            "year": year,
            "weeks": weeks_data,
            "day_headers": ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        }

    # -------- PREFERENCES --------
    @property
    def widgetPreferences(self):
        return {}
    

    @property
    def widgetDefaultPreferences(self):
        return {
            "show_week_numbers": False,
            "use_google_cal": False,   # Set True + provide creds to enable
            "google_cal_id": "primary"
        }

    @property
    def updateTimer(self):
        # Refresh every 10 minutes
        return 600_000

    # -------- SAVE HELPERS --------
    def _save_state(self):
        with open(self.state_file, "w") as f:
            json.dump({
                "current_date": self.current_date.isoformat()
            }, f)

    def _save_events(self):
        with open(self.events_file, "w") as f:
            json.dump(self._events, f)

    # -------- OPTIONAL DEFAULT DATA --------
    def update(self):
        """Called by the widget subsystem on a timer. Fetches events if enabled."""
        if self._preferences.get("use_google_cal"):
            self._fetch_google_events()
        else:
            # Only add demo data if nothing exists yet
            if not self._events:
                today = date.today().isoformat()
                self._events[today] = ["Class 4PM – LC 22", "Gym 5PM"]

        print(f"Calendar Widget updated – {date.today().strftime('%B %Y')}")

    def _fetch_google_events(self):
        """
        Stub for Google Calendar API integration.
        To enable: install google-auth + google-api-python-client,
        create OAuth credentials, and fill in the logic below.
        """
        try:
            # TODO: implement OAuth flow and fetch events for current month
            # from googleapiclient.discovery import build
            # service = build("calendar", "v3", credentials=creds)
            # events_result = service.events().list(...).execute()
            raise NotImplementedError("Google Calendar auth not yet configured.")
        except Exception as e:
            print(f"[calendarWidget] Google Calendar fetch failed: {e}")

    def handle_event(self, event, args):

    # -------- ADD TASK --------
        if event == "add_event":
            date_str = args.get("date")
            title = args.get("title", "Event")

            if date_str:
                if date_str not in self._events:
                    self._events[date_str] = []

                self._events[date_str].append({
                    "id": int(time.time()*1000),
                    "title": title
                })

                self._save_events()

        # -------- NEXT MONTH --------
        elif event == "next_month":
            print("NEXT MONTH TRIGGERED")

            if self.current_date.month == 12:
                self.current_date = self.current_date.replace(
                    year=self.current_date.year + 1,
                    month=1
                )
            else:
                self.current_date = self.current_date.replace(
                    month=self.current_date.month + 1
                )

            self._save_state()
            print("NEW MONTH:", self.current_date)

        # -------- PREVIOUS MONTH --------
        elif event == "prev_month":
            print("PREV MONTH TRIGGERED")

            if self.current_date.month == 1:
                self.current_date = self.current_date.replace(
                    year=self.current_date.year - 1,
                    month=12
                )
            else:
                self.current_date = self.current_date.replace(
                    month=self.current_date.month - 1
                )

            self._save_state()
            print("NEW MONTH:", self.current_date)

        else:
            print(f"[calendarWidget] Unhandled event: {event} args={args}")