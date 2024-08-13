from FInCalc import *
import streamlit as st
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt

def main():
    

    # Simulation parameters
    initial_savings = 100000  # Initial savings in dollars
    annual_savings = 10000  # Annual savings in dollars
    annual_expenses = 40000  # Annual expenses in retirement
    annual_return = 0.07  # Expected annual return on investment
    inflation_rate = 0.02  # Expected annual inflation rate
    years_to_retirement = 20  # Years until retirement
    years_in_retirement = 30  # Years in retirement
    withdrawal_rate = 0.04  # Withdrawal rate in retirement
    num_simulations = 1000  # Number of simulation runs

    # Function to simulate one scenario
    def simulate_retirement():
        # Simulate the savings accumulation phase
        savings = initial_savings
        for _ in range(years_to_retirement):
            savings *= (1 + annual_return)
            savings += annual_savings

        # Simulate the retirement phase
        portfolio_values = []
        for _ in range(years_in_retirement):
            withdrawal = annual_expenses
            withdrawal *= (1 + inflation_rate)  # Adjust for inflation
            savings -= withdrawal
            savings *= (1 + annual_return)
            portfolio_values.append(savings)

        return portfolio_values

    # Run simulations
    all_simulations = []
    for _ in range(num_simulations):
        simulation_result = simulate_retirement()
        all_simulations.append(simulation_result)

    # Calculate probabilities
    success_count = sum(1 for simulation in all_simulations if simulation[-1] > 0)
    success_probability = success_count / num_simulations

    # Plot the results
    plt.figure(figsize=(12, 6))
    for simulation in all_simulations:
        plt.plot(simulation, color='grey', alpha=0.1)

    plt.axhline(0, color='red', linestyle='--', label='Broke Line')
    plt.title('Monte Carlo Simulation of Retirement Portfolio')
    plt.xlabel('Years in Retirement')
    plt.ylabel('Portfolio Value ($)')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

    print(f"Probability of financial success: {success_probability:.2%}")

if __name__ == "__page__":
    main()
            