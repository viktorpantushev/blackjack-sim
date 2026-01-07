import numpy as np

seed=42

def gewinnt_spieler(eigene_hand, fremde_hand, punktlandung=False):
    '''
    Gewinnt der Spieler, bzw mach er eine Punktlandung
    Input: Spielerhand, Dealerhand, Punktlandung
    Output: Spieler gewinnt? Boolean
    '''
    '''Rückgabe Spieler gewinne -> true sonst false'''
    if punktlandung:
        if hand_berechnen(eigene_hand) == 21:
            return True
        else:
            return False
    else:
        if   (21 - hand_berechnen(eigene_hand)) < (21 - hand_berechnen(fremde_hand)):
            return True
        elif (21 - hand_berechnen(eigene_hand)) > (21 - hand_berechnen(fremde_hand)):
            return False
        elif (21 - hand_berechnen(eigene_hand)) == (21 - hand_berechnen(fremde_hand)):
            if len(eigene_hand) > len(fremde_hand):
                return False
            elif len(eigene_hand) < len(fremde_hand):
                return True
            else:
                return False


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
    Input: Deckanzahl, optionaler Seed für Randomisierung
    Output: Gemischtes Deck
    '''
    # Ranks of the cards
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    # Create the full deck
    deck = ranks * 4 * decks
    # Set the random seed
    np.random.seed(seed)
    # Shuffle the deck
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