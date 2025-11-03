import numpy as np
import time

start_time = time.time()  
SEED = np.random.seed(42)



def hand_berechnen(hand):
    '''
    Die Hand berechnen
    Input: Hand
    Output: Wert der Hand
    '''
    wert = 0
    asse = 0

    #Generelle Berechnung
    for karte in hand:
        if karte in ['K', 'Q', 'J']:
            wert+= 10
        elif karte == 'A':
            asse += 1
            wert += 11
        else:
            wert += int(karte)
    
    #Für Asse nachjustieren
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



def berechne_kommende_karte(eigene_hand, zaehlweise, bisherige_karten, uebrige_karten):
    '''
    Wie sicher kommen gute Karten?
    Input: eigene Hand, Zaehlweise, Kartenhistorie aller Spieler, Anzahl übriger Karten
    Output: Zuverlässigkeits-Score
    '''

    if zaehlweise == 'erster Test':
        eigene_hand = 21 - hand_berechnen(eigene_hand)
        plusminus = 0
        for karte in bisherige_karten:
            if karte in ['K', 'Q', 'J', '10']:
                plusminus += 1
            elif karte in ['2', '3', '4', '5']:
                plusminus -= 1

        if plusminus >= 4:
            return 0.6
        elif plusminus >= 2:
            return 0.3
        elif plusminus >= 1:
            return 0.15
        elif plusminus == 0:
            return 0
        elif plusminus <= -4:
            return -0.6
        elif plusminus <= -2:
            return -0.3
        elif plusminus <= 1:
            return -0.15 
        else:
            return 0



def gewinnt_spieler(spieler_hand, dealer_hand, punktlandung=False):
    '''
    Gewinnt der Spieler, bzw mach er eine Punktlandung
    Input: Spielerhand, Dealerhand, Punktlandung
    Output: Spieler gewinnt? Boolean
    '''
    '''Rückgabe Spieler gewinne -> true sonst false'''
    if punktlandung:
        if hand_berechnen(spieler_hand) == 21:
            return True
    else:
        if (21 - hand_berechnen(spieler_hand)) < (21 - hand_berechnen(dealer_hand)):
            return False
        elif (21 - hand_berechnen(spieler_hand)) > (21 - hand_berechnen(dealer_hand)):
            return True
        elif (21 - hand_berechnen(spieler_hand)) == (21 - hand_berechnen(dealer_hand)):
            if len(spieler_hand) > len(dealer_hand):
                return False
            elif len(spieler_hand) < len(dealer_hand):
                return True


#Fix naming
def denk_logik(karten_chance, spielerbraucht, dealerbraucht):
    spieler_denkt_spieler_karte_kommt = 0
    spieler_denkt_dealer_karte_kommt = 0
    
    if karten_chance < 0 and spielerbraucht >= 6:
            spieler_denkt_spieler_karte_kommt = karten_chance
    elif karten_chance < 0 and spielerbraucht < 6 and spielerbraucht > 3:
        spieler_denkt_spieler_karte_kommt = karten_chance
    elif karten_chance > 0 and spielerbraucht < 10:
        spieler_denkt_spieler_karte_kommt = karten_chance 
    elif karten_chance > 0 and spielerbraucht < 6:
        spieler_denkt_spieler_karte_kommt = -100
    if karten_chance < 0 and dealerbraucht >= 6:
        spieler_denkt_dealer_karte_kommt = karten_chance
    elif karten_chance < 0 and dealerbraucht < 6 and dealerbraucht > 3:
        spieler_denkt_dealer_karte_kommt = karten_chance
    elif karten_chance > 0 and dealerbraucht < 10:
        spieler_denkt_dealer_karte_kommt = karten_chance 
    elif karten_chance > 0 and dealerbraucht < 6:
        spieler_denkt_dealer_karte_kommt = -100

    return spieler_denkt_spieler_karte_kommt, spieler_denkt_dealer_karte_kommt


def blackjack_spielrunde(spieler_buget, dealer_buget, deck, bisherige_karten, spielerstrategie, dealerstrategie):
    uebrige_karten = len(deck)
    einsatz = 0
    while uebrige_karten > 10 and spieler_buget > 0 and dealer_buget > 0:
        print('Spielerbuget: ', spieler_buget)
        print('Dealerbuget: ', dealer_buget)
        
        einsatz_temp = 10
        einsatz += einsatz_temp
        spieler_buget -= einsatz_temp/2
        dealer_buget -= einsatz_temp/2

        dealer_karten_total = []
        spieler_karten_total = []
        #Zwei Karten nehmen
        spieler_karten, deck = karte_austeilen(deck)
        spieler_karten_total.append(spieler_karten)
        bisherige_karten.append(spieler_karten)
        spieler_karten, deck = karte_austeilen(deck)
        spieler_karten_total.append(spieler_karten)
        bisherige_karten.append(spieler_karten)

        dealer_karten, deck = karte_austeilen(deck)
        dealer_karten_total.append(dealer_karten)
        bisherige_karten.append(dealer_karten)
        dealer_karten, deck = karte_austeilen(deck)
        dealer_karten_total.append(dealer_karten)
        bisherige_karten.append(dealer_karten)

        #Patt
        if gewinnt_spieler(spieler_karten_total, dealer_karten_total, True) and gewinnt_spieler(dealer_karten_total, spieler_karten_total, True):
            print("Patt")
            spieler_buget += einsatz/2
            dealer_buget += einsatz/2
            return spieler_buget, dealer_buget, deck, bisherige_karten
        #Spieler gewinnt
        elif gewinnt_spieler(spieler_karten_total, dealer_karten_total, True):
            print("Spieler gewinnt")
            spieler_buget += einsatz
            return spieler_buget, dealer_buget, deck, bisherige_karten
        #Dealer gewinnt
        elif gewinnt_spieler(dealer_karten_total, spieler_karten_total, True):
            print("Dealer gewinnt")
            dealer_buget += einsatz
            return spieler_buget, dealer_buget, deck, bisherige_karten

        einsatz += einsatz_temp
        spieler_buget -= einsatz_temp/2
        dealer_buget -= einsatz_temp/2

        #Spieler denkt nach
        karten_chance = berechne_kommende_karte(spieler_karten_total, spielerstrategie, bisherige_karten, uebrige_karten)
        dealerbraucht = 21 - hand_berechnen(dealer_karten_total)
        spielerbraucht = 21 - hand_berechnen(spieler_karten_total)
        print('Einsatz: ', einsatz)
        print('Spielerhand: ', spieler_karten_total)
        print('Spieler braucht: ', spielerbraucht)
        print('Dealerhand: ', dealer_karten_total)
        print('Dealer braucht: ', dealerbraucht)
        spieler_denkt_spieler_karte_kommt = 0.0
        spieler_denkt_dealer_karte_kommt = 0.0
        #Kleine Karte <=5; Große Karte >= 10
        spieler_denkt_spieler_karte_kommt, spieler_denkt_dealer_karte_kommt = denk_logik(karten_chance, spielerbraucht, dealerbraucht)
        

        print('Kartenchance: ', karten_chance)
        print('Spieler denkt Spieler karte kommt: ', spieler_denkt_spieler_karte_kommt)
        print('Spieler denkt Dealer karte kommt: ', spieler_denkt_dealer_karte_kommt)
        


        #Dealer denkt nach
        karten_chance = berechne_kommende_karte(dealer_karten_total, dealerstrategie, bisherige_karten, uebrige_karten)
        dealerbraucht = 21 - hand_berechnen(dealer_karten_total)
        spielerbraucht = 21 - hand_berechnen(spieler_karten_total)
        dealer_denkt_spieler_karte_kommt = 0.0
        dealer_denkt_dealer_karte_kommt = 0.0
        #Kleine Karte <=5; Große Karte >= 10
        
        dealer_denkt_dealer_karte_kommt, dealer_denkt_spieler_karte_kommt= denk_logik(karten_chance, dealerbraucht, spielerbraucht)


        print('Kartenchance: ', karten_chance)
        print('Dealer denkt Spieler karte kommt: ', dealer_denkt_spieler_karte_kommt)
        print('Dealer denkt Dealer karte kommt: ', dealer_denkt_dealer_karte_kommt)

        print()
        uebrige_karten = len(deck)

    spieler_buget += einsatz/2
    dealer_buget += einsatz/2

    print()
    print()
    return spieler_buget, dealer_buget, deck, bisherige_karten 


def blackjack():
    deck = deck_erstellen(4)
    uebrige_karten = len(deck)
    spieler_buget = 1000
    dealer_buget = 1000
    bisherige_karten = []


    while uebrige_karten > 10 and spieler_buget > 0 and dealer_buget > 0:
        
        spieler_buget, dealer_buget, deck, bisherige_karten = blackjack_spielrunde(spieler_buget,dealer_buget,deck, bisherige_karten, 'erster Test', 'erster Test')
        print('spieler_buget', spieler_buget)
        print('dealer_buget', dealer_buget)
        uebrige_karten = len(deck)
        

for _ in range (10_000):
    blackjack()