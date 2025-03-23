from FInCalc import *
import streamlit as st
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
import pandas as pd

def main():
    # Retrieve global variables.
    discrete_palette = st.session_state.discrete_palette
    fontsize = st.session_state.fontsize

    # Define input widgets.
    with st.expander("**Calculator inputs**", expanded = True):
        col1, col2, col3, col4 = st.columns(4, vertical_alignment = "center")
        with col1: 
            principal = st.number_input("Initial investment (€)", 
                                        min_value = 0, 
                                        value = 1500, 
                                        step = 50, 
                                        help = "Amount in Euros")

            contribution = st.number_input("Contribution (€)", 
                                           min_value = 0, 
                                           value = 100, 
                                           step = 50, 
                                           help = "Recurrent contribution")

        with col2: 
            times_compounded = st.number_input("Times compounded", 
                                               min_value = 1, 
                                               value = 12, 
                                               help = "How many times the interest compounds")

            years = st.number_input("Years", 
                                    min_value = 1, 
                                    value = 35, 
                                    help = "Time horizon")

        with col3:
            annual_rate = st.number_input("Annual Growth Rate (%)", 
                                          min_value = 0.00, 
                                          value = 5.0, 
                                          step = 0.01, 
                                          help = "Expected annual growth rate")

            ter = st.number_input("TER (%)", 
                                  min_value = 0.00, 
                                  value = 0.00, 
                                  step = 0.01, 
                                  help = "Total Expense Ratio, from a given ETF. Use 0 otherwise.")
        
        with col4:
            inflation = st.toggle("Account for inflation?", 
                                  help = "This substracts an average 2% inflation to the annual rate provided.")
            
            log_y = st.toggle("Log scale?", 
                              help = "Log 10 scale the Y axis.")
            
    
    # Compute compound interst and return data.
    amount = compound_interest(principal = principal, 
                               annual_rate = annual_rate, 
                               times_compounded = times_compounded, 
                               years = years, 
                               contribution = contribution,
                               ter = ter, 
                               inflation = inflation)        
    
    # Compute plots.
    p1, p2 = plot_compound_interest(data = amount, 
                                   discrete_palette = discrete_palette, 
                                   log_y = log_y, 
                                   fontsize = fontsize)
    
    # Display items.

    # Tags.
    with st.container():
        col1, col2, col3, col4 = st.columns(4, vertical_alignment = "center")
        with col1: st.metric("Initial Investment", f"{format_number(principal)} €")
        with col2: st.metric("Periodical contributions", f"{format_number(contribution * times_compounded * years)} €")
        with col3: st.metric("Interest earned", f"{format_number(amount['Interest'].values.tolist()[-1])} €")
        with col4: st.metric("Total earned", f"{format_number(amount['Total Show'].values.tolist()[-1])} ")
        style_metric_cards(border_left_color = "black", box_shadow = False)

    # Plots
    with st.container():
       st.plotly_chart(p1, use_container_width = True)

       col1, col2 = st.columns([1, 2])

       with col1: st.plotly_chart(p2, use_container_width = True)

       # Make dataframe pretty.
       # Format numbers with dots as thousands separator

       with col2: st.dataframe(amount.loc[:, ["Year", "Initial Investment", "Contributions", "Interest", "Total Show"]],
        hide_index = True,
        column_config = {"Initial Investment": st.column_config.NumberColumn(format="euro", step = 1),
        "Contributions": st.column_config.NumberColumn(format="euro", step = 1),
        "Interest": st.column_config.NumberColumn(format="euro", step = 1),
            "Total Show": st.column_config.NumberColumn("Total", format="euro", step = 0)})



if __name__ == "__page__":
    main()
            