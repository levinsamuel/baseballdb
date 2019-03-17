import logging
import pathlib

from django.test import SimpleTestCase

from bbapp.loader import Load, log as loaderlog
from bbapp.models import Player, Batting

log = logging.getLogger(__name__)
root_level = logging.getLogger().getEffectiveLevel()


class SimpleLoaderTest(SimpleTestCase):

    def setUp(self):
        log.setLevel(root_level)
        loaderlog.setLevel(root_level)

    def test_label_files(self):

        log.debug('load files from directory')
        # loader.log.setLevel(logging.DEBUG)
        # log.setLevel(logging.DEBUG)

        cur = pathlib.Path(__file__)

        load = Load()
        load.find_and_label_files(
            cur.parent / '../../../data/baseballdatabank-master'
        )
        log.debug('Labeled files: %s', load)

        playermap = filter(lambda m: m.typ == Player, load.mappings) \
            .__next__()
        self.assertEqual(
            'People.csv', playermap.file.name
        )
        self.assertIn('id', playermap.headerList,
                      'Expected player to use local map from playerID to id')

        battingmap = filter(lambda m: m.typ == Batting, load.mappings) \
            .__next__()
        self.assertEqual(
            'Batting.csv', battingmap.file.name
        )

    def test_get_model_fields(self):

        load = Load()
        player_map = filter(lambda m: m.typ == Player, load.mappings) \
            .__next__()
        player_fields = player_map.fields
        log.debug('player fields: %s', player_fields)

        self.assertIn('id', player_fields,
                      'Expected field to be in player field list')
        self.assertIn('deathCountry', player_fields,
                      'Expected field to be in player field list')
        self.assertIn('bbrefID', player_fields,
                      'Expected field to be in player field list')
        self.assertNotIn('player_id', player_fields,
                         'Unexpected field in player field list')

        # Test batting key
        batting_map = filter(lambda m: m.typ == Batting, load.mappings) \
            .__next__()
        batting_fields = batting_map.fields
        log.debug('batting fields: %s', batting_fields)
        self.assertIn('player_id', batting_fields,
                      'Expected field to be in batting field list')
        self.assertIn('id', batting_fields,
                      'Expected field to be in batting field list')

    def test_log_levels(self):

        log.info('hi')
