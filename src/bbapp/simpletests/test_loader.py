from django.test import SimpleTestCase
from django.db.models.fields import Field
from bbapp import loader
from bbapp.models import Player, Batting
import logging
import inspect

logging.basicConfig()
log = logging.getLogger('simple_loader_tests')
log.setLevel(logging.DEBUG)


class SimpleLoaderTest(SimpleTestCase):

    def test_label_files(self):

        log.debug('load files from directory')
        loader.load_from_directory('.')

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
        self.assertIn('player', batting_fields,
                      'Expected field to be in batting field list')
        self.assertIn('id', batting_fields,
                      'Expected field to be in batting field list')
