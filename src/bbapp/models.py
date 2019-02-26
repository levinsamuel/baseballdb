from django.db import models


class Player(models.Model):

    id = models.CharField(max_length=9, primary_key=True)
    birthYear = models.IntegerField(default=0)
    birthMonth = models.IntegerField(default=0)
    birthDay = models.IntegerField(default=0)
    birthCountry = models.CharField(max_length=255)
    birthState = models.CharField(max_length=255)
    birthCity = models.CharField(max_length=255)
    deathYear = models.IntegerField(null=True, blank=True)
    deathMonth = models.IntegerField(null=True, blank=True)
    deathDay = models.IntegerField(null=True, blank=True)
    deathCountry = models.CharField(max_length=255, null=True, blank=True)
    deathState = models.CharField(max_length=255, null=True, blank=True)
    deathCity = models.CharField(max_length=255, null=True, blank=True)
    nameFirst = models.CharField(max_length=255)
    nameLast = models.CharField(max_length=255)
    nameGiven = models.CharField(max_length=255)
    weight = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    bats = models.CharField(max_length=1)
    throws = models.CharField(max_length=1)
    debut = models.DateField()
    finalGame = models.DateField(null=True, blank=True)
    retroID = models.CharField(max_length=16)
    bbrefID = models.CharField(max_length=16)

    def __str__(self):
        return f"Player:: id:{self.id}"


class Batting(models.Model):

    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    yearID = models.IntegerField(default=0)
    stint = models.IntegerField(default=0)
    teamID = models.IntegerField(default=0)
    lgID = models.CharField(max_length=10)
    G = models.IntegerField(default=0)
    AB = models.IntegerField(default=0)
    R = models.IntegerField(default=0)
    H = models.IntegerField(default=0)
    doubles = models.IntegerField(default=0)
    triples = models.IntegerField(default=0)
    HR = models.IntegerField(default=0)
    RBI = models.IntegerField(default=0)
    SB = models.IntegerField(default=0)
    CS = models.IntegerField(default=0)
    BB = models.IntegerField(default=0)
    SO = models.IntegerField(default=0)
    IBB = models.IntegerField(default=0)
    HBP = models.IntegerField(default=0)
    SH = models.IntegerField(default=0)
    SF = models.IntegerField(default=0)
    GIDP = models.IntegerField(default=0)

    def __str__(self):
        return f"Batting season:: player:{self.player} year:{self.yearID}"


class Pitching(models.Model):

    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    yearID = models.IntegerField(default=0)
    stint = models.IntegerField(default=0)
    teamID = models.CharField(max_length=5)
    lgID = models.CharField(max_length=10)
    W = models.IntegerField(default=0)
    L = models.IntegerField(default=0)
    G = models.IntegerField(default=0)
    GS = models.IntegerField(default=0)
    CG = models.IntegerField(default=0)
    SHO = models.IntegerField(default=0)
    SV = models.IntegerField(default=0)
    IPOuts = models.IntegerField(default=0)
    H = models.IntegerField(default=0)
    ER = models.IntegerField(default=0)
    HR = models.IntegerField(default=0)
    BB = models.IntegerField(default=0)
    SO = models.IntegerField(default=0)
    BAOpp = models.FloatField()
    ERA = models.FloatField()
    IBB = models.IntegerField(default=0)
    WP = models.IntegerField(default=0)
    HBP = models.IntegerField(default=0)
    BK = models.IntegerField(default=0)
    BFP = models.IntegerField(default=0)
    GF = models.IntegerField(default=0)
    R = models.IntegerField(default=0)
    "Sacrifices by opposing batters"
    SH = models.IntegerField(default=0)
    "Sacrifice flies"
    SF = models.IntegerField(default=0)
    GIDP = models.IntegerField(default=0)

    def __str__(self):
        return f"Pitching season:: player:{self.player} year:{self.yearID}"
