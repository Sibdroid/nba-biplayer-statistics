import docs
import utils
import parsing
from typing import List, Optional, Tuple
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np
import time
def draw_scatter_plot(ax: plt.Axes,
                      data: pd.DataFrame,
                      x_lim: List[float],
                      y_lim: List[float],
                      x_tick_amount: int,
                      y_tick_amount: int,
                      x_labels: List[str],
                      y_labels: List[str],
                      line_color: str,
                      line_style: str,
                      line_width: float,
                      dot_size: float,
                      line_coords: Tuple[List[float]]) -> plt.Axes:
    """Draws a scatter plot based on the data provided.

    Args:
        ax (plt.Axes): axes to be drawn on.
        data (pd.DataFrame): data to be drawn.
        lim (List[float]): limits of the plot.
        tick_amount (int): the amount of ticks of the legend.
        line_color (str): the color of the line dividing the plot.
        line_style (str): the style of the line.
        line_width (float): the width of the line.
        dot_size (float): the size of each dot.
        line_coords (Tuple[List[float]]): the coordinates of
        the line going through the plot.

    Returns:
        plt.Axes containing the drawn scatter plot.

    Raises:
        TypeError: if any of the arguments are of the wrong type.
        KeyError: if the data provided doesn't have "x", "y", "color"
        and "ecolor" columns.
        ValueError: if x_lim or y_lim provided consist of something
        other than floats or ints. 
    """
    types = ["matplotlib.pyplot.Axes", "pandas.DataFrame", "list", "list",
             "int", "int", "list", "list", "str", "str",
             ["int", "float"], ["int", "float"], "tuple"]
    docs.check_function_args(*docs.get_args(draw_scatter_plot, locals()), types)
    for i in x_lim:
        if not isinstance(i, int) and not isinstance(i, float):
            raise ValueError(f"X_lim has to be a list of ints or floats"
                             f"; {type(i)} is not allowed.")
    for i in y_lim:
        if not isinstance(i, int) and not isinstance(i, float):
            raise ValueError(f"X_lim has to be a list of ints or floats"
                             f"; {type(i)} is not allowed.")        
    ax.set_xlim(x_lim); ax.set_ylim(y_lim)    
    x_ticks = [int(i) for i in np.linspace(*x_lim, x_tick_amount)]
    y_ticks = [int(i) for i in np.linspace(*y_lim, y_tick_amount)]
    ax.set_xticks(x_ticks); ax.set_xticklabels(x_labels)
    ax.set_yticks(y_ticks); ax.set_yticklabels(y_labels)
    ax.plot(*line_coords, c = line_color,
            ls = line_style, lw = line_width)
    for i in ["top", "right", "bottom", "left"]:
        ax.spines[i].set_visible(False)
    ax.scatter(x = data["x"], y = data["y"], c = data["color"],
               s = dot_size, edgecolor = data["ecolor"])
    return ax
def draw_bar_plot(ax: plt.Axes,
                  colors: List[str],
                  percentages: List[float],
                  points: List[float],
                  bar_width: float,
                  keep_color: Optional[str] = None,
                  neutral_color: Optional[str] = None) -> plt.Axes:
    """Draws a vertical bar plot with data and colors provided.

    Args:
        ax (plt.Axes): axes to be drawn on.
        colors (List[str]): list of colors.
        percentages (List[float]): list of values to be plotted.
        points (List[float]): the list of x-coordinates to serve
        as anchor points.
        bar_width (float): the width of each bar.
        keep_color (Optional[str]): the only color to be left
        while the others are greyed out. If this and/or neutral_color
        are set to None, nothing will be greyed out.
        neutral_color: the color to use for greying out.
        If this and/or neutral_color are set to None, nothing
        will be greyed out.

    Returns:
        plt.Axes containing the drawn bar plot.

    Raises:
        TypeError: if any of the non-Optional arguments are of the
        wrong type.
        ValueError: if either of keep_color and neutral_color arguments
        cannot be interpreted as a color.
    """
    types = ["matplotlib.pyplot.Axes", ["list", "tuple"], ["list", "tuple"],
             ["list", "tuple"], "float"]
    docs.check_function_args(*docs.get_args(draw_bar_plot, locals()), types)
    conditions = [keep_color is not None,
                  neutral_color is not None]
    for color, percentage, point in zip(colors, percentages, [180, 190, 200, 210]):
        if all(conditions) and color == keep_color:
            color = keep_color
        elif all(conditions) and color != keep_color:
            color = neutral_color
        rectangle = patches.Rectangle((point, 0), bar_width, percentage * 1.8,
                                      linewidth = 1, facecolor = color)
        ax.add_patch(rectangle)
    return ax
def draw_final_plot(ax: plt.Axes,
                    ax_technical: plt.Axes,
                    percentages: Tuple[float],
                    df_tuples: Tuple[Tuple[pd.DataFrame]],
                    colors: Tuple[str],
                    keep_color: str) -> plt.Axes:
    """Draws two side-by-side plots based on the data provided:
    a scatter plot on the left and a bar plot on the right.

    Args:
        ax (plt.Axes): axes to be drawn on.
        ax_technical (plt.Axes): axes for technical purposes,
        currently only used to draw the right-sided ticks. 
        percentages (Tuple[float]): a list of percentages that
        will be represented by the bar plot.
        df_tuples (Tuple[Tuple[pd.DataFrame]]): a list
        of tuples, each containing two dfs generated by get_plotting_dfs().
        colors: (Tuple[str]): a list of colors.
        keep_color (str): the only color to be kept; all others are greyed out.

    Returns:
        plt.Axes containing the drawn plots.

    Raise:
        TypeError: if any arguments are of the wrong type.
        ValueError: if any of the percentages, df_tuples or colors
        are not precisely four elements wrong.
        ValueError: if either of colors or keep_color cannot be
        interpreted as a color.
    """
    types = ["matplotlib.pyplot.Axes", "matplotlib.pyplot.Axes",
             "tuple", "tuple", "tuple", "str"]
    docs.check_function_args(*docs.get_args(draw_final_plot, locals()), types)
    ticks = [f"{int(i)}" for i in np.linspace(0, 180, 19)]
    df_tuple = [i for i, j in zip(df_tuples, colors) if j == keep_color][0]
    draw_bar_plot(ax, colors, percentages, [180, 190, 200, 210], 8.9, 
                  keep_color, "#E0E0E0")
    for df in df_tuple:
        draw_scatter_plot(ax, df, [0, 220], [0, 180], 23, 19,
                          ticks + ([""] * 4), ticks, "#A3A3A3",
                          "--", 1.5, 5, ([0, 180], [0, 180]))
    for i in range(0, 230, 10):
        ax.vlines(i, 0, 180, lw = 0.15, colors = ["#A3A3A3"])
        if i <= 180:
            ax.hlines(i, 0, 180, lw = 0.15, colors = ["#A3A3A3"])
    ax_technical.set_yticks(np.linspace(0, 110, 11, False))
    ax_technical.set_yticklabels([f"{int(i)}%" for i in np.linspace(0, 110, 11, False)])
    for i in ["top", "right", "bottom", "left"]:
        ax_technical.spines[i].set_visible(False)
    return ax
def draw_gif(player_codes: Tuple[int],
             player_names: Tuple[str],
             team_code: str,
             years: str,
             duration: float) -> None:
    """Draws a gif made of four frames, each created by draw_final_plot().

    Args:
        player_codes: the codes of individual players, each represented as
        an integer (for example, 3975 for Stephen Curry).
        player_names: the names (or surnames) of individual plauer.
        team_code: three letter code of a team (for example, "gsw" for
        Golden State Warriors).
        years: the year(s) of the data. Can be provided in two ways:
        as a single year (for example, "2015") or as a range
        (for example, "2012-2016"). In the latter case,
        the data parsed will be merged into one. 
        duration: the time each frame is shown.

    Raises:
        TypeError: if any arguments are of the wrong type.
        ValueError: if an invalid url was formed with arguments
        provided.
    """
    types = ["tuple", "tuple", "str", "str", ["int", "float"]]
    docs.check_function_args(*docs.get_args(draw_gif, locals()), types)
    fig, ax = plt.subplots(figsize = (12.222, 10))
    ax_technical = ax.twinx()
    years = utils.years_to_list(years)
    if len(years) == 1:
        df = parsing.get_comparative_stats(player_codes, team_code, years[0],
                                           ("#EF798A", "#68C5DB"),
                                           "#ABA2E9", "#666666", "#666666")
    else:
        dfs = []
        for year in range(years[0], years[1] + 1):
            df = parsing.get_comparative_stats(player_codes, team_code, year,
                                           ("#EF798A", "#68C5DB"),
                                           "#ABA2E9", "#666666", "#666666")
            time.sleep(3)
            dfs += [df]
            print(f"{year} done")
        df = pd.concat(dfs)
        df = df.reset_index()
    colors = ["#EF798A", "#68C5DB", "#ABA2E9", "#666666"]
    (percentages, df_tuples,
     colors, text_ends) = parsing.get_final_data(df, colors, "#E0E0E0", player_names)
    results = ["best", "second-best", "second-worst", "worst"]
    file_names = []
    for color, text_end, result in zip(colors, text_ends, results):
        draw_final_plot(ax, ax_technical, percentages,
                        df_tuples, colors, color)
        team_name = utils.code_to_team_name(team_code)
        ax.set_title(f"{team_name} were {result} {text_end}", fontsize = 10)
        ax.set_xlabel(f"Points scored by {team_name}", loc = "left")
        ax.set_ylabel("Points scored by opponent team", loc = "bottom")
        plt.savefig(f"{color}.png")
        file_names += [f"{color}.png"]
        ax.clear()
        ax_technical.clear()
    utils.images_to_gif(file_names, f"{player_codes}-{team_code}-{years}.gif",
                        duration = duration)
       
    

    
    
