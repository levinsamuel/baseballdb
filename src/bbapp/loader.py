import logging
from collections import deque
from pathlib import Path

from django.db.models.fields.related import ForeignKey

from bbapp.models import Batting, Fielding, Pitching, Player

log = logging.getLogger(__name__)

# Global maps are overridden by type-specific maps
global_maps = {
    'playerID': 'player_id'
}


class Mapping:
    """Mapping from type to its header fields and data file. Throws a KeyError
    on an invalid type"""
    field_mappings = {
        Player: {
            'playerID': 'id',
        },
        Batting: {
            '2B': 'doubles',
            '3B': 'triples',
        },
        Pitching: {
            'IPouts': 'IPOuts',
        },
        Fielding: {
            'POS': 'Pos'
        },
    }

    def __init__(self, typ):
        self.typ = typ
        self.mapping = Mapping.field_mappings[typ]
        self.fields = \
            {(fn.name + '_id' if isinstance(fn, ForeignKey) else fn.name)
             for fn in typ._meta.fields}
        self.file = None
        self.missing = None
        self.headerList = None

    def __repr__(self):
        return f'mapping for type: {self.typ}'

    def update_file_mapping(self, chld, hmapped, missing):
        self.file, self.headerList, self.missing =\
            chld, hmapped, missing


class Load:
    """An instance of a load, to track where it left off and stuff"""
    def __init__(self, mappings=None, *args, **kwargs):

        super(Load, self).__init__(*args, **kwargs)
        if mappings is not None:
            self.mappings = mappings
        else:
            self.mappings = [Mapping(t) for t in Mapping.field_mappings.keys()]

        self.current_map = self.mappings[0]
        self.current_line = 0

    @staticmethod
    def from_type_list(type_list):
        return Load([Mapping(t) for t in type_list])

    def find_and_label_files(self, root, depth=4,
                             allowed_suffixes=('txt', 'csv', 'dat')):
        """Given a root directory, search all subdirectories for files
        matching the model classes based on their headers"""

        # Function to perform on each file in root dir
        def update_maps(each_file):
            log.debug('reading candidate file: %s', each_file)
            # If a file, read the header and check for a match with
            # existing model fields
            header_maps = _map_header_to_model(each_file, self.mappings)

            # Check if the current file is a better match for the known types
            for map, hm in zip(self.mappings, header_maps):
                hmapped, missing = hm
                if map.missing is None or map.missing > missing:
                    log.debug('Better file match for type %s: %s',
                              map, each_file.name)
                    map.update_file_mapping(each_file, hmapped, missing)

        _bfs(root, update_maps, allowed_suffixes=allowed_suffixes, depth=depth)

    def load_from_mappings(self, batch_size=1000):
        """Given a map containing the model fields and some associated data,
        including the file to load, load the files"""
        for maps in self.mappings:
            file, header = maps.file, maps.headerList
            log.info('loading type %s from file: %s', maps.typ.__name__,
                     file)
            with open(file, 'r') as reader:
                # header
                reader.readline()
                created = 0
                while True:
                    batch = _read_batch(reader, batch_size)
                    if batch:
                        mapped = \
                            [maps.typ(
                                **_to_map(header, line.strip().split(','))
                             ) for line in batch]
                        maps.typ.objects.bulk_create(mapped)
                        created += len(batch)
                        log.info('Created %d %s records', created,
                                 maps.typ.__name__)
                    if len(batch) < batch_size:
                        break

    def load_from_directory(self, root, depth=4, batch_size=1000):
        """Find the files in a given root directory which correspond to the
        expected model fields, and then load those files into the DB"""
        self.find_and_label_files(root, depth)
        self.load_from_mappings(batch_size)

    def write_progress(self):
        pass


def _read_batch(handle, batch_size):
    """Read lines into a deque"""
    # handle has to come second, or else the generator will try to read
    # an extra line before it find that range has run out, and will lose
    # a line
    batch = deque([line for _, line in zip(range(batch_size), handle)])
    return batch


def _map_header_to_model(data_file, mappings):
    """Read file header and compare it to each expected model type to find
    the best fit. Return a map from the type to the header of the file,
    mapped to that type, and the number of missing fields for that file."""
    log.debug('Reading file: %s', data_file)
    with open(data_file, 'r') as f:
        header = f.readline().strip()
    log.debug('header: %s', header)
    hfields = header.split(',')

    choice = []
    for maps in mappings:
        # typ = model type, map = mapping from text header to model
        # fields, fields = set of model fields
        typ, mapping, fields = maps.typ, maps.mapping, maps.fields
        log.debug('checking type for match: %s', typ)

        # map read header to field names in model
        hmapped = [_map_header_fields(h, mapping) for h in hfields]

        # check how many fields are found in each type
        headerset = set(hmapped)
        ints = headerset & fields
        missing = (len(fields) - len(ints)) + \
                  (len(headerset) - len(ints))
        log.debug('''header for file %s is missing %d fields
                  for type %s''', data_file.name, missing, typ)

        choice.append((hmapped, missing))

    return choice


def _map_header_fields(f, local_map):
    if local_map is not None and f in local_map:
        return local_map[f]
    elif f in global_maps:
        return global_maps[f]
    else:
        return f


def _to_map(keys, vals):
    """Attach the keys from the file header to the values. Both are assumed
    to be in the order read from the input file"""
    return {k: v for k, v in zip(keys, vals)
            if v is not None and v != ''}


def _bfs(root, fileexec, allowed_suffixes=[], depth=4):
    """Breadth-first search through a directory and execute the passed function
    on each file matching the criteria"""
    _allowedsfx = {('.' + sfx if not sfx.startswith('.') else sfx)
                   for sfx in allowed_suffixes}

    # BFS through root dir
    fileq = deque([(Path(root), 0)])
    while len(fileq) > 0:
        cur, lvl = fileq.popleft()
        for chld in cur.iterdir():
            if chld.is_dir() and lvl < depth:
                fileq.append((chld, lvl + 1))
            elif chld.is_file() and\
                    (len(_allowedsfx) == 0 or chld.suffix in _allowedsfx):

                # Pass function to execute on each file
                fileexec(chld)
