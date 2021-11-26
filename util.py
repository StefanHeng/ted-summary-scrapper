from functools import reduce
from typing import TypeVar, Generic, Iterable
import json

T = TypeVar('T')


def get(dic, ks):
    """
    :param dic: Potentially multi-level dictionary
    :param ks: Potentially `.`-separated keys
    """
    ks = ks.split('.')
    return reduce(lambda acc, elm: acc[elm], ks, dic)


def config(attr):
    """
    Retrieves the queried attribute value from the config file.

    Loads the config file on first call.
    """
    if not hasattr(config, 'config'):
        # with open(f'{PATH_BASE}/{DIR_PROJ}/config.json') as f:
        with open('config.json') as f:
            config.config = json.load(f)
    return get(config.config, attr)


# def flatten(lst: list[list[T]]) -> list[T]:
# def flatten(lst: Iterable[Iterable[T]]) -> Iterable[T]:
def flatten(lst):
    """
    Flatten list of list into
    """
    return sum(lst, [])
