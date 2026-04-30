from widget import Widget
from datetime import datetime, date
import calendar
import json
import os
import time


class calendarWidget(Widget):

    def __init__(self):
        # -------- FILES --------
        self.state_file = "calendar_state.json"
        self.events_file = "calendar_events.json"

        # -------- DEFAULT STATE --------
        self.current_date = date.today()

        # -------- LOAD MONTH STATE --------
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    state = json.load(f)
                    if "current_date" in state:
                        self.current_date = date.fromisoformat(state["current_date"])
            except:
                print("State file corrupted, resetting")

        # -------- LOAD EVENTS --------
        if os.path.exists(self.events_file):
            try:
                with open(self.events_file, "r") as f:
                    self._events = json.load(f)
            except:
                print("Events file corrupted, resetting")
                self._events = {}
        else:
            self._events = {}

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
        return self._preferences

    @widgetPreferences.setter
    def widgetPreferences(self, value):
        self._preferences = value

    @property
    def widgetDefaultPreferences(self):
        return {
            "show_week_numbers": False,
            "use_google_cal": False,
            "google_cal_id": "primary"
        }

    @property
    def updateTimer(self):
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
        if not self._events:
            today = date.today().isoformat()
            self._events[today] = [
                {"id": int(time.time()*1000), "title": "Class 4PM – LC 22"},
                {"id": int(time.time()*1000)+1, "title": "Gym 5PM"}
            ]
            self._save_events()

    # -------- EVENT HANDLER --------
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