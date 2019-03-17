from django.test import TestCase
from bbapp.loader import Load
from bbapp.models import Player, Pitching, Batting, Fielding
from pathlib import Path
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class LoaderTest(TestCase):

    def test_loader(self):

        # log.setLevel(logging.DEBUG)
        # loader.log.setLevel(logging.DEBUG)
        # only select a subset of types
        load = Load.from_type_list([Player, Batting, Fielding])

        # load files
        load.load_from_directory(Path(__file__).parent)

        # query tests
        results = Player.objects.all()
        # File has 9 lines + header
        self.assertEqual(9, len(results))

        # query for hank aaron
        aarons = Player.objects.filter(nameLast='Aaron',
                                       nameFirst__startswith='H')

        # should only find one
        self.assertEqual(1, len(aarons))
        aaron = aarons[0]
        # find all 23 batting seasons
        self.assertEqual(23, len(aaron.batting_set.all()),
                         'Expected 23 batting seasons')
        # all fielding seasons
        self.assertEqual(36, len(aaron.fielding_set.all()),
                         'Expected 36 fielding seasons')

# TODO: this is super borken!
    def _load_sample(self):
        pkeys = ('playerID,yearID,stint,teamID,lgID,W,L,G,GS,CG,SHO,SV,IPouts,'
                 'H,ER,HR,BB,SO,BAOpp,ERA,IBB,WP,HBP,BK,BFP,GF,R,SH,SF,GIDP').\
            split(',')

        gr04 = ('greinza01,2004,1,KCA,AL,8,11,24,24,0,0,0,435,143,64,26,26,100'
                ',0.256,3.97,3,1,8,1,599,0,64,3,2,8').split(',')

        gr04mp = loader.to_map(pkeys, gr04)
        p = Pitching(**gr04mp)
        p.save()
        log.debug('read: %s', g.pitching_set.all())

        gr05 = ('greinza01,2005,1,KCA,AL,5,17,33,33,2,0,0,549,233,118,23,53,'
                '114,0.309,5.80,0,4,13,2,829,0,125,4,4,14').split(',')

        g = Player.objects.filter(nameLast='Greinke')
        g = g[0]
        g.pitching_set.create(**loader.to_map(pkeys, gr05))
        log.debug('read: %s', g.pitching_set.all())

        log.debug('read: %s', g.pitching_set.all())
