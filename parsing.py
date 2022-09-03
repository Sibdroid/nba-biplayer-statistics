import utils
import docs
from typing import List, Union, Tuple, Iterator, TypeVar
from pydoc import locate
import pandas as pd
import time
def get_stats(team_or_code: Union[str, int], year: int) -> pd.DataFrame:
    """Fetches game statistics from espn.com and processes them.

    Args:
        team_or_code (Union[str, int]): controls what kind of statistics
        the function is going to fetch. If a string is given
        (for example, "gsw" for Golden State Warriors or "lal" for
        Los Angeles Lakers), team data will be fetched. If an int is given
        (for example, 1966 for LeBron James), individual player data will be
        fetched.
        year (int): determines the year of the statistics.

    Returns:
        A df with the processed statistics. If player statistics was
        requested, the data will have four columns: x, y, date and score.
        Otherwise, it will have three: x, y and date. X, y and score
        are positive integers, while data is a string (for example,
        "Sun, Jun 5"). Score isn't technically necessary and
        is removed later on, in get_comparative_stats(),
        but it might be important, so it's best to keep it.

    Raises:
        TypeError: if either of the arguments is of the wrong type.
        ValueError: if an invalid url was formed with the argument(s)
        entered.
    """
    types = [["str", "int"], "int"]
    docs.check_function_args(*docs.get_args(get_stats, locals()), types)
    if utils.has_special_chars(team_or_code) or utils.has_special_chars(year):
        raise ValueError("Invalid argument(s) entered, statistics not recognized.")
    try: 
        if isinstance(team_or_code, str):
            url = (f"https://www.espn.com/nba/team/schedule/_/name/"
                   f"{team_or_code}/season/{year}/seasontype/2")
            data = pd.read_html(url, header = 0)[0]
            columns = ["DATE", "RESULT"]
        else:
            url = (f"https://www.espn.com/nba/player/gamelog/_/id/"
                   f"{team_or_code}/type/nba/year/{year}")
            data = pd.read_html(url, header = 0)
            data = pd.concat(data, axis = 0)
            columns = ["Date", "Result", "PTS"]
    except ValueError:
        raise ValueError("Invalid argument(s) entered, statistics not recognized.")
    data = data[columns]
    data = data.dropna(axis = 0)
    data[columns[1]] = data[columns[1]].apply(lambda x: utils.score_to_tuple(x))
    data = data.dropna(axis = 0)
    data = data[data[columns[1]].map(lambda x: len(x) != 0)]
    for i, name in enumerate("xy"):
        data[name] = [j[1-i] for j in data[columns[1]]]
    if isinstance(team_or_code, str):
        data["date"] = data[columns[0]]
    else:
        data["date"] = data[columns[0]].apply(lambda x: utils.date_convert(x))
        data["score"] = data[columns[-1]].apply(lambda x: int(x))
    for i in columns:
        data = data.drop(i, axis = 1)
    return data
def in_dfs_to_color(df: pd.DataFrame,
                    dfs_compare: Union[List[pd.DataFrame],
                                       Tuple[pd.DataFrame, pd.DataFrame]],
                    player_colors: Union[List[str], Tuple[str, str]],
                    both_color: str,
                    neutral_color: str,
                    neutral_ecolor: str) -> pd.DataFrame:
    """Compares two player dfs with team df and sets colors according
    to their participation. If neither participated in a game,
    neutral_color and neutral_ecolor are set, if one of them
    participated, that player's color is set (given by player_colors),
    and if both participated, both_color is set.

    Args:
        df (pd.DataFrame): a df containing the team's results for that year.
        dfs_compare (Union[List[pd.DataFrame], Tuple[pd.DataFrame, pd.DataFrame]]):
        two dfs, each containing individual player's game results.
        player_colors (Union[List[str], Tuple[str, str]]): two colors linked to
        players, each given as a string (for example, "#EF798A").
        both_color (str): color used when both players participated.
        neutral_color (str): color used when neither did.
        neutral_ecolor (str): ecolor (edgecolor) used when neither did.
        
    Returns:
        A df containing the team's results for that year,
        with "color" and "ecolor" columns clarifying player participation.

    Raises:
        TypeError: if either of the arguments is of the wrong type.
    """
    types = ["pandas.DataFrame", ["list", "tuple"], ["list", "tuple"],
             "str", "str", "str"]
    docs.check_function_args(*docs.get_args(in_dfs_to_color, locals()), types)
    if any([not isinstance(i, pd.DataFrame) for i in dfs_compare]):
        raise TypeError(f"Dfs_compare has to be a list of dfs; {type(i)} is not allowed.")
    if any([not isinstance(i, str) for i in player_colors]):
        raise TypeError(f"Player_colors has to be a list of strs; {type(i)} is not allowed.")
    dict_colors = {(False, False): neutral_color,
                   (True, False): player_colors[0],
                   (False, True): player_colors[1],
                   (True, True): both_color}
    df["color"] = df.apply(lambda row: (utils.row_in_df(row, dfs_compare[0]),
                                        utils.row_in_df(row, dfs_compare[1])),
                           axis = 1)
    df["color"] = df["color"].apply(lambda x: dict_colors[x])
    ecolors = df["color"].apply(lambda x: x if x != neutral_color else neutral_ecolor) 
    df["ecolor"] = ecolors
    return df
def get_comparative_stats(players: Tuple[int, int],
                          team: str,
                          year: int,
                          player_colors: Tuple[str, str],
                          both_color: str,
                          neutral_color: str,
                          neutral_ecolor: str) -> pd.DataFrame:
    """Gathers data for individual players as well as their team,
    then keeps only regular season results and turns all the possible
    values to integers, then sets the colors using in_dfs_to_color().
    
    Args:
        players (Tuple[int, int]): a tuple containing individual player codes
        (same as in the get_stats().
        team (str): individual team code.
        year (int): season, given as the second year (for example,
        2020 stands for 2019-20 season).
        player_colors: same as in_dfs_to_color().
        both_color: same as above.
        neutral_color: same as above.
        neutral_ecolor: same as above.

    Returns:
        A df with ready, processed, clean statistics. Contains five columns: 
        x, y, date, color and ecolor. X and y are integers, date, color
        and ecolor are strings (for example, "Tue, Oct 19", "#EF798A" and
        "#EF798A" respectively).

    Raises:
        TypeError: if any of the arguments is not of their respective type.
        ValueError: if an invalid url was formed with the argument(s)
        entered.
    """
    types = ["tuple", "str", "int", "tuple", "str", "str", "str"]
    docs.check_function_args(*docs.get_args(get_comparative_stats, locals()), types)
    for i in players:
        if not isinstance(i, int):
            raise TypeError(f"Players has to be a tuple of ints; {type(i)} is not allowed.")
    for i in player_colors:
        if not isinstance(i, str):
            raise TypeError(f"Player_colors has to be a tuple of strs; {type(i)} is not allowed.")
    df_players = [get_stats(player, year) for player in players
                  if time.sleep(3) == None]
    df_team = get_stats(team, year)
    df_players = [df_player.apply(lambda x: utils.keep_row_if_in_df(df_team, x, x[:-1]),
                                  axis = 1).dropna(axis = 0) for df_player in df_players]
    df_players = [i.drop("score", axis = 1) for i in df_players]
    df_players = [i.apply(pd.to_numeric, errors = "ignore")
                  for i in df_players]
    df_team = in_dfs_to_color(df_team, df_players, player_colors,
                              both_color, neutral_color, neutral_ecolor)
    return df_team    
def get_plotting_dfs(df: pd.DataFrame,
                     color: str,
                     neutral_color: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Replaces "color" and "ecolor" with requested neutral_color if they
    don't fit the requested color.

    Args:
        df (pd.DataFrame): a df obtained from get_comparative_stats().
        color (str): color that you want to be kept.
        neutral_color (str): color that you want to replace all
        values that don't fit.

    Returns:
        Two dfs, first one with only neutral color, second one only
        with requested color (for example, #EF798A),
    Raises:
        TypeError: if any of the arguments is not of their respective type.
        KeyError: if a "color" or "ecolor" column is missing from the df. 
    """
    types = ["pandas.DataFrame", "str", "str"]
    docs.check_function_args(*docs.get_args(get_plotting_dfs, locals()), types)
    color_criteria = df["color"] == color
    df_color_yes, df_color_no = df[color_criteria], df[~color_criteria]
    # used to prevent SettingWithCopyWarning
    pd.options.mode.chained_assignment = None
    df_color_no["color"] = df["color"].apply(lambda x: neutral_color)
    df_color_no["ecolor"] = df["ecolor"].apply(lambda x: neutral_color)
    return df_color_no, df_color_yes
def get_final_data(df: pd.DataFrame,
                   colors: List[str],
                   neutral_color: str,
                   player_names: Tuple[str]) -> Iterator[TypeVar("T")]:
    """Creates data for visualization based on df created by
    get_comparative_stats() and a list of four colors.

    Args:
        df (pd.DataFrame): a df created by get_comparative_stats().
        colors (List[str]): a list with four colors, representing categories
        of games: two for games where either of the players played,
        one for games where they both played, and one for games where
        neither played.
        player_names: the names of individual players.

    Returns:
        A zip object containing three objects:
        * a list of win ratios of each category,
        represented as floats.
        * a list of tuples, each containing two DataFrames:
        one containing only games with the set color, second one only
        with the neutral color.
        * a list of colors, individual elements identical to those
        of the colors provided.
        All three are sorted using the first one as key.

    Raises:
        TypeError: if any of the arguments is of the wrong type.
        ValueError: if any of the colors provided cannot be interpreted
        as a color.
    """
    types = ["pandas.DataFrame", "list", "str", "tuple"]
    docs.check_function_args(*docs.get_args(get_final_data,
                                            locals()), types)    
    df_tuples = [get_plotting_dfs(df, color, neutral_color)
                 for color in colors]
    percentages = [utils.get_wins_percentage(df[df["color"] == color], 2)
                   for color in colors]
    text_ends = [f"with {player_names[0]} and no {player_names[1]}",
                 f"with {player_names[1]} and no {player_names[0]}",
                 f"with both {player_names[0]} and {player_names[1]}",
                 f"with neither {player_names[0]} and {player_names[1]}"]
    return utils.sort_as_one(percentages, df_tuples,
                             colors, text_ends, reverse = True)
