from django.core.management.base import BaseCommand, CommandError
from bbapp.models import Player
from bbapp import loader
import logging

log = logging.getLogger('load_command')
log.setLevel(logging.INFO)


class Command(BaseCommand):
    """Command to load into a DB given a directory for data files"""
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument('root_dir')

    def handle(self, *args, **options):
        root = options['root_dir']
        log.debug('read root dir: %s', root)
        loader.load_from_directory(root)
