from FInCalc import *
import streamlit as st
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
import pandas as pd

def main():
    # Inject CSS
    st.markdown(
        """
        <style>
        /* Remove top and bottom padding */
        .css-18e3th9 {
            padding-top: 0rem;
            padding-bottom: 0rem;
        }
        
        /* Remove padding between elements */
        .stMarkdown {
            margin-top: 0.5rem;
            margin-bottom: 0.5rem;
        }

        /* Adjust padding for specific sections if needed */
        div[data-testid="stBlock"] {
            padding-top: 0rem;
            padding-bottom: 0rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    discrete_palette = st.session_state.discrete_palette
    fontsize = st.session_state.fontsize
    with st.expander("**Calculator inputs**", expanded = True):
        col1, col2, col3, col4 = st.columns(4, vertical_alignment = "center")
        with col1: 
            principal = st.number_input("Initial investment (€)", min_value = 0, value = None, step = 50, placeholder = "1500", help = "Amount in Euros")
            contribution = st.number_input("Contribution (€)", min_value = 0, value = None, step = 50, placeholder = "100", help = "Recurrent contribution")
        with col2: 
            times_compounded = st.number_input("Times compounded", min_value = 1, value = None, placeholder = "12", help = "How many times the interest compounds")
            years = st.number_input("Years", min_value = 1, value = None, placeholder = "35", help = "Time horizon")
        with col3:
            annual_rate = st.number_input("Annual Growth Rate (%)", min_value = 0.00, value = None, step = 0.01, placeholder = "5.0", help = "Expected annual growth rate")
            ter = st.number_input("TER (%)", min_value = 0.00, value = 0.00, step = 0.01, placeholder = "0.22", help = "Total Expense Ratio, from a given ETF. Use 0 otherwise.")
        with col4:

            inflation = st.toggle("Account for inflation?", help = "This substracts an average 2% inflation to the annual rate provided.")
            
            log_y = st.toggle("Log scale?", help = "Log 10 scale the Y axis.")
            
        variables_check = [principal, contribution, times_compounded, years, annual_rate, ter]
        
    if all(x is not None for x in variables_check):
        amount = compound_interest(principal = principal, 
                                   annual_rate = annual_rate, 
                                   times_compounded = times_compounded, 
                                   years = years, 
                                   contribution = contribution,
                                   ter = ter, 
                                   inflation = inflation)        
        
        p, p2 = plot_compound_interest(data = amount, discrete_palette = discrete_palette, log_y = log_y, fontsize = fontsize)
        
        with st.container():
            col1, col2, col3 = st.columns([1, 1, 1], vertical_alignment = "center")
            with col1: 
                st.metric("Initial Investment", f"{format_number(principal)} €")
                st.metric("Periodical contributions", f"{format_number(contribution * times_compounded * years)} €")
            with col2: 
                st.metric("Interest earned", f"{format_number(amount['Interest'].values.tolist()[-1])} €")
                st.metric("Total earned", f"{format_number(amount['Total Show'].values.tolist()[-1])} €")
            style_metric_cards(border_left_color = "black", box_shadow = False)

            with col3: 
                st.plotly_chart(p2, use_container_width=True)
            st.plotly_chart(p, use_container_width=True)


    else:
        st.info('Please fill the **empty input fields**. Once done, the plot will **update automatically** every time you **modify** a value.', icon="🔜")

if __name__ == "__page__":
    main()
            