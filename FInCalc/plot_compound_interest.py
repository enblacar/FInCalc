from .utils import *

def plot_compound_interest(data, discrete_palette, log_y, fontsize, currency_use):
    """
    Plot the compound interest as a stacked bar plot using Plotly.

    :param data: DataFrame containing the future value data.
    :param discrete_palette: Discrete color palette to use. 
    :param log_y: Whether to log10 scale the Y axis. 
    :param fontsize: Font size to use in the plot.
    :param currency_use: Whether to use Euro or Dollar.
    """

    # Turn wide data to long data.
    data_long = pd.melt(data.loc[:, ["Year", "Initial Investment", "Contributions", "Interest", "Total"]],
                        id_vars = "Year",
                        var_name = "Type",
                        value_name = "Amount")
    
    # Calculate the total amount per Year
    totals = data_long.groupby("Year")["Amount"].sum().reset_index()
    totals.rename(columns = {"Amount": "Total"}, inplace = True)
    

    # Merge the total amounts back into the original DataFrame
    data_long = data_long.merge(totals, on = "Year")
    color_map = generate_color_map(data_long["Type"], discrete_palette)
    color_map["Total"] = "white"

    p = px.bar(data_frame = data_long,
               x = "Year",
               y = "Amount",
               color = "Type",
               text_auto = False,
               title = None,
               color_discrete_map = color_map,
               custom_data = ["Type", "Total"],
               log_y = log_y) 
    

    p.update_traces(marker = dict(line = dict(color = "white", width = 1)),
                    hovertemplate = f"<b>%{{customdata[0]}}:</b> %{{y:,.2f}} {currency_use}" +
                                     "<extra></extra>")
    

    # Surgically insert things in the hover :D.
    p.data[3].update(customdata = data_long.loc[:, ["Year", "Total"]],
                     hovertemplate = f"<b>Total:</b> %{{customdata[1]:,.2f}} {currency_use}" +
                                     "<extra></extra>",
                     showlegend =  False,
                     marker = dict(line = dict(color = "white", width = 1)))

    # Update layout
    p.update_layout(xaxis_title = "Year",
                    yaxis_title = f"Total ({currency_use})",
                    legend_title = "",
                    bargap = 0.2,
                    hovermode = "x unified",
                    hoverlabel = dict(bgcolor="white", font_size = fontsize),
                    margin = dict(l = 0, r = 0, t = 0, b = 0),
                    legend = dict(x = 0.5, y = 1.1, xanchor = "center", yanchor = "top", orientation = "h"))

    p = update_plot_layout(fig = p, type = "bar", fontsize = fontsize)

    totals = data_long[data_long["Year"] == max(data_long["Year"])].groupby("Type")["Amount"].sum().reset_index()
    totals.rename(columns = {"Amount": "Total"}, inplace = True)
    p2 = donut_plot(totals, discrete_palette = discrete_palette, fontsize = fontsize, currency_use = currency_use)
    

    return(p, p2)