import numpy as np
import time
from blackjack_core import hand_berechnen, deck_erstellen, karte_austeilen

start_time = time.time()
SEED = np.random.seed(42)



def berechne_kommende_karte(eigene_hand, zaehlweise, bisherige_karten, uebrige_karten):
    '''
    Wie sicher kommen gute Karten?
    Input: eigene Hand, Zaehlweise, Kartenhistorie aller Spieler, Anzahl übriger Karten
    Output: Zuverlässigkeits-Score
    '''
    a = 2

    if zaehlweise == 'erster Test':
        eigene_hand = 21 - hand_berechnen(eigene_hand)
        plusminus = 0
        for karte in bisherige_karten:
            if karte in ['K', 'Q', 'J', '10']:
                plusminus += 1
            elif karte in ['2', '3', '4', '5']:
                plusminus -= 1

        if plusminus >= a*2:
            return 0.6
        elif plusminus >= a:
            return 0.3
        elif plusminus >= a/2:
            return 0.15
        elif plusminus == 0:
            return 0
        elif plusminus <= -a*2:
            return -0.6
        elif plusminus <= -a:
            return -0.3
        elif plusminus <= -a/2:
            return -0.15
        else:
            return 0

    if zaehlweise == 'zweiter Test':
        eigene_hand = 21 - hand_berechnen(eigene_hand)
        plusminus = 0
        niedrig = 0
        for karte in bisherige_karten:
            if karte in ['K', 'Q', 'J', '10']:
                plusminus += 1
            elif karte in  ['2', '3', '4', '5']:
                if karte in ['2', '3']:
                    niedrig += 1
                    plusminus -= 1
                else:
                    plusminus -= 1

        #print('Plusminus', plusminus * 0.15)
        if plusminus >= 4:
            return 0.6
        elif plusminus >= 2:
            return 0.3
        elif plusminus >= 1:
            return 0.15
        elif plusminus == 0:
            return 0
        elif plusminus <= -4:
            if niedrig * 5 > uebrige_karten:
                return -1.2
            else:
                return -0.6
        elif plusminus <= -2:
            if niedrig * 5 > uebrige_karten:
                return -0.6
            else:
                return -0.3
        elif plusminus <= 1:
            if niedrig * 5 > uebrige_karten:
                return -0.3
            else:
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


def denk_logik(karten_chance, spieler_brauche, a = 5):
    spieler_karte_kommt = 0

    if karten_chance < 0 and spieler_brauche >= 6:
        spieler_karte_kommt = 2 * abs(karten_chance)
    elif karten_chance < 0 and spieler_brauche <= a and spieler_brauche > 3:
        spieler_karte_kommt = 1 * abs(karten_chance)
    elif karten_chance > 0 and spieler_brauche <= a-1:
        spieler_karte_kommt = -100
    elif karten_chance > 0 and spieler_brauche < 10:
        spieler_karte_kommt = 1 * abs(karten_chance)
    elif karten_chance > 0 and spieler_brauche > 10:
        spieler_karte_kommt = 2 * abs(karten_chance)

    return spieler_karte_kommt


#def dealer_logik():
    #print()


def spielerrunde(spieler_buget, dealer_buget, deck, bisherige_karten, spielerstrategie, dealerstrategie):
    print('TRAALALALALAl')
    uebrige_karten = len(deck)
    spieler_in = True
    spieler_karten_total = []
    dealer_karten_total = []

    spieler_karten, deck = karte_austeilen(deck)
    spieler_karten_total.append(spieler_karten)
    bisherige_karten.append(spieler_karten)
    spieler_karten, deck = karte_austeilen(deck)
    spieler_karten_total.append(spieler_karten)
    bisherige_karten.append(spieler_karten)

    if gewinnt_spieler(spieler_karten_total, dealer_karten_total, True):
        return spieler_buget, dealer_buget, spieler_karten_total, dealer_karten_total, deck, bisherige_karten, spielerstrategie, dealerstrategie

    else:
        uebrige_karten = len(deck)
        while spieler_in and uebrige_karten > 5:
            karten_chance = berechne_kommende_karte(spieler_karten_total, spielerstrategie, bisherige_karten,
                                                    uebrige_karten)
            #dealerbraucht = 21 - hand_berechnen(dealer_karten_total)

            spielerbraucht = 21 - hand_berechnen(spieler_karten_total)
            #print('Spieler braucht ', spielerbraucht)

            spieler_denkt_spieler_karte_kommt = denk_logik(karten_chance,
                                                                                             spielerbraucht)
            if spieler_denkt_spieler_karte_kommt == -100:
                spieler_in = False
            elif spieler_denkt_spieler_karte_kommt > 0.15:
                spieler_karten, deck = karte_austeilen(deck)
                spieler_karten_total.append(spieler_karten)
                bisherige_karten.append(spieler_karten)
                #print('Karte genommen')
            else:
                spieler_in = False
            #print('spieler_denkt_spieler_karte_kommt', spieler_denkt_spieler_karte_kommt)

            if hand_berechnen(spieler_karten_total) > 21:
                #print('Spieler überschiesst')
                spieler_in = False


            uebrige_karten = len(deck)
    return spieler_buget, dealer_buget, spieler_karten_total, dealer_karten_total, deck, bisherige_karten, spielerstrategie, dealerstrategie