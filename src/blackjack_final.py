import numpy as np
import time
from blackjack_core import hand_berechnen, deck_erstellen, karte_austeilen, gewinnt_spieler

class Blackjack:
    def __init__(self, zaehlweise_spieler, a=2, b=6, c=8, buget=1000, decksize=6):
        self.zaehlweise_spieler = zaehlweise_spieler
        self.a = a
        self.b = b
        self.c = c
        self.spiel_resets = 0
        self.decksize = decksize
        self.spieler_karte_kommt = 0.0
        self.buget = buget
        self.rundenlaenge = 0
        self.validation = []
        self.resetGame()
        #print('Blackjack initializiert')

    def resetGame(self, moneyreset=True):
        self.spielerhand = []
        self.dealerhand = []
        self.bisherige_karten = []
        self.deck = deck_erstellen(self.decksize)
        self.uebrige_karten = len(self.deck)
        self.einsatz = 0
        self.spieler_karte_kommt = 0.0
        self.validation = []
        self.rundenlaenge = 0

        if moneyreset:
            self.spieler_buget = self.buget
            self.dealer_buget = self.buget

    @property
    def get_money(self):
        return self.spieler_buget, self.dealer_buget

    @property
    def get_resets(self):
        return self.spiel_resets


    def set_A_and_B_and_C(self, a,b,c):
        self.a = a
        self.b = b
        self.c = c



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
                sicherheit = -0.15
            else:
                sicherheit = 0

            spieler_karte_kommt = 0.0

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

            self.spieler_karte_kommt = spieler_karte_kommt

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

            spieler_karte_kommt = 0.0


            if sicherheit < 0 and spieler_brauche >= self.c:
                spieler_karte_kommt = 2 * abs(sicherheit)
            elif sicherheit < 0 and spieler_brauche <= self.c and spieler_brauche > 3:
                spieler_karte_kommt = 1 * abs(sicherheit)
            elif sicherheit > 0 and spieler_brauche > 10:
                spieler_karte_kommt = 2 * abs(sicherheit)
            elif sicherheit > 0 and spieler_brauche <= self.c-1:
                spieler_karte_kommt = -100
            elif sicherheit > 0 and spieler_brauche < 10:
                spieler_karte_kommt = 1 * abs(sicherheit)
            # else:
            #     print('lol ', sicherheit, ' ', spieler_brauche)
            

            self.spieler_karte_kommt = spieler_karte_kommt
            if spieler_karte_kommt > 0.15:
                return 'Nehmen'
            else:
                return 'Nicht Nehmen'      
        
        elif self.zaehlweise_spieler == 'Dealer':
            if hand_berechnen(self.dealerhand) >= 17:
                return 'Nicht Nehmen'
            else:
                return 'Nehmen'


    def __dealer_spielt(self):
        if hand_berechnen(self.dealerhand) >= 17:
            return 'Nicht Nehmen'
        else:
            return 'Nehmen'

    def spielerrunde(self):
        self.spielerhand = []
        self.dealerhand = []
        self.uebrige_karten = len(self.deck)
        
        self.rundenlaenge += 1
        if (self.uebrige_karten > int(float(self.decksize)*52.0*0.3) and self.spieler_buget > int(self.buget/2) and self.dealer_buget > int(self.buget/2)):
            self.rundenlaenge += 1
            for i in range(2):
                spieler_karten, self.deck = karte_austeilen(self.deck)
                self.spielerhand.append(spieler_karten)
                self.bisherige_karten.append(spieler_karten)
            
            for i in range(2):
                dealer_karten, self.deck = karte_austeilen(self.deck)
                self.dealerhand.append(dealer_karten)
                self.bisherige_karten.append(dealer_karten)

            self.uebrige_karten = len(self.deck)

            verbleiben = (self.decksize*52 / self.uebrige_karten) * 2
            if verbleiben > 3:
                verbleiben = 3
            elif verbleiben < 1:
                verbleiben = 1

            verbleiben = ((self.decksize*52) / self.uebrige_karten) * 2
            if verbleiben > 3:
                verbleiben = 3
            elif verbleiben < 1:
                verbleiben = 1

            einsatz_t = 30 * verbleiben
            self.spieler_buget -= einsatz_t
            self.dealer_buget -= einsatz_t
            self.einsatz += einsatz_t*2

            if gewinnt_spieler(self.dealerhand, self.spielerhand, True) and not gewinnt_spieler(self.spielerhand, self.dealerhand, True):
                self.dealer_buget += self.einsatz
                self.einsatz = 0
            elif gewinnt_spieler(self.dealerhand, self.spielerhand, True) and gewinnt_spieler(self.spielerhand, self.dealerhand, True):
                self.dealer_buget += self.einsatz/2
                self.spieler_buget += self.einsatz/2
                self.einsatz = 0
            elif gewinnt_spieler(self.spielerhand, self.dealerhand, True):
                einsatz_t = int(self.einsatz/2)
                self.dealer_buget -= einsatz_t
                self.einsatz += einsatz_t

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
                            verbleiben = ((self.decksize*52) / self.uebrige_karten) * 2
                            if verbleiben > 3:
                                verbleiben = 3
                            elif verbleiben < 1:
                                verbleiben = 1

                            karte_kommt = self.spieler_karte_kommt * 12.0
                            if self.spieler_karte_kommt < 1:
                                karte_kommt = 1
                            if self.spieler_karte_kommt > 7:
                                self.spieler_karte_kommt = 7

                            if self.zaehlweise_spieler == 'Viktors Special':
                                einsatz_t = int(40 * abs(karte_kommt) * (verbleiben*1.5))
                            else:
                                einsatz_t = int(50 * verbleiben)
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


            karte_kommt = self.spieler_karte_kommt * 12.0
            # print(karte_kommt)
            if karte_kommt < 1:
                karte_kommt = 1
            if karte_kommt > 7:
                karte_kommt = 7

            verbleiben = (((self.decksize*52) / self.uebrige_karten))*2
            if verbleiben > 3:
                verbleiben = 3
            elif verbleiben < 1:
                verbleiben = 1

            if wer_gewinnt == 'Spieler':
                #Spielergewinnt, kartekommt, verbleibt
                self.validation.append([True, karte_kommt, verbleiben])
            else:
                self.validation.append([False, karte_kommt, verbleiben])


        else:
            if self.spieler_buget <= int(self.buget/2) or self.dealer_buget <= int(self.buget/2):
                self.spiel_resets += 1
                tempspieler, tempdealer = self.spieler_buget, self.dealer_buget
                spieler_gewinnt = False
                if tempspieler > tempdealer:
                    spieler_gewinnt = True
                
                temp_ruendenlaenge = self.rundenlaenge
                self.resetGame()
                return spieler_gewinnt, temp_ruendenlaenge, self.validation
            else:
                self.resetGame(moneyreset=False)
            
        return False, 0, []