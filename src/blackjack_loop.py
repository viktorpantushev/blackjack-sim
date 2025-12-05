import numpy as np
import pandas as pd
import time
import sys


if '../src' in sys.path:
    sys.path.remove('../src')

sys.path.append('../src')

from blackjack_core import hand_berechnen, deck_erstellen, karte_austeilen
from blackjack_final import Blackjack

from multiprocessing import Pool

def f(x):
    spieler_weise = 'Viktors Special'
    # spieler_weise = 'high/low'
    # spieler_weise = 'Dealer'

    # iterationen_a = [1_000, 5_000, 10_000, 20_000, 40_000, 60_000, 80_000, 100_000]
    total_batches = 10
    batch_size = 100

    for _ in range(1, total_batches):
        spieler_gewinnt = []
        spieler_verliert = []

        for _ in range(1, batch_size):
            spieler_batches = []
            dealer_batches = []

            spieler_gewinnt_n = 0
            # spieler_verliert_n = 0
            rundenlaenge = []
            validation = []

            game = Blackjack(spieler_weise, buget=1000, decksize=6)

            resets = 0
            ## Best for Viktors Special a = 2, b = 6, c = 9
            game.set_A_and_B_and_C(a=2, b=4, c=9)
            ## Best for high/low a = 8
            # game.set_A_and_B_and_C(a=8, b=6, c=9)

            while resets < batch_size:

                spieler_gewinnt_j, temp_rundenlaenge, temp_validation = game.spielerrunde()

                if game.get_resets > resets:
                    if spieler_gewinnt_j == True:
                        spieler_gewinnt_n += 1
                    # elif spieler_gewinnt_j==False:
                    # spieler_verliert_n += 1

                    resets = game.get_resets

                    rundenlaenge.append(temp_rundenlaenge)
                    validation.append(temp_validation)

            # print('Spieler hat n mal gewinnen: ', spieler_gewinnt_n)
            spieler_gewinnt.append(spieler_gewinnt_n)
        print(spieler_gewinnt)

            # spieler_verliert.append(spieler_verliert_n)



if __name__ == '__main__':
    with Pool(12) as p:
        print(p.map(f, [1,1,1,1,1]))




