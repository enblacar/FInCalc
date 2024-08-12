from FInCalc import *
import streamlit as st

def main():
    discrete_palette = st.session_state.discrete_palette
    fontsize = st.session_state.fontsize
    with st.expander("**Calculator inputs**", expanded = True):
        col1, col2, col3, col4 = st.columns(4, vertical_alignment = "center")
        with col1: 
            principal = st.number_input("Initial investment (€)", min_value = 0, value = None, step = 50, placeholder = "1500", help = "Amount in Euros")
        with col2: 
            years = st.number_input("Years", min_value = 1, value = None, placeholder = "35", help = "Time horizon")
        with col3:
            annual_rate = st.number_input("Annual Growth Rate (%)", min_value = 0.00, value = None, step = 0.01, placeholder = "5.0", help = "Expected annual growth rate")
        with col4:

            inflation = st.toggle("Account for inflation?", help = "This substracts an average 2% inflation to the annual rate provided.")
            
            log_y = st.toggle("Log scale?", help = "Log 10 scale the Y axis.")
            
        variables_check = [principal, years, annual_rate]
        
    if all(x is not None for x in variables_check):
        amount = simple_interest(principal = principal, 
                                 annual_rate = annual_rate, 
                                 years = years, 
                                 inflation = inflation)
        
        p = plot_simple_interest(data = amount, discrete_palette = discrete_palette, log_y = log_y, fontsize = fontsize)
        
        st.plotly_chart(p, use_container_width=True)
    else:
        st.info('Please fill the **empty input fields**. Once done, the plot will **update automatically** every time you **modify** a value.', icon="🔜")

if __name__ == "__page__":
    main()
            