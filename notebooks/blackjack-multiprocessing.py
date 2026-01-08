import numpy as np
import sys
if '../src' in sys.path:
    sys.path.remove('../src')
sys.path.append('../src')

cpu_cores = 12

from blackjack_final import Blackjack
from multiprocessing import Pool

total_batches = 2  # total batches *  cpu_cores
batch_size = 600

# Function needed to run the simulation with multiprocessing
def f(x):
    spieler_weise = 'Viktors Special'
    # spieler_weise = 'high/low'
    # spieler_weise = 'Dealer'


    spieler_gewinnt_total = []

    for _ in range(0, total_batches):
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

                    resets = game.get_resets

                    rundenlaenge.append(temp_rundenlaenge)
                    validation.append(temp_validation)

            spieler_gewinnt.append(spieler_gewinnt_n)
        spieler_gewinnt_total.append(spieler_gewinnt)
    return spieler_gewinnt_total



if __name__ == '__main__':
    spieler_gewinnt_total = []
    with Pool(cpu_cores) as p:
        results = p.map(f, range(cpu_cores))  # Pass a range or list to map
        # print(results)

    for result in results:
        # print(result)
        spieler_gewinnt_total.append(result)

    spieler_gewinnt_total = np.array(spieler_gewinnt_total)


    print(spieler_gewinnt_total.mean())
    print(spieler_gewinnt_total.std(ddof=1) / np.sqrt(len(spieler_gewinnt_total)))