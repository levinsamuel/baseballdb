from django.test import SimpleTestCase
from bbapp import loader
import logging

logging.basicConfig()
log = logging.getLogger('simple_loader_tests')
log.setLevel(logging.DEBUG)


class SimpleLoaderTest(SimpleTestCase):

    def test_label_files(self):

        log.debug('load files from directory')
        loader.load_from_directory('.')
