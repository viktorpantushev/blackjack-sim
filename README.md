# 🃏 Blackjack Monte Carlo Simulation

This project provides a high-performance simulation environment for the game **Blackjack**. Using the **Monte Carlo simulation**, hundreds of games are automated to statistically evaluate the efficiency of different counting strategies.

## 🎯 Project Objective
The goal is to provide a quantitative comparison between several card counting strategies and their effectiveness against a dealer using standard Blackjack rules. The primary metric for success is the win rate.

### Strategies
* **Hi-Lo Counting Strategy (using one score):**  Add 1 to the score for each high card played ('K', 'Q', 'J', '10'), subtract 1 for each low card ('2', '3', '4', '5').
* **Viktor's Special (using two scores):** First score is Hi-Lo and second one is calculated by adding 1 to very low cards ('2', '3').

## 🚀 Features
* **Multi-Processing:** Leverages `Multiprocessing` to distribute simulations across all available CPU cores for maximum performance.


## 📂 Project Structure
* `notebooks/blackjack-multiprocessing.py`: Central entry point for simulation execution with multiprocessing (not a notebook because multiprocessing and notebooks don't work together).
* `notebooks/notebook.ipynb`: Central entry point for simulation execution without multiprocessing.


* `src/`:
    * `blackjack_core.py`: Implements basic functions for: who wins, calculating hand values, mixing decks and dealing cards.
    * `blackjack_final.py`: Implements everything else in the Backjack class.
    
## 📊 Interpretation of Results
The player wins around 44% of the time (in 7200 games). 


## 🛠 Installation & Usage
**Count your cpu cores and change cpu_cores in blackjack-multiprocessing.py** 
    (```
    cpu_cores = ...
    ```)
1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Execute blackjack-multiprocessing.py and enjoy the power of Python Multi-Processing!**

**OR (without multiprocessing):** 

1.  **Run notebook.ipynb**
