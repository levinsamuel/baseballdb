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


def to_map(keys, vals):
    return {k: (v if v != '' else None) for k, v in zip(keys, vals)}


def load_from_directory(root):
    pt = Path(root)
