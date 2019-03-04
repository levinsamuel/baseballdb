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


# Global maps are overridden by type-specific maps
global_maps = {
    'playerID': 'player_id'
}

# The types to load:
# key: type
# value: list about the type mapping and file: [
#     item_0: map from header field to model field,
#     item_1: list of model fields, as read from the file,
#     item_2: tuple containing info about the matched file: [
#         item_0: the file that goes with this model,
#         item_1: the order of model fields in this file,
#         item_2: the number of missing fields
#     ]
# ]
types_to_load = {
    Player: [{
        'playerID': 'id',
    }],
    Batting: [{
        '2B': 'doubles',
        '3B': 'triples',
    }],
    Pitching: [{
        'IPouts': 'IPOuts',
    }],
    Fielding: [{
        'POS': 'Pos'
    }]
}

for t in types_to_load.keys():
    types_to_load[t].append(_get_fields_for_type(t))


def map_header_fields(f, local_map):
    if f in local_map:
        return local_map[f]
    elif f in global_maps:
        return global_maps[f]
    else:
        return f


def find_and_label_files(root, depth=4):
    """Given a root directory, search all subdirectories for files matching the
    model classes based on their headers"""
    ttll = {t: list(vals) for t, vals in types_to_load.items()}
    # BFS through root dir
    pt = Path(root)
    fileq = deque([(pt, 0)])
    while len(fileq) > 0:
        cur, lvl = fileq.popleft()
        for chld in cur.iterdir():
            if chld.is_dir() and lvl < depth:
                fileq.append((chld, lvl + 1))
            elif chld.is_file():

                # If a file, read the header and check for a match with
                # existing model fields
                comps = map_header_to_model(chld)

                # Check if the current file is a better match for the known
                # types
                for typ in types_to_load:
                    hmapped, missing = comps[typ]
                    try:
                        prevmissing = ttll[typ][2][2]
                        if prevmissing > missing:
                            log.debug('Better file match for type %s: %s',
                                      typ, chld.name)
                            ttll[typ][2] = (chld, hmapped, missing)
                    except IndexError:
                        ttll[typ].append((chld, hmapped, missing))

    return ttll


def map_header_to_model(data_file):

    log.debug('Reading file: %s', data_file)
    with open(data_file, 'r') as f:
        header = f.readline().strip()
    log.debug('header: %s', header)
    hfields = header.split(',')

    choice = {}
    for typ, maps in types_to_load.items():
        # typ = model type, map = mapping from text header to model
        # fields, fields = set of model fields
        map, fields = maps
        log.debug('checking type for match: %s', typ)

        # map read header to field names in model
        hmapped = [map_header_fields(h, map) for h in hfields]

        # check how many fields are found in each type
        headerset = set(hmapped)
        ints = headerset & fields
        missing = (len(fields) - len(ints)) + \
                  (len(headerset) - len(ints))
        log.debug('''header for file %s is missing %d fields
                  for type %s''', data_file.name, missing, typ)

        choice[typ] = (hmapped, missing)

    return choice


def to_map(keys, vals):
    """Attach the keys from the file header to the values. Both are assumed
    to be in the order read from the input file"""
    return {k: v for k, v in zip(keys, vals)
            if v is not None and v != ''}


def load_from_type_map(type_map):
    """Given a map containing the model fields and some associated data,
    including the file to load, load the files"""
    for typ, maps in type_map.items():
        file, header, _ = maps[2]
        with open(file, 'r') as reader:
            # header
            reader.readline()
            for line in reader:
                fmap = to_map(header, line.strip().split(','))
                obj = typ(**fmap)
                obj.save()


def load_from_directory(root, depth=4):
    """Find the files in a given root directory which correspond to the
    expected model fields, and then load those files into the DB"""
    ttll = find_and_label_files(root, depth)
    load_from_type_map(type_map)
