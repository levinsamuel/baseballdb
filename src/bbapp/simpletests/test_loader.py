from django.test import SimpleTestCase
from django.db.models.fields import Field
from bbapp import loader
from bbapp.models import Player, Batting
import logging
import inspect
import pathlib

logging.basicConfig()
log = logging.getLogger('simple_loader_tests')


class SimpleLoaderTest(SimpleTestCase):

    def setUp(self):
        log.setLevel(logging.INFO)
        loader.log.setLevel(logging.INFO)

    def test_label_files(self):

        log.debug('load files from directory')
        # loader.log.setLevel(logging.DEBUG)
        # log.setLevel(logging.DEBUG)

        cur = pathlib.Path(__file__)
        types_with_files = loader.find_and_label_files(
            cur.parent / '../../../data/baseballdatabank-master'
        )
        log.debug('Labeled files: %s', types_with_files)

        playermap = filter(lambda m: m.typ == Player, types_with_files)\
            .__next__()
        self.assertEqual(
            'People.csv', playermap.file.name
        )
        self.assertIn('id', playermap.headerList,
                      'Expected player to use local map from playerID to id')

        battingmap = filter(lambda m: m.typ == Batting, types_with_files)\
            .__next__()
        self.assertEqual(
            'Batting.csv', battingmap.file.name
        )

    def test_get_model_fields(self):

        player_map = filter(lambda m: m.typ == Player, loader.all_types)\
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
        batting_map = filter(lambda m: m.typ == Batting, loader.all_types)\
            .__next__()
        batting_fields = batting_map.fields
        log.debug('batting fields: %s', batting_fields)
        self.assertIn('player_id', batting_fields,
                      'Expected field to be in batting field list')
        self.assertIn('id', batting_fields,
                      'Expected field to be in batting field list')

    # def test_field_mapping(self):
    #     # log.setLevel(logging.DEBUG)
    #
