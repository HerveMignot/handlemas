import random

import streamlit as st


MAX_GAMES = 10_000

def estimate_handle(start: float, payback_rate: float, bet: float, run: int = 100) -> float:
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


st.title("Handle Estimator")

start_amount = st.number_input('Initial amount:', min_value=0, max_value=1000)
payback_rate = st.number_input('Payback rate:', min_value=0.0, max_value=1.0, value=0.95)
minimum_bet = st.number_input('Minimum bet:', min_value=1, max_value=10)

simulate_btn = st.button("Simulate")
if simulate_btn:
    handle, games, history = estimate_handle(start_amount, payback_rate, minimum_bet)
    st.write('Estimated Handle:', handle)
    st.write('Number of games', games)
    st.line_chart(history)
