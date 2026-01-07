# 🃏 Blackjack Monte Carlo Analysis

This project provides a high-performance simulation environment for the game **Blackjack**. Using the **Monte Carlo simulation**, hundreds of games are automated to statistically evaluate the efficiency of different counting strategies.

## 🎯 Project Objective
The goal is to provide a quantitative comparison between several card counting strategies and their effectiveness against a dealer using standard Blackjack rules. The primary metric for success is the win rate.

### Strategies
* **Hi-Lo Counting Strategy:** High card ('K', 'Q', 'J', '10') +1, low cards ('2', '3', '4', '5') -1
* **Viktor's Special:** Hi-Lo and extra count for very low cards ('2', '3') +1

## 🚀 Features
* **Multi-Processing:** Leverages `Multiprocessing` to distribute simulations across all available CPU cores for maximum performance.


## 📂 Project Structure
* `notebooks/blackjack-multiprocessing.py`: Central entry point for simulation execution with multiprocessing (not a notebook because multiprocessing and notebooks don't work together).
* `notebooks/notebook.ipynb`: Central entry point for simulation execution without multiprocessing (not a notebook because multiprocessing and notebooks don't work together).


* `src/`:
    * `blackjack_core.py`: Implement basic functions like functions for: who will win, calculating hand values, mixing decks and deal cards.
    * `blackjack_final.py`: Implementation of everything else in the BackJack class.
    
## 📊 Interpretation of Results
The player wins around 3240 out of 7200 times. 


## 🛠 Installation & Usage
0. **Count your cpu cores and change cpu_cores in blackjack-multiprocessing.py**
    ```bash
    cpu_cores = ...
    ```
1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Execute the simulation:**
    ```bash
    python main.py
    ```
