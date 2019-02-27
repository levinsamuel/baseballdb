from bbapp.models import Pitching, Player

global_maps = {
    'playerID': 'player_id'
}

pitching_maps = {
    'IPouts': 'IPOuts'
}

batting_maps = {
    '2B': 'doubles',
    '3B': 'triples'
}

gr04 = 'greinza01,2004,1,KCA,AL,8,11,24,24,0,0,0,435,143,64,26,26,100,0.256,3.97,3,1,8,1,599,0,64,3,2,8'.split(',')
pkeys = 'playerID,yearID,stint,teamID,lgID,W,L,G,GS,CG,SHO,SV,IPouts,H,ER,HR,BB,SO,BAOpp,ERA,IBB,WP,HBP,BK,BFP,GF,R,SH,SF,GIDP'.split(',')
pkeys[0] = 'player_id'
pkeys[pkeys.index('IPouts')] = 'IPOuts'
g = Player.objects.filter(nameLast='Greinke')
g = g[0]
g.pitching_set.all()


def to_map(keys, vals):
    return {k: (v if v != '' else None) for k, v in zip(keys, vals)}


gr04mp = to_map(pkeys, gr04)
p = Pitching(**gr04mp)
p.save()
g.pitching_set.all()
gr05 = 'greinza01,2005,1,KCA,AL,5,17,33,33,2,0,0,549,233,118,23,53,114,0.309,5.80,0,4,13,2,829,0,125,4,4,14'.split(',')
g.pitching_set.create(**to_map(pkeys, gr05))
g.pitching_set.all()
