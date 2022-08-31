from typing import Callable, Tuple, List, Union, T
import inspect
import pydoc
def get_args(function: Callable,
             locals_: dict) -> Tuple[List[T], List[str]]:
    """Returns names and values of function's args.

    Args:
        function (Callable): the function.

    Returns:
        A tuple of two lists: the first one contains the values
        of the arguments, the second one contains their names.

    Raises:
        TypeError: if anything other than a function is entered
        for function argument or if locals_ isn't a dictionary.
        KeyError: if locals_ doesn't contain any of the
        function's arguments (really unlikely and basically impossible,
        but could be theoretically caused by wrong locals_ being provided).
    """
    if not inspect.isfunction(function) and not inspect.isbuiltin(function):
        raise TypeError(f"Function has to be a user-defined or built-in"
                        f", not {type(function)}"
                        )
    arg_names = inspect.getfullargspec(function)._asdict()["args"]
    for name in arg_names:
        if name not in locals_.keys():
            raise KeyError(f"Provided locals don't have an argument {name}")
    return [locals_[i] for i in arg_names], arg_names
def check_if_type(object_: T, type_: Union[str, List[str]],
                  object_name: str) -> None:
    """Checks if the object fits the type(s), raises an error if not.

    Args:
        object_ (T): object to be checked.
        type_ (str or List[str]): type(s) to be checked against.

    Returns:
        None.

    Raises:
        TypeError: if type_ is not a str or a list of strs or
        if an object_name isn't a str. 
        TypeError: if the object doesn't fit any of the types.
        ValueError: if type_ contains an invalid class name.
    """
    if not isinstance(type_, str) and not isinstance(type_, list):
        raise TypeError(f"Type_ has to be a str or a list of strs, not a {type(type_)}")
    if not isinstance(object_name, str):
        raise TypeError(f"Object_name has to be a str, not a {type(object_name)}")
    if isinstance(type_, list) and any([not isinstance(i, str) for i in type_]):
        raise TypeError(f"If type_ is a list, it has to be a list of strs")
    if isinstance(type_, str):
        if pydoc.locate(type_) is None:
            raise ValueError(f"{type_} is not a valid name for a class.")
        if not isinstance(object_, pydoc.locate(type_)):
            raise TypeError(f"{object_name} has to be a {type_}, not a {type(object_)}")
    else:
        for i in type_:
            if pydoc.locate(i) is None:
                raise ValueError(f"{i} is not a valid name for a class.")
        if not any([isinstance(object_, pydoc.locate(i)) for i in type_]):
            raise TypeError(f"{object_name} has to be one of the following: {', '.join(type_)}"
                            f", not a {type(object_)}."
                            )
def check_function_args(values: List[T],
                        arguments: List[str],
                        types: List[Union[List[str], str]]) -> None:
    """Checks if the values of the arguments fit their respective types,
    raises a TypeError if at least one doesn't.

    Args:
        values (List[T]): values to be checked.
        arguments (List[str]): names of the arguments.
        types (List[Union[List[str], str]]): types to be checked against.
        
    Raises:
        TypeError: if any of the values doesn't fit its
        respective type.
        ValueError: if any of the types is invalid.
    """
    for value, type_, arg in zip(values, types, arguments):
        check_if_type(value, type_, arg)
    
