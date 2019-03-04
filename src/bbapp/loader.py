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


class Mapping:

    def __init__(self, typ, mapping):
        self.typ = typ
        self.mapping = mapping
        self.fields = _get_fields_for_type(typ)
        self.file = None
        self.missing = None
        self.headerList = None

    def __repr__(self):
        return f'mapping for type: {self.typ}'

    def copy(self):
        cop = Mapping(self.typ, {**self.mapping})
        return cop


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
all_types = [
    Mapping(Player, {
        'playerID': 'id',
    }),
    Mapping(Batting, {
        '2B': 'doubles',
        '3B': 'triples',
    }),
    Mapping(Pitching, {
        'IPouts': 'IPOuts',
    }),
    Mapping(Fielding, {
        'POS': 'Pos'
    })
]


def map_header_fields(f, local_map):
    if f in local_map:
        return local_map[f]
    elif f in global_maps:
        return global_maps[f]
    else:
        return f


def find_and_label_files(root, to_load_input=all_types, depth=4,
                         allowed_suffixes=['txt', 'csv', 'dat']):
    """Given a root directory, search all subdirectories for files matching the
    model classes based on their headers"""
    if to_load_input is None or len(to_load_input) == 0:
        return None
    elif isinstance(to_load_input[0], Mapping):
        to_load = [m.copy() for m in to_load_input]
    elif isinstance(to_load_input[0], type):
        to_load = [m.copy() for m in all_types if m.typ in to_load_input]
    else:
        raise TypeError(f'Not sure what to do with this: {to_load_input}')

    _allowedsfx = set([('.' + sfx if not sfx.startswith('.') else sfx)
                       for sfx in allowed_suffixes])

    # BFS through root dir
    pt = Path(root)
    fileq = deque([(pt, 0)])
    while len(fileq) > 0:
        cur, lvl = fileq.popleft()
        for chld in cur.iterdir():
            if chld.is_dir() and lvl < depth:
                fileq.append((chld, lvl + 1))
            elif chld.is_file() and\
                    (len(_allowedsfx) == 0 or chld.suffix in _allowedsfx):

                log.debug('reading candidate file: %s', chld)
                # If a file, read the header and check for a match with
                # existing model fields
                comps = _map_header_to_model(chld, to_load)

                # Check if the current file is a better match for the known
                # types
                for mapng in to_load:
                    hmapped, missing = comps[mapng.typ]
                    if mapng.missing is None or mapng.missing > missing:
                        log.debug('Better file match for type %s: %s',
                                  mapng, chld.name)
                        mapng.file, mapng.headerList, mapng.missing =\
                            (chld, hmapped, missing)

    return to_load


def _map_header_to_model(data_file, to_load):

    log.debug('Reading file: %s', data_file)
    with open(data_file, 'r') as f:
        header = f.readline().strip()
    log.debug('header: %s', header)
    hfields = header.split(',')

    choice = {}
    for maps in to_load:
        # typ = model type, map = mapping from text header to model
        # fields, fields = set of model fields
        typ, map, fields = maps.typ, maps.mapping, maps.fields
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
    for maps in type_map:
        file, header = maps.file, maps.headerList
        with open(file, 'r') as reader:
            # header
            reader.readline()
            for line in reader:
                fmap = to_map(header, line.strip().split(','))
                obj = maps.typ(**fmap)
                obj.save()


def load_from_directory(root, depth=4):

    """Find the files in a given root directory which correspond to the
    expected model fields, and then load those files into the DB"""
    ttll = find_and_label_files(all_types, root, depth)
    load_from_type_map(ttll)
