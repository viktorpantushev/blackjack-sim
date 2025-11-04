import numpy as np
import time

start_time = time.time()  
#SEED = np.random.seed(42)

printe_es_aus = True

def printe_aus(message= '', ja_nein=False):
    if ja_nein == True:
        print(message)



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
def denk_logik(karten_chance, spieler_brauche, gegenspieler_braucht):
    spieler_karte_kommt = 0
    gegenspieler_karte_kommt = 0
    
    if karten_chance < 0 and spieler_brauche >= 6:
        spieler_karte_kommt = 2 * abs(karten_chance)
    elif karten_chance < 0 and spieler_brauche < 6 and spieler_brauche > 3:
        spieler_karte_kommt = 1 * abs(karten_chance)
    elif karten_chance > 0 and spieler_brauche < 7:
        spieler_karte_kommt = -100
    elif karten_chance > 0 and spieler_brauche < 10:
        spieler_karte_kommt = 1 * abs(karten_chance)
    elif karten_chance > 0 and spieler_brauche > 10:
        spieler_karte_kommt = 2 * abs(karten_chance)
    if karten_chance < 0 and gegenspieler_braucht >= 6:
        gegenspieler_karte_kommt = 2 * abs(karten_chance)
    elif karten_chance < 0 and gegenspieler_braucht < 6 and gegenspieler_braucht > 3:
        gegenspieler_karte_kommt = 1 * abs(karten_chance)
    elif karten_chance > 0 and gegenspieler_braucht < 7:
        gegenspieler_karte_kommt = -100
    elif karten_chance > 0 and gegenspieler_braucht < 10:
        gegenspieler_karte_kommt = 1 * abs(karten_chance)
    elif karten_chance > 0 and gegenspieler_braucht > 10:
        gegenspieler_karte_kommt = 2 * abs(karten_chance)

    return spieler_karte_kommt, gegenspieler_karte_kommt


def blackjack_spielrunde(spieler_buget, dealer_buget, deck, bisherige_karten, spielerstrategie, dealerstrategie):
    uebrige_karten = len(deck)
    einsatz = 0
    while uebrige_karten > 10 and spieler_buget > 0 and dealer_buget > 0:
        printe_aus(f'Spielerbuget: {spieler_buget}', printe_es_aus)
        printe_aus(f'Dealerbuget: {dealer_buget}', printe_es_aus)
        
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
            printe_aus("Patt", True)
            printe_aus(hand_berechnen(spieler_karten_total), True)
            printe_aus((spieler_karten_total), True)
            spieler_buget += einsatz/2
            dealer_buget += einsatz/2
            return spieler_buget, dealer_buget, deck, bisherige_karten
        #Spieler gewinnt
        elif gewinnt_spieler(spieler_karten_total, dealer_karten_total, True):
            printe_aus("Spieler gewinnt", True)
            printe_aus(hand_berechnen(spieler_karten_total), True)
            printe_aus((spieler_karten_total), True)
            spieler_buget
            spieler_buget += einsatz
            return spieler_buget, dealer_buget, deck, bisherige_karten
        #Dealer gewinnt
        elif gewinnt_spieler(dealer_karten_total, spieler_karten_total, True):
            printe_aus("Dealer gewinnt", True)
            printe_aus(hand_berechnen(dealer_karten_total), True)
            printe_aus((dealer_karten_total), True)
            dealer_buget += einsatz
            return spieler_buget, dealer_buget, deck, bisherige_karten
        else:
            printe_aus('Niemand gewinnt', True)

        einsatz += einsatz_temp
        spieler_buget -= einsatz_temp/2
        dealer_buget -= einsatz_temp/2

        #Spieler denkt nach
        karten_chance = berechne_kommende_karte(spieler_karten_total, spielerstrategie, bisherige_karten, uebrige_karten)
        dealerbraucht = 21 - hand_berechnen(dealer_karten_total)
        spielerbraucht = 21 - hand_berechnen(spieler_karten_total)
        printe_aus(f'Einsatz: {einsatz}', printe_es_aus)
        printe_aus(f'Spielerhand: {spieler_karten_total}', printe_es_aus)
        printe_aus(f'Spieler braucht: {spielerbraucht}', printe_es_aus)
        printe_aus(f'Dealerhand: {dealer_karten_total}', printe_es_aus)
        printe_aus(f'Dealer braucht: {dealerbraucht}', printe_es_aus)

        spieler_denkt_spieler_karte_kommt, spieler_denkt_dealer_karte_kommt = denk_logik(karten_chance, spielerbraucht, dealerbraucht)
        

        printe_aus(f'Kartenchance: {karten_chance}', printe_es_aus)
        printe_aus(f'Spieler denkt Spieler karte kommt: {spieler_denkt_spieler_karte_kommt}', printe_es_aus)
        printe_aus(f'Spieler denkt Dealer karte kommt: {spieler_denkt_dealer_karte_kommt}', printe_es_aus)
        


        #Dealer denkt nach
        karten_chance = berechne_kommende_karte(dealer_karten_total, dealerstrategie, bisherige_karten, uebrige_karten)
        dealerbraucht = 21 - hand_berechnen(dealer_karten_total)
        spielerbraucht = 21 - hand_berechnen(spieler_karten_total)
        
        dealer_denkt_dealer_karte_kommt, dealer_denkt_spieler_karte_kommt= denk_logik(karten_chance, dealerbraucht, spielerbraucht)


        printe_aus(f'Kartenchance: {karten_chance}', printe_es_aus)
        printe_aus(f'Dealer denkt Spieler karte kommt: {dealer_denkt_spieler_karte_kommt}', printe_es_aus)
        printe_aus(f'Dealer denkt Dealer karte kommt: {dealer_denkt_dealer_karte_kommt}', printe_es_aus)

        printe_aus('', printe_es_aus)
        uebrige_karten = len(deck)

    spieler_buget += einsatz/2
    dealer_buget += einsatz/2

    printe_aus('', printe_es_aus)
    printe_aus('', printe_es_aus)
    return spieler_buget, dealer_buget, deck, bisherige_karten 


def blackjack():
    runden = 0
    deck = deck_erstellen(4)
    uebrige_karten = len(deck)
    spieler_buget = 1000
    dealer_buget = 1000
    bisherige_karten = []


    while uebrige_karten > 10 and spieler_buget > 0 and dealer_buget > 0:
        runden += 1
        spieler_buget, dealer_buget, deck, bisherige_karten = blackjack_spielrunde(spieler_buget,dealer_buget,deck, bisherige_karten, 'erster Test', 'erster Test')
        printe_aus(f'spieler_buget {spieler_buget}', printe_es_aus)
        printe_aus(f'dealer_buget {dealer_buget}', printe_es_aus)
        uebrige_karten = len(deck)
    printe_aus(f'Runde {runden}', True)
    return spieler_buget, dealer_buget
        

for _ in range (1_000):
    spieler_buget, dealer_buget = blackjack()
    printe_aus(f'Spielerbuget {spieler_buget}', True)
    printe_aus(f'Dealer_buget {dealer_buget}', True)

end_time = time.time()
elapsed_time = end_time - start_time
print(elapsed_time)
