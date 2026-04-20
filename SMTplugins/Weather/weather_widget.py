from widget import Widget
from weather_route import get_nws_weather

class weatherrWidget(Widget):

    def widgetName(self):
        return "Weather"
    
    def widgetID(self):
        return "weather"
    
    def widgetHTML(self):
        return "<div id='weather'></div>"
    
    def widgetData(self):
        return get_nws_weather()
    
    def widgetPreferences(self):
        return {}
    
    def widgetDefaultPreferences(self):
        return {}
    
    def updateTimer(self):
        return 15000 #Update every 15 secs for testing
    
    def handle_event(self, event, args):
        return None
    
    def update(self):
        return get_nws_weather()