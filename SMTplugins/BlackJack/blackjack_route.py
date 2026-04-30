from flask import Blueprint, jsonify, request
import random
from SMTplugins.BlackJack.blackjack_widget import BlackjackWidget
blackjack_bp = Blueprint('blackjack_bp', __name__)

SUITS = ['hearts', 'diamonds', 'spades', 'clubs']
VALUES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

def get_score(hand):
    score = 0
    aces = 0
    for c in hand:
        if c['value'] in ['J', 'Q', 'K']: score += 10
        elif c['value'] == 'A': score += 11; aces += 1
        else: score += int(c['value'])
    while score > 21 and aces > 0:
        score -= 10
        aces -= 1
    return score

@blackjack_bp.route('/blackjack/deal', methods=['GET'])
def deal():
    deck = [{'value': v, 'suit': s} for s in SUITS for v in VALUES]
    random.shuffle(deck)
    player = [deck.pop(), deck.pop()]
    dealer = [deck.pop(), deck.pop()]
    return jsonify({"player": player, "dealer": dealer, "deck": deck})

@blackjack_bp.route('/blackjack/hit', methods=['POST'])
def hit():
    data = request.json
    deck = data.get('deck', [])
    return jsonify({"card": deck.pop(), "remaining_deck": deck})

@blackjack_bp.route('/blackjack/stand', methods=['POST'])
def stand():
    data = request.json
    deck = data.get('deck', [])
    dealer_hand = data.get('dealer_hand', [])
    
    # Dealer must hit until score >= 17
    while get_score(dealer_hand) < 17:
        dealer_hand.append(deck.pop())
        
    return jsonify({
        "dealer_hand": dealer_hand,
        "remaining_deck": deck,
        "dealer_score": get_score(dealer_hand)
    })