'''import numpy as np
import time
from blackjack_core import hand_berechnen, deck_erstellen, karte_austeilen

start_time = time.time()
#SEED = np.random.seed(42)
#seed sequence



def berechne_kommende_karte(eigene_hand, zaehlweise, bisherige_karten, uebrige_karten, a=2,b=3):
    
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
        if plusminus >= a*2:
            return 0.6
        elif plusminus >= a:
            return 0.3
        elif plusminus >= a/2:
            return 0.15
        elif plusminus == 0:
            return 0
        elif plusminus <= -a*2:
            if niedrig * b > uebrige_karten:
                return -1.2
            else:
                return -0.6
        elif plusminus <= -a:
            if niedrig * b > uebrige_karten:
                return -0.6
            else:
                return -0.3
        elif plusminus <= a/2:
            if niedrig * b > uebrige_karten:
                return -0.3
            else:
                return -0.15
        else:
            return 0


def gewinnt_spieler(spieler_hand, dealer_hand, punktlandung=False):
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


def denk_logik(karten_chance, spieler_brauche, a = 5, spieler = 'Spieler'):
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


def dealer_spielt(dealer_hand):
    if hand_berechnen(dealer_hand) >= 17:
        return 'Nicht nehmen'
    else:
        return 'Nehmen'



def spielerrunde(spieler_buget, dealer_buget, deck, bisherige_karten, spielerstrategie, a=5):
    uebrige_karten = len(deck)
    spieler_in = True
    dealer_in = True
    spieler_karten_total = []
    dealer_karten_total = []

    spieler_karten, deck = karte_austeilen(deck)
    spieler_karten_total.append(spieler_karten)
    bisherige_karten.append(spieler_karten)
    spieler_karten, deck = karte_austeilen(deck)
    spieler_karten_total.append(spieler_karten)
    bisherige_karten.append(spieler_karten)

    einsatz_t = 10
    spieler_buget -= einsatz_t
    dealer_buget -= einsatz_t
    einsatz = 0
    einsatz += einsatz_t*2

    if gewinnt_spieler(spieler_karten_total, dealer_karten_total, True):
        spieler_buget += einsatz_t
        return spieler_buget, dealer_buget, spieler_karten_total, dealer_karten_total, deck, bisherige_karten, spielerstrategie, True

    else:
        erste_runde = True
        uebrige_karten = len(deck)
        while spieler_in and uebrige_karten > 2:
            karten_chance = berechne_kommende_karte(spieler_karten_total, spielerstrategie, bisherige_karten,
                                                    uebrige_karten)
            #dealerbraucht = 21 - hand_berechnen(dealer_karten_total)

            spielerbraucht = 21 - hand_berechnen(spieler_karten_total)
            #print('Spieler braucht ', spielerbraucht)

            spieler_denkt_spieler_karte_kommt = denk_logik(karten_chance,spielerbraucht, a=a)
            if spieler_denkt_spieler_karte_kommt == -100:
                spieler_in = False
            elif spieler_denkt_spieler_karte_kommt > 0.15:
                if erste_runde:
                    #Einsatz erhöhen
                    einsatz_t += 100 * spieler_denkt_spieler_karte_kommt
                    einsatz += einsatz_t*2
                    spieler_buget -= einsatz_t
                    dealer_buget -= einsatz_t
                    erste_runde = False
                


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
    
        while dealer_in and uebrige_karten > 2:
            dealer_wert = dealer_spielt(dealer_karten_total)

            if dealer_wert == 'Nehmen':
                dealer_karten, deck = karte_austeilen(deck)
                dealer_karten_total.append(dealer_karten)
                bisherige_karten.append(dealer_karten)
            else:
                dealer_in = False

            if hand_berechnen(spieler_karten_total) > 21:
                #print('Spieler überschiesst')
                dealer_in = False

            uebrige_karten = len(deck)
        
    wer_gewinnt = gewinnt_spieler(spieler_karten_total, dealer_karten_total)
    #Spieler gewinnt
    if wer_gewinnt:
        spieler_buget += einsatz
    else:
        dealer_buget += einsatz


    return spieler_buget, dealer_buget, spieler_karten_total, dealer_karten_total, deck, bisherige_karten, spielerstrategie, wer_gewinnt'''