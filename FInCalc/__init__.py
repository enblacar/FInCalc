# Imports.
from .utils import update_plot_layout, get_plotly_colors, display_palette_as_gradient
from .calculators import compound_interest, simple_interest
from .plot_compound_interest import plot_compound_interest
from .plot_simple_interest import plot_simple_interest

__all__ = ["update_plot_layout",
           "simple_interest",
           "compound_interest",
           "plot_compound_interest",
           "plot_simple_interest",
           "get_plotly_colors",
           "display_palette_as_gradient"]