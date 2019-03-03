from bbapp.models import Batting, Fielding, Pitching, Player
from pathlib import Path

global_maps = {
    'playerID': 'player_id'
}

pitching_maps = {
    'IPouts': 'IPOuts'
}

batting_maps = {
    '2B': 'doubles',
    '3B': 'triples'
}

types_to_load = (Player, Batting, Pitching, Fielding)


def to_map(keys, vals):
    return {k: (v if v != '' else None) for k, v in zip(keys, vals)}


def load_from_directory(root):
    pt = Path(root)


def find_and_label_files(root):
    pt = Path(root)


def _get_fields_for_type(t):
    """Given a model type, return a list of the DB fields defined on it"""
    return [fn.name for fn in t._meta.get_fields()]


def _find_and_label_files(root):

    pt = Path(root)
