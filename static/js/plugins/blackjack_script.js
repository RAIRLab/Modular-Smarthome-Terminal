let deck = [];
let pHand = [];
let dHand = [];

async function startNewGame() {
    const res = await fetch('/blackjack/deal');
    const data = await res.json();
    deck = data.deck;
    pHand = data.player;
    dHand = data.dealer;
    // Hide dealer's second card initially for UI
    updateUI(false, true); 
}

async function hit() {
    const res = await fetch('/blackjack/hit', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ deck: deck })
    });
    const data = await res.json();
    pHand.push(data.card);
    deck = data.remaining_deck;
    
    if (calcScore(pHand) > 21) endGame("Busted! Dealer Wins.");
    else updateUI(false, true);
}

async function stand() {
    const res = await fetch('/blackjack/stand', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ deck: deck, dealer_hand: dHand })
    });
    const data = await res.json();
    dHand = data.dealer_hand;
    deck = data.remaining_deck;
    
    const pScore = calcScore(pHand);
    const dScore = data.dealer_score;
    
    if (dScore > 21) endGame("Dealer Busted! You Win!");
    else if (pScore > dScore) endGame("You Win!");
    else if (dScore > pScore) endGame("Dealer Wins.");
    else endGame("Push (Tie).");
}

function calcScore(hand) {
    let s = 0, aces = 0;
    hand.forEach(c => {
        if (['J','Q','K'].includes(c.value)) s += 10;
        else if (c.value === 'A') { s += 11; aces++; }
        else s += parseInt(c.value);
    });
    while (s > 21 && aces > 0) { s -= 10; aces--; }
    return s;
}

function updateUI(over, hideDealer = false) {
    render('bj-player-cards', pHand);
    // If hideDealer is true, we only show the first card
    render('bj-dealer-cards', hideDealer ? [dHand[0]] : dHand);
    
    document.getElementById('bj-player-score').innerText = calcScore(pHand);
    document.getElementById('bj-dealer-score').innerText = hideDealer ? "?" : calcScore(dHand);
    
    document.getElementById('bj-deal-btn').disabled = !over;
    document.getElementById('bj-hit-btn').disabled = over;
    document.getElementById('bj-stand-btn').disabled = over;
    if (!over) document.getElementById('bj-status').innerText = "Game in progress...";
}

function render(id, hand) {
    const el = document.getElementById(id);
    el.innerHTML = '';
    hand.forEach(c => {
        const color = (c.suit === 'hearts' || c.suit === 'diamonds') ? 'red' : 'black';
        el.innerHTML += `<div class="bj-card ${color}">${c.value}</div>`;
    });
}

function endGame(m) {
    updateUI(true, false);
    document.getElementById('bj-status').innerText = m;
}

document.addEventListener('click', e => {
    if (e.target.id === 'bj-deal-btn') startNewGame();
    if (e.target.id === 'bj-hit-btn') hit();
    if (e.target.id === 'bj-stand-btn') stand();
});

async function setup(){
    const widget = document.getElementById('bj-container');
    if(!widget) return;

    try{

        widget.innerHTML = `
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
        `
    } catch(error){
        console.error('BlackJack widget error:', error)
    }
}

setup();