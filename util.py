from functools import reduce
import json


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

