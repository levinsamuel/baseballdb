from django.test import TestCase
from bbapp import loader
from bbapp.models import Player, Pitching


class LoaderTest(TestCase):

    def test_loader(self):
        pass

    def _load_sample(self):
        pkeys = ('playerID,yearID,stint,teamID,lgID,W,L,G,GS,CG,SHO,SV,IPouts,'
                 'H,ER,HR,BB,SO,BAOpp,ERA,IBB,WP,HBP,BK,BFP,GF,R,SH,SF,GIDP').\
            split(',')

        gr04 = ('greinza01,2004,1,KCA,AL,8,11,24,24,0,0,0,435,143,64,26,26,100'
                ',0.256,3.97,3,1,8,1,599,0,64,3,2,8').split(',')

        g = Player.objects.filter(nameLast='Greinke')
        g = g[0]
        g.pitching_set.all()

        gr04mp = loader.to_map(pkeys, gr04)
        p = Pitching(**gr04mp)
        p.save()
        g.pitching_set.all()

        gr05 = ('greinza01,2005,1,KCA,AL,5,17,33,33,2,0,0,549,233,118,23,53,'
                '114,0.309,5.80,0,4,13,2,829,0,125,4,4,14').split(',')

        g.pitching_set.create(**loader.to_map(pkeys, gr05))
        g.pitching_set.all()
