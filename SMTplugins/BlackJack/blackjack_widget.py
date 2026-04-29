from widget import Widget

class BlackjackWidget(Widget):
    
    def widgetName(self): return "Blackjack"
    
    def widgetID(self): return "blackjack"
    
    def widgetHTML(self):
        return """
        <div id="bj-container">
            <div class="bj-area">
                <span class="bj-label">Dealer: <span id="bj-dealer-score">0</span></span>
                <div id="bj-dealer-cards" class="card-row"></div>
            </div>
            <div class="bj-area">
                <span class="bj-label">Player: <span id="bj-player-score">0</span></span>
                <div id="bj-player-cards" class="card-row"></div>
            </div>
            <div class="bj-controls">
                <button id="bj-deal-btn">Deal</button>
                <button id="bj-hit-btn" disabled>Hit</button>
                <button id="bj-stand-btn" disabled>Stand</button>
            </div>
            <div id="bj-status">Press Deal to Start</div>
        </div>
        """
    @property
    def widgetData(self): return {}
    @property
    def widgetPreferences(self): return {}
    @property
    def widgetDefaultPreferences(self): return {}
    @property
    def updateTimer(self): return 0
    def update(self): pass