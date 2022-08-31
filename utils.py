import docs
import parsing
from typing import *
from typing import T
import pandas as pd
import re
import imageio
import os
def has_special_chars(string: str) -> bool:
    """Checks whether a string has any special characters

    Args:
        string (str): string to be checked.

    Returns:
        A bool.
    """
    return not bool(re.match('^[a-zA-Z0-9]*$', str(string)))
def score_to_tuple(score: str) -> Optional[List[int]]:
    """Transforms a score from a string to a list.

    Args:
        score (str): score represented as a string. Expected to look like
        "W131-118" (the team won 131-118), "L112-109" (the team lost 109-112)
        or "W123-120 OT" (the team won 123-120 in OT). If it doesn't fit this
        format, the function will return None.

    Returns:
        any None (if the score doesn't fit the format) or a list of two
        integers. If a team won, the first integer will be larger, otherwise,
        the second one will be larger.

    Raises:
        TypeError: if score isn't a string.
    """
    if not isinstance(score, str):
        raise TypeError(f"Score has to be a string, not {type(score)}.")
    if not all([i in "0123456789-WLOT " for i in score]):
        return None
    numbers = [int(i) for i in re.findall(r"\d+", score)][:2]
    if "W" in score:
        return numbers
    return numbers[::-1]
def date_convert(date: str) -> str:
    """Converts date from one string format to another.

    Args:
        date (str): date represented as a string. Expected to look like
        "Sun 6/5" or "Sat 5/7".
    Returns:
        A date represented as a string that looks like "Sun, Jun 5"
        or "Sat, May 7".

    Raises:
        TypeError: if date isn't a string.
        IndexError: if a month wasn't found (that is, wrong format).
        KeyError: if a date wasn't found (same, wrong format).
    """
    if not isinstance(date, str):
        raise TypeError(f"Date has to be a string, not {type(date)}.")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    number_to_month = {i+1: f", {j} " for i, j in enumerate(months)}
    try:
        month_number = [int(i) for i in re.findall(r"\d+", date)][0]
    except IndexError:
        raise IndexError("Wrong format: month number not found.")
    try:
        date = date.replace(f"{month_number}", number_to_month[month_number], 1)
    except KeyError:
        raise KeyError("Wrong format: day not found.")
    date = date.replace(" ", "", 1).replace("/", "")
    return date
def row_in_df(row: pd.Series,
              df: pd.DataFrame) -> bool:
    """Checks if a row is in a df.

    Args:
        row (pd.Series): row to be checked.
        df (pd.DataFrame): df.

    Returns:
        A boolean.

    Raises:
        TypeError: if row isn't a Series or df isn't a DataFrame.
    """
    types = ["pandas.Series", "pandas.DataFrame"]
    docs.check_function_args(*docs.get_args(row_in_df, locals()), types)
    if not isinstance(row, pd.Series):
        raise TypeError(f"Row has to be a pd.Series, not a {type(row)}.")
    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"Df has to be a pd.DataFrame, not a {type(df)}.")
    return (df == row).all(1).any()
def keep_row_if_in_df(df: pd.DataFrame,
                      row_original: pd.Series,
                      row_changed: pd.Series) -> pd.Series:
    """Checks if a row is in a df, returns another row if true,
    returns empty row if false.

    Args:
        df (pd.DataFrame): df.
        row_original: row to be checked.
        row_changed: row to be returned if row_original is in df.

    Returns:
        any row_changed or an empty pd.Series.

    Raises:
        TypeError: if any of the arguments is of the wrong type.
    """
    types = ["pandas.DataFrame", "pandas.Series", "pandas.Series"]
    docs.check_function_args(*docs.get_args(keep_row_if_in_df, locals()), types)
    if row_in_df(row_changed, df):
        return row_original
    # dtype doesn't matter since it's deleted any way
    # but pandas throws a warning if it's omitted
    return pd.Series([], dtype = "float64")
def split_list(list_: List[T],
               length: int) -> List[List[T]]:
    """Divides the list into a chunks of set length

    Args:
        list_ (List[T]): a list to be divided.
        length (int): the length of each chunk.

    Returns:
        A divided list, represented in a nested way. If there is no
        way for each chunk to be of set size (for example, calling
        split_list([1, 2, 3, 4, 5], 2)), the last chunk will be shorter.

    Raises:
        TypeError: if any of the arguments is of the wrong type.
        ValueError: if length argument cannot be interpreted properly
        (for example, if 0.5 or 0 is given).
    """
    types = ["list", "int"]
    docs.check_function_args(*docs.get_args(split_list, locals()), types)
    return [list_[i:i+length] for i in range(0, len(list_), length)]
def flatten_list(list_: List[List[T]]) -> List[T]:
    """Flattens a nested list.

    Args:
        list_ (List[List[T]]): a nested list.

    Returns:
        A flattened list.

    Raises:
        TypeError: if list_ is something other than a list.
        TypeError: if list_ cannot be interpreted as a nested list.
    """
    if not isinstance(list_, list):
        raise TypeError(f"list_ has to be a list, not a {type(list_)}")
    for i in list_:
        if not isinstance(i, list):
            raise TypeError(f"list_ has to be a list of lists, "
                            f"{type(i)} is not a list")
    return [j for i in list_ for j in i]
def get_wins_percentage(df: pd.DataFrame,
                        precision: int) -> float:
    """Gets the percentage of wins from a df storing records.

    Args:
        df (pd.DataFrame): df.
        precision (int): a value representing the precision of rounding.
         
    Returns:
        A float representing the percentage of wins. 

    Raises:
        IndexError: if df is something other than a pd.DataFrame.
        KeyError: if df has no "x" or "y" columns.
    """
    types = ["pandas.DataFrame", "int"]
    docs.check_function_args(*docs.get_args(get_wins_percentage,
                                            locals()), types)
    try:
        return round(len(df[df.x < df.y]) / len(df) * 100, precision)
    except ZeroDivisionError:
        return 0
def sort_as_one(*args: TypeVar("T"),
                reverse: bool) -> Iterator[TypeVar("T")]: 
    """Sorts an arbitrary amount of iterables as one iterable.

    Args:
        *args: the iterables.

    Returns:
        A zip object containing sorted iterables.

    Raises:
        TypeError: if either of the iterables provided cannot be
        interpreted as an iterable.
        TypeError: if reverse argument cannot be interpeted properly.
    """
    return zip(*sorted(zip(*args), reverse = reverse))
def years_to_list(years: str) -> List[int]:
    """Converts the years provided to draw_gif() function to a list
    of years.

    Args:
        years (str): the years provided. Can be singular ("2015")
        or multiple ("2012-2016").

    Returns:
        A list of years, each represented as an int.

    Raises:
        TypeError: if years argument is not a string.
    """
    if not isinstance(years, str):
        raise TypeError(f"years has to be a str, not a {type(years)}")
    return [int(i) for i in re.findall(r"\d+", years)]
def code_to_team_name(code: str) -> str:
    """Returns a team name based on a three-letter code.

    Args:
        code: the three-letter code (like "gsw" or "phx")

    Returns:
        A team name (like Warriors or Suns).

    Raises:
        KeyError: if the code cannot be converted to a team name.
    """
    codes = {"atl": "Hawks",
             "bkn": "Nets",
             "bos": "Celtics",
             "cha": "Hornets",
             "chi": "Bulls",
             "cle": "Cavaliers",
             "dal": "Mavericks",
             "den": "Nuggets",
             "det": "Pistons",
             "gsw": "Warriors",
             "hou": "Rockets",
             "ind": "Pacers",
             "lac": "Clippers",
             "lal": "Lakers",
             "mem": "Grizzies",
             "mia": "Heat",
             "mil": "Bucks",
             "min": "Timberwolves",
             "nop": "Pelicans",
             "nyk": "Knicks",
             "okc": "Thunder",
             "orl": "Magic",
             "phi": "76ers",
             "phx": "Suns",
             "por": "Blazers",
             "sac": "Kings",
             "sas": "Spurs",
             "tor": "Raptors",
             "uta": "Jazz",
             "wsh": "Wizards"}
    return codes[code]
def images_to_gif(image_names: List[str],
                  gif_name: str,
                  duration: float,
                  delete_images: bool = True) -> None:
    """Creates a gif from a list of images.

    Args:
        image_names (List[str]): a list of image names.
        gif_name: the name of the resulting gif.
        duration: the time each frame of the resulting gif is shown.
        delete_images (bool): whether to delete the original images.
        Set to True by default.
    Raises:
        TypeError: if any of the arguments are of the wrong type.
        ValueError: if any of the image_names cannot be interpreted
        as a valid file name.
        ValueError: if gif_name cannot be interpreted as a valid
        file name.
        OverflowError: if negative duration was provided.
        FileNotFoundError: if any of the image_names does not exist
        as a file.
    """
    types = ["list", "str", ["int", "float"], "bool"]
    docs.check_function_args(*docs.get_args(images_to_gif, locals()), types)
    image_names_interpreted = [imageio.imread(i) for i in image_names]
    imageio.mimsave(gif_name, image_names_interpreted, duration = duration)
    if delete_images:
        for i in image_names:
            os.remove(i)        
