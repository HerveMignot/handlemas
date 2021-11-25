import random

import streamlit as st

from typing import Tuple, List

from streamlit.config import _global_development_mode


MAX_GAMES = 10_000

def simulate_handle(start: float, payback_rate: float, bet: float) -> Tuple[float, int, List[float]]:
    """Run a simulation game and stop when player is broken

    Parameters
    ----------
    start: float: initial amount available
    payback_rate: float: payback rate
    bet: float: minimum bet
    
    Return
    ------
    A tuple with the calculated handle, the number of games, and the history of amount available to player

    """
    purse, handle, games = start, 0, 0
    history = []
    while purse >= bet:
        purse += -bet if random.random() > payback_rate else 0
        handle += bet
        games += 1
        history.append(purse)
        if games >= MAX_GAMES:
            break
    
    return (handle, games, history)


def estimate_handle(start: float, payback_rate: float, bet: float, run: int = 100) -> Tuple[float, float, List[float], List[int]]:
    handles: List[float] = []
    games: List[int] = []

    for r in range(run):
        handle, game, _ = simulate_handle(start, payback_rate, bet)
        handles.append(handle)
        games.append(game)
    return (sum(handles) / len(handles), sum(games) / len(games), handles, games)

    
st.title("Handle Estimator")
st.write("Try with initial 100, 94% and minimum 3")
start_amount = st.number_input('Initial amount:', min_value=0, max_value=1000)
payback_rate = st.number_input('Payback rate:', min_value=0.0, max_value=1.0, value=0.95)
minimum_bet = st.number_input('Minimum bet:', min_value=1, max_value=10)

buttons = st.columns(3)
simulate_btn = buttons[0].button("Simulate 1 game")
estimate_btn = buttons[1].button("Estimate handle")
nb_runs = buttons[2].slider('Runs:', 0, 500, 100, step=10)

if simulate_btn:
    handle, games, history = simulate_handle(start_amount, payback_rate, minimum_bet)
    st.write('Computed handle:', handle)
    st.write('Number of games', games)
    st.line_chart(history)

if estimate_btn and nb_runs > 0:
    #nb_runs = 100
    estimated_handle, average_games, handles, games = estimate_handle(start_amount, payback_rate, minimum_bet, nb_runs)
    st.write('Estimated handle:', round(estimated_handle, 2), ' over ', nb_runs, 'simulation' + 's' if nb_runs > 1 else '')
    st.write('Average number of games', round(average_games,1))
    st.line_chart(handles)
