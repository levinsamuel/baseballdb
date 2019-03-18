from django.test import SimpleTestCase
# import TestCase for integrated tests


class PlayerTests(SimpleTestCase):

    def test_float_to_int_conversion(self):
        header = ('playerID,yearID,stint,teamID,lgID,W,L,G,GS,CG,SHO,SV,'
                  'IPouts,H,ER,HR,BB,SO,BAOpp,ERA,IBB,WP,HBP,BK,BFP,GF,R,SH,'
                  'SF,GIDP')
        line = ('atkinal01,1884,1,PH4,AA,11,11,22,22,20,1,0,553,186,86,3,21,93'
                ',,4.20,,28,10.0,0,792,0,130,,,')


