import numpy as np
import time
from blackjack_core import hand_berechnen, deck_erstellen, karte_austeilen, gewinnt_spieler

class Blackjack:
    def __init__(self, zaehlweise_spieler, a=2, b=4):
        self.resetGame()
        self.zaehlweise_spieler = zaehlweise_spieler
        self.a = a
        self.b = b
        self.spiel_resets = 0
        print('Blackjack initializiert')

    def resetGame(self):
        self.spielerhand = []
        self.dealerhand = []
        self.bisherige_karten = []
        self.deck = deck_erstellen(6)
        self.uebrige_karten = len(self.deck)
        self.einsatz = 0

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




    def __spieler_spielt(self, spieler_brauche):
        '''
        Wie sicher kommen gute Karten dank Zählstrategien?
        Output: Karten nehmen oder nicht
        '''
        sicherheit:float

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
            elif sicherheit < 0 and spieler_brauche <= a and spieler_brauche > 3:
                spieler_karte_kommt = 1 * abs(sicherheit)
            elif sicherheit > 0 and spieler_brauche <= a-1:
                spieler_karte_kommt = -100
            elif sicherheit > 0 and spieler_brauche < 10:
                spieler_karte_kommt = 1 * abs(sicherheit)
            elif sicherheit > 0 and spieler_brauche > 10:
                spieler_karte_kommt = 2 * abs(sicherheit)

            
            if spieler_denkt_spieler_karte_kommt > 0.15:
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
                if niedrig * self.b > uebrige_karten:
                    sicherheit = -1.2
                else:
                    sicherheit = -0.6
            elif plusminus <= -self.a:
                if niedrig * self.b > uebrige_karten:
                    sicherheit = -0.6
                else:
                    sicherheit = -0.3
            elif plusminus <= self.a/2:
                if niedrig * self.b > uebrige_karten:
                    sicherheit = -0.3
                else:
                    sicherheit = -0.15
            else:
                sicherheit = 0

            spieler_karte_kommt = 0

            if sicherheit < 0 and spieler_brauche >= 6:
                spieler_karte_kommt = 2 * abs(sicherheit)
            elif sicherheit < 0 and spieler_brauche <= a and spieler_brauche > 3:
                spieler_karte_kommt = 1 * abs(sicherheit)
            elif sicherheit > 0 and spieler_brauche <= a-1:
                spieler_karte_kommt = -100
            elif sicherheit > 0 and spieler_brauche < 10:
                spieler_karte_kommt = 1 * abs(sicherheit)
            elif sicherheit > 0 and spieler_brauche > 10:
                spieler_karte_kommt = 2 * abs(sicherheit)

            
            if spieler_denkt_spieler_karte_kommt > 0.15:
                return 'Nehmen'
            else:
                return 'Nicht Nehmen'
        
        
        
    def __dealer_spielt(self):
        if hand_berechnen(self.dealerhand) >= 17:
            return 'Nicht Nehmen'
        else:
            return 'Nehmen'

    def spielerrunde(self):
        if self.uebrige_karten > 4:
            for i in range(2):
                spieler_karten, self.deck = karte_austeilen(self.deck)
                self.spielerhand.append(spieler_karten)
                self.bisherige_karten.append(spieler_karten)
            
            for i in range(2):
                dealer_karten, self.deck = karte_austeilen(self.deck)
                self.dealerhand.append(dealer_karten)
                self.bisherige_karten.append(dealer_karten)

            einsatz_t = 10
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
                dealer_in = True

                while spieler_in and self.uebrige_karten > 2:
                    if self.__spieler_spielt == 'Nehmen':
                        spieler_karten, self.deck = karte_austeilen(self.deck)
                        self.spielerhand.append(spieler_karten)
                        self.bisherige_karten.append(spieler_karten)
                        if erste_runde:
                            #Eisatz setzten
                            einsatz_t = 10
                            self.einsatz += einsatz_t*2
                            self.spieler_buget -= einsatz_t
                            self.dealer_buget -= einsatz_t
                            erste_runde = False
                    else:
                        spieler_in = False
                
                    if hand_berechnen(self.spielerhand) > 21:
                        #print('Spieler überschiesst')
                        spieler_in = False
                        self.dealer_buget += self.einsatz
                        self.einsatz = 0
                        #Return
                        return 'Spieler verliert'

                    self.uebrige_karten = len(self.deck)

                #Else condition
                while dealer_in and self.uebrige_karten > 2:
                    if self.__dealer_spielt == 'Nehmen':
                        dealer_karten, self.deck = karte_austeilen(self.deck)
                        self.dealerhand.append(dealer_karten)
                        self.bisherige_karten.append(dealer_karten)
                    else:
                        dealer_in = False

                    if hand_berechnen(self.dealerhand) > 21:
                        #print('Spieler überschiesst')
                        dealer_in = False
                        self.spieler_buget += self.einsatz
                        self.einsatz = 0
                        return 'Dealer verliert'


                    self.uebrige_karten = len(self.deck)
            

            spieler_value = hand_berechnen(self.spielerhand)
            dealer_value = hand_berechnen(self.dealerhand)

            if spieler_value < 21 and dealer_value < 21:
                wer_gewinnt = gewinnt_spieler(self.spielerhand, self.dealerhand)
                if wer_gewinnt:
                    self.spieler_buget += self.einsatz
                    self.einsatz = 0
                else:
                    self.dealer_buget += self.einsatz
                    self.einsatz = 0
            elif spieler_value > 21 and dealer_value > 21:
                self.dealer_buget += self.einsatz/2
                self.spieler_buget += self.einsatz/2
                self.einsatz = 0
            elif spieler_value > 21:
                self.dealer_buget += self.einsatz
                self.einsatz = 0
            else:
                self.spieler_buget += self.einsatz
                self.einsatz = 0


            print('Spieler Hand', self.spielerhand)
            print('Dealer Hand', self.dealerhand)
            print('Gewinnt Spieler ', wer_gewinnt)

        else:
            self.spiel_resets += 1
            self.resetGame()
            self.spielerrunde()