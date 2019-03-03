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
        loader.log.setLevel(logging.DEBUG)
        cur = pathlib.Path(__file__)
        loader.find_and_label_files(
            cur.parent / '../../../data/baseballdatabank-master'
        )

    def test_get_model_fields(self):

        player_fields = loader._get_fields_for_type(Player)
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
        batting_fields = loader._get_fields_for_type(Batting)
        log.debug('batting fields: %s', batting_fields)
        self.assertIn('player_id', batting_fields,
                      'Expected field to be in batting field list')
        self.assertIn('id', batting_fields,
                      'Expected field to be in batting field list')

    def test_field_mapping(self):
        # log.setLevel(logging.DEBUG)
        log.debug('%s', loader.types_to_load)
