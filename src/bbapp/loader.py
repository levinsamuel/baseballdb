from bbapp.models import Batting, Fielding, Pitching, Player
from django.db.models.fields.related import ForeignKey
from pathlib import Path
from collections import deque
import logging

log = logging.getLogger('model_loader')
log.setLevel(logging.INFO)


def _get_fields_for_type(t):
    """Given a model type, return a list of the DB fields defined on it"""
    return [(fn.name + '_id' if isinstance(fn, ForeignKey) else fn.name)
            for fn in t._meta.fields]


global_maps = {
    'playerID': 'player_id'
}

types_to_load = {
    Player: [{}],
    Batting: [{
        '2B': 'doubles',
        '3B': 'triples'
    }],
    Pitching: [{
        'IPouts': 'IPOuts'
    }],
    Fielding: [{}]
}

for t in types_to_load.keys():
    types_to_load[t].append(_get_fields_for_type(t))


def find_and_label_files(root):

    ttll = dict(types_to_load)
    pt = Path(root)
    fileq = deque([pt])
    while len(fileq) > 0:
        cur = fileq.popleft()
        for chld in cur.iterdir():
            if chld.is_dir():
                fileq.append(chld)
            elif chld.is_file():
                log.debug('Reading file: %s', chld)
                with open(chld, 'r') as f:
                    header = f.readline()
                log.debug('header: %s', header)
                hfields = [(global_maps[h] if h in global_maps else h)
                           for h in header.split(',')]

                for typ, maps in types_to_load.items():
                    map, fields = maps
                    log.debug('checking type for match: %s', typ)
                    hmapped = set((map[h] if h in map else h) for h in hfields)
                    # TODO: check how many fields are found in each type


def _find_and_label_files(root, q):

    pt = Path(root)


def to_map(keys, vals):
    return {k: (v if v != '' else None) for k, v in zip(keys, vals)}


def load_from_directory(root):
    pt = Path(root)
