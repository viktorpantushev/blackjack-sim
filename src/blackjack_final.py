import numpy as np
import time
from blackjack_core import hand_berechnen, deck_erstellen, karte_austeilen, gewinnt_spieler

class Blackjack:
    def __init__(self, zaehlweise_spieler, a=5, b=3):
        self.zaehlweise_spieler = zaehlweise_spieler
        self.a = a
        self.b = b
        self.spiel_resets = 0
        self.resetGame()
        print('Blackjack initializiert')

    def resetGame(self, moneyreset=True):
        self.spielerhand = []
        self.dealerhand = []
        self.bisherige_karten = []
        self.deck = deck_erstellen(6)
        self.uebrige_karten = len(self.deck)
        self.einsatz = 0

        if moneyreset:
            self.spieler_buget = 1000
            self.dealer_buget = 1000

    @property
    def get_money(self):
        return self.spieler_buget, self.dealer_buget

    @property
    def get_resets(self):
        return self.spiel_resets


    def set_A_and_B(a,b):
        self.a = a
        self.b = b



    #a verändern
    def __spieler_spielt(self):
        '''
        Wie sicher kommen gute Karten dank Zählstrategien?
        Output: Karten nehmen oder nicht
        '''
        sicherheit:float

        spieler_brauche = 21 - hand_berechnen(self.spielerhand)

        if self.zaehlweise_spieler == 'high/low':
            plusminus = 0
            for karte in self.bisherige_karten:
                if karte in ['K', 'Q', 'J', '10']:
                    plusminus += 1
                elif karte in ['2', '3', '4', '5']:
                    plusminus -= 1
            

            if plusminus >= self.a*2:
                sicherheit = 0.6
            elif plusminus >= self.a:
                sicherheit = 0.3
            elif plusminus >= self.a/2:
                sicherheit = 0.15
            elif plusminus == 0:
                sicherheit = 0
            elif plusminus <= -self.a*2:
                sicherheit = -0.6
            elif plusminus <= -self.a:
                sicherheit = -0.3
            elif plusminus <= -self.a/2:
                sicherheit = -0.3
            else:
                sicherheit = 0

            spieler_karte_kommt = 0

            if sicherheit < 0 and spieler_brauche >= 6:
                spieler_karte_kommt = 2 * abs(sicherheit)
            elif sicherheit < 0 and spieler_brauche <= self.a and spieler_brauche > 3:
                spieler_karte_kommt = 1 * abs(sicherheit)
            elif sicherheit > 0 and spieler_brauche <= self.a-1:
                spieler_karte_kommt = -100
            elif sicherheit > 0 and spieler_brauche < 10:
                spieler_karte_kommt = 1 * abs(sicherheit)
            elif sicherheit > 0 and spieler_brauche > 10:
                spieler_karte_kommt = 2 * abs(sicherheit)

            
            if spieler_karte_kommt > 0.15:
                return 'Nehmen'
            else:
                return 'Nicht Nehmen'
        
        
        elif self.zaehlweise_spieler == 'Viktors Special':
            plusminus = 0
            niedrig = 0
            for karte in self.bisherige_karten:
                if karte in ['K', 'Q', 'J', '10']:
                    plusminus += 1
                elif karte in  ['2', '3', '4', '5']:
                    if karte in ['2', '3']:
                        niedrig += 1
                        plusminus -= 1
                    else:
                        plusminus -= 1

            #print('Plusminus', plusminus * 0.15)
            if plusminus >= self.a*2:
                sicherheit = 0.6
            elif plusminus >= self.a:
                sicherheit = 0.3
            elif plusminus >= self.a/2:
                sicherheit = 0.15
            elif plusminus == 0:
                sicherheit = 0
            elif plusminus <= -self.a*2:
                if niedrig * self.b > self.uebrige_karten:
                    sicherheit = -1.2
                else:
                    sicherheit = -0.6
            elif plusminus <= -self.a:
                if niedrig * self.b > self.uebrige_karten:
                    sicherheit = -0.6
                else:
                    sicherheit = -0.3
            elif plusminus <= self.a/2:
                if niedrig * self.b > self.uebrige_karten:
                    sicherheit = -0.3
                else:
                    sicherheit = -0.15
            else:
                sicherheit = 0

            spieler_karte_kommt = 0

            if sicherheit < 0 and spieler_brauche >= 6:
                spieler_karte_kommt = 2 * abs(sicherheit)
            elif sicherheit < 0 and spieler_brauche <= self.a and spieler_brauche > 3:
                spieler_karte_kommt = 1 * abs(sicherheit)
            elif sicherheit > 0 and spieler_brauche <= self.a-1:
                spieler_karte_kommt = -100
            elif sicherheit > 0 and spieler_brauche < 10:
                spieler_karte_kommt = 1 * abs(sicherheit)
            elif sicherheit > 0 and spieler_brauche > 10:
                spieler_karte_kommt = 2 * abs(sicherheit)

            
            if spieler_karte_kommt > 0.15:
                return 'Nehmen'
            else:
                return 'Nicht Nehmen'      
        
    def __dealer_spielt(self):
        if hand_berechnen(self.dealerhand) >= 17:
            return 'Nicht Nehmen'
        else:
            return 'Nehmen'

    def spielerrunde(self):
        self.spielerhand = []
        self.dealerhand = []
        self.uebrige_karten = len(self.deck)
        if self.uebrige_karten > 6 and self.spieler_buget > 100 and self.dealer_buget > 100:
            for i in range(2):
                spieler_karten, self.deck = karte_austeilen(self.deck)
                self.spielerhand.append(spieler_karten)
                self.bisherige_karten.append(spieler_karten)
            
            for i in range(2):
                dealer_karten, self.deck = karte_austeilen(self.deck)
                self.dealerhand.append(dealer_karten)
                self.bisherige_karten.append(dealer_karten)

            einsatz_t = 70
            self.spieler_buget -= einsatz_t
            self.dealer_buget -= einsatz_t
            self.einsatz += einsatz_t*2

            if gewinnt_spieler(self.dealerhand, self.spielerhand, True):
                self.dealer_buget += self.einsatz
                self.einsatz = 0
            elif gewinnt_spieler(self.spielerhand, self.dealerhand, True):
                self.spieler_buget += self.einsatz
                self.einsatz = 0

            else:
                #fuer ersten einsatz
                erste_runde = True
                self.uebrige_karten = len(self.deck)
                spieler_in = True
                spieler_ueberschiesst = False
                dealer_in = True
                dealer_ueberschiesst = False

                while spieler_in and self.uebrige_karten > 2:
                    if self.__spieler_spielt() == 'Nehmen':
                        spieler_karten, self.deck = karte_austeilen(self.deck)
                        self.spielerhand.append(spieler_karten)
                        self.bisherige_karten.append(spieler_karten)
                        if erste_runde:
                            #Eisatz setzten
                            einsatz_t = 150
                            self.einsatz += einsatz_t*2
                            self.spieler_buget -= einsatz_t
                            self.dealer_buget -= einsatz_t
                            erste_runde = False
                    else:
                        spieler_in = False
                
                    if hand_berechnen(self.spielerhand) > 21:
                        #print('Spieler überschiesst')
                        spieler_in = False
                        spieler_ueberschiesst = True

                    self.uebrige_karten = len(self.deck)

                #Else condition
                while not spieler_ueberschiesst and not dealer_ueberschiesst and dealer_in and self.uebrige_karten > 2:
                    if self.__dealer_spielt() == 'Nehmen':
                        dealer_karten, self.deck = karte_austeilen(self.deck)
                        self.dealerhand.append(dealer_karten)
                        self.bisherige_karten.append(dealer_karten)
                    else:
                        dealer_in = False

                    if hand_berechnen(self.dealerhand) > 21:
                        #print('Spieler überschiesst')
                        dealer_in = False
                        dealer_ueberschiesst = True


                    self.uebrige_karten = len(self.deck)
            

            spieler_value = hand_berechnen(self.spielerhand)
            dealer_value = hand_berechnen(self.dealerhand)

            if spieler_value < 21 and dealer_value < 21:
                wer_gewinnt = gewinnt_spieler(self.spielerhand, self.dealerhand)
                if wer_gewinnt:
                    wer_gewinnt = 'Spieler'
                    self.spieler_buget += self.einsatz
                    self.einsatz = 0
                else:
                    wer_gewinnt = 'Dealer'
                    self.dealer_buget += self.einsatz
                    self.einsatz = 0
            elif spieler_value > 21 and dealer_value > 21:
                wer_gewinnt = 'Niemand'
                self.dealer_buget += self.einsatz/2
                self.spieler_buget += self.einsatz/2
                self.einsatz = 0
            elif spieler_value > 21:
                wer_gewinnt = 'Dealer'
                self.dealer_buget += self.einsatz
                self.einsatz = 0
            else:
                wer_gewinnt = 'Spieler'
                self.spieler_buget += self.einsatz
                self.einsatz = 0

        else:
            if self.spieler_buget < 100 or self.dealer_buget < 100:
                self.spiel_resets += 1
                tempspieler, tempdealer = self.spieler_buget, self.dealer_buget
                self.resetGame()
                return tempspieler, tempdealer
            else:
                self.resetGame(moneyreset=False)
                return 0,0
            
        return 0,0