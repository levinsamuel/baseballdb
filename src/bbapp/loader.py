from bbapp.models import Batting, Fielding, Pitching, Player
from django.db.models.fields.related import ForeignKey
from pathlib import Path
from collections import deque
import logging

log = logging.getLogger('model_loader')
log.setLevel(logging.INFO)


def _get_fields_for_type(t):
    """Given a model type, return a list of the DB fields defined on it"""
    return {(fn.name + '_id' if isinstance(fn, ForeignKey) else fn.name)
            for fn in t._meta.fields}


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

    ttll = {t: list(vals) for t, vals in types_to_load.items()}
    # BFS through root dir
    pt = Path(root)
    fileq = deque([pt])
    while len(fileq) > 0:
        cur = fileq.popleft()
        for chld in cur.iterdir():
            if chld.is_dir():
                fileq.append(chld)
            elif chld.is_file():
                # If a file, read the header and check for a match with
                # existing model fields
                log.debug('Reading file: %s', chld)
                with open(chld, 'r') as f:
                    header = f.readline()
                log.debug('header: %s', header)
                hfields = [(global_maps[h] if h in global_maps else h)
                           for h in header.split(',')]

                for typ, maps in types_to_load.items():
                    # typ = model type, map = mapping from text header to model
                    # fields, fields = set of model fields
                    log.debug('maps: %s', maps)
                    map, fields = maps
                    log.debug('checking type for match: %s', typ)

                    # map read header to field names in model
                    hmapped = {(map[h] if h in map else h) for h in hfields}
                    # check how many fields are found in each type
                    ints = hmapped & fields
                    missing = (len(fields) - len(ints)) + \
                              (len(hmapped) - len(ints))
                    log.debug('''header for file %s is missing %d fields
                              for type %s''', chld.name, missing, typ)

                    try:
                        typfile, prevmissing = ttll[typ][2]
                        if prevmissing > missing:
                            log.debug('Better file match for type %s: %s',
                                      typ, chld.name)
                            ttll[typ][2] = (chld, missing)
                    except IndexError:
                        ttll[typ].append((chld, missing))

    return ttll


def _find_and_label_files(root, q):

    pt = Path(root)


def to_map(keys, vals):
    return {k: (v if v != '' else None) for k, v in zip(keys, vals)}


def load_from_directory(root):
    pt = Path(root)
