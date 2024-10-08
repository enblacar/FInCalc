import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.colors as pc
import plotly.graph_objects as go


# Function to generate color map
def generate_color_map(labels, palette):
    """
    Generate a color map for a given set of labels.

    :param labels: Unique labels to generate a color map for.
    :param palette: Color palette to use from plotly.
    """
    categories = labels.dropna().unique()
    return {category: palette[i % len(palette)] for i, category in enumerate(categories)}

# Function to apply common theming across plots.
def update_plot_layout(fig, type = None, fontsize = None, font_color = "black"):
    """
    Wrapper to update plotly plot themes automatically.

    :param fig: Plotly plot object.
    :param type: Type of plot: pie, heatmap.
    :param fontsize: Font size to apply generally.
    :param font_color: Font color to apply generally.
    """
    fig.update_layout(legend = dict(font = dict(size = fontsize),
                                    itemsizing = "constant"),
                      legend_title = dict(font = dict(size = fontsize)),
                      font = dict(size = fontsize, color = font_color),
                      plot_bgcolor = "white", 
                      paper_bgcolor = "white",
                      xaxis = dict(showline = True,
                                  ticks = "",
                                  tickfont = dict(size = fontsize, color = font_color),
                                  titlefont = dict(size = fontsize, color = font_color)),
                      yaxis = dict(showline = True,
                                  ticks = "",
                                  tickfont = dict(size = fontsize, color = font_color),
                                  titlefont = dict(size = fontsize, color = font_color)))  

    if type == "pie":
        fig.update_layout(margin = dict(l = 0, r = 0, t = 0, b = 0),
                          showlegend = False)
            
    return fig

def get_plotly_colors():
    # Create a dictionary of the colors for each color palette in plotly.
    qualitative_colors = {palette_name: getattr(px.colors.qualitative, palette_name)
                         for palette_name in dir(px.colors.qualitative)
                         if not palette_name.startswith("_") and isinstance(getattr(px.colors.qualitative, palette_name), list)}

    sequential_colors = {palette_name: getattr(px.colors.sequential, palette_name)
                        for palette_name in dir(px.colors.sequential)
                        if not palette_name.startswith("_") and isinstance(getattr(px.colors.sequential, palette_name), list)}
    
    diverging_colors = {palette_name: getattr(px.colors.diverging, palette_name)
                        for palette_name in dir(px.colors.diverging)
                        if not palette_name.startswith("_") and isinstance(getattr(px.colors.diverging, palette_name), list)}
    
    return qualitative_colors, sequential_colors, diverging_colors

def display_palette_as_gradient(palette, continuous = True, num_colors = 100):
    # Create a continuous color scale based on the selected qualitative palette
    color_scale = pc.make_colorscale(palette)
    if continuous:
        colors_use = pc.sample_colorscale(color_scale, [i/(num_colors-1) for i in range(num_colors)], colortype='rgb')
    else:
        colors_use = palette

    # Prepare an HTML string to render the color scale as a single line of div elements
    color_boxes = ''.join(
        f'<div style="background-color:{color}; height:50px; width:100%; flex:1; margin:0; padding:0;"></div>'
        for color in colors_use
    )

    # Display the color scale as a single horizontal line
    st.write(f'<div style="display:flex; width:100%;">{color_boxes}</div>', unsafe_allow_html=True)
    
def format_number(num):
    """
    Format a number to include a suffix based on its magnitude.
    
    :param num: The number to format.
    :return: A string representation of the number with a suffix.
    """
    num = float(num)
    if abs(num) >= 1_000_000_000_000:
        return f"{num / 1_000_000_000_000:.2f}T"
    elif abs(num) >= 1_000_000_000:
        return f"{num / 1_000_000_000:.2f}B"
    elif abs(num) >= 1_000_000:
        return f"{num / 1_000_000:.2f}M"
    elif abs(num) >= 1_000:
        return f"{num / 1_000:.2f}K"
    else:
        return f"{num:.2f}"
    

def donut_plot(data, discrete_palette, fontsize):

    p = go.Pie(labels = data["Type"],
               values = data["Total"],
               hole = 0.75,
               textinfo= "none", 
               hoverinfo = "label + percent + value",
               title = "Investments",
               customdata = ["Type", "Value"],
               marker = dict(colors = discrete_palette,
                             line = dict(color = "white", 
                                         width = 1.5)),
               hovertemplate = '<b>%{label}:</b> %{value:,.2f} €'+
                                    '<extra></extra>',)  
    
    p = go.Figure(p)

    p = update_plot_layout(fig = p, type = "pie", fontsize = fontsize)
    
    return p