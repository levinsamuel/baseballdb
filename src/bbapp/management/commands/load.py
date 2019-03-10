from django.core.management.base import BaseCommand, CommandError
from bbapp.models import Player
from bbapp.loader import Load, log as loader_log
import logging

log = logging.getLogger('load_command')
log.setLevel(logging.INFO)


class Command(BaseCommand):
    """Command to load into a DB given a directory for data files"""
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument('root_dir')
        parser.add_argument('-b', '--batch-size', type=int, dest='batch_size',
                            default=1000)

    def handle(self, *args, **options):
        root = options['root_dir']
        batch_size = options['batch_size']
        verbosity = options['verbosity']
        if verbosity > 1:
            log.setLevel(logging.DEBUG)
            loader_log.setLevel(logging.DEBUG)
        if verbosity == 1:
            log.setLevel(logging.INFO)
            loader_log.setLevel(logging.INFO)
        log.debug('read root dir: %s', root)

        load = Load()
        load.load_from_directory(root, batch_size=batch_size)
