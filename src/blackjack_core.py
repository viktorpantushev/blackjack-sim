import numpy as np



def hand_berechnen(hand):
    '''
    Die Hand berechnen
    Input: Hand
    Output: Wert der Hand
    '''
    wert = 0
    asse = 0

    # Generelle Berechnung
    for karte in hand:
        if karte in ['K', 'Q', 'J']:
            wert += 10
        elif karte == 'A':
            asse += 1
            wert += 11
        else:
            wert += int(karte)

    # Für Asse nachjustieren
    while wert > 21 and asse != 0:
        wert -= 10
        asse -= 1

    return wert


def deck_erstellen(decks):
    '''
    Deck erstellen
    Input: Deckanzahl
    Output: Gemischtes Deck
    '''
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = ranks * 4 * decks
    np.random.shuffle(deck)
    return deck




def karte_austeilen(deck):
    '''
    Karte aus Deckziehen
    Input: Deck
    Output: gezogene Karte, restliches Deck
    '''
    karten = []
    m = deck.pop()
    karten.append(m)
    return m, deck

