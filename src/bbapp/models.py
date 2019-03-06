from django.db import models


class Player(models.Model):

    id = models.CharField(max_length=9, primary_key=True)
    birthYear = models.IntegerField(null=True, blank=True)
    birthMonth = models.IntegerField(null=True, blank=True)
    birthDay = models.IntegerField(null=True, blank=True)
    birthCountry = models.CharField(max_length=255, null=True, blank=True)
    birthState = models.CharField(max_length=255, null=True, blank=True)
    birthCity = models.CharField(max_length=255, null=True, blank=True)
    deathYear = models.IntegerField(null=True, blank=True)
    deathMonth = models.IntegerField(null=True, blank=True)
    deathDay = models.IntegerField(null=True, blank=True)
    deathCountry = models.CharField(max_length=255, null=True, blank=True)
    deathState = models.CharField(max_length=255, null=True, blank=True)
    deathCity = models.CharField(max_length=255, null=True, blank=True)
    nameFirst = models.CharField(max_length=255, null=True, blank=True)
    nameLast = models.CharField(max_length=255, null=True, blank=True)
    nameGiven = models.CharField(max_length=255, null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    bats = models.CharField(max_length=1, null=True, blank=True)
    throws = models.CharField(max_length=1, null=True, blank=True)
    debut = models.DateField(null=True, blank=True)
    finalGame = models.DateField(null=True, blank=True)
    retroID = models.CharField(max_length=16, null=True, blank=True)
    bbrefID = models.CharField(max_length=16, null=True, blank=True)

    def __str__(self):
        return f"Player:: id:{self.id}"


class Batting(models.Model):

    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    yearID = models.IntegerField(default=0)
    stint = models.IntegerField(default=0)
    teamID = models.CharField(max_length=5)
    lgID = models.CharField(max_length=10)
    G = models.IntegerField(null=True, blank=True)
    AB = models.IntegerField(null=True, blank=True)
    R = models.IntegerField(null=True, blank=True)
    H = models.IntegerField(null=True, blank=True)
    doubles = models.IntegerField(null=True, blank=True)
    triples = models.IntegerField(null=True, blank=True)
    HR = models.IntegerField(null=True, blank=True)
    RBI = models.IntegerField(null=True, blank=True)
    SB = models.IntegerField(null=True, blank=True)
    CS = models.IntegerField(null=True, blank=True)
    BB = models.IntegerField(null=True, blank=True)
    SO = models.IntegerField(null=True, blank=True)
    IBB = models.IntegerField(null=True, blank=True)
    HBP = models.IntegerField(null=True, blank=True)
    SH = models.IntegerField(null=True, blank=True)
    SF = models.IntegerField(null=True, blank=True)
    GIDP = models.IntegerField(null=True, blank=True)

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
    BAOpp = models.FloatField(null=True, blank=True)
    ERA = models.FloatField(null=True, blank=True)
    IBB = models.IntegerField(null=True, blank=True)
    WP = models.IntegerField(null=True, blank=True)
    HBP = models.IntegerField(null=True, blank=True)
    BK = models.IntegerField(null=True, blank=True)
    BFP = models.IntegerField(null=True, blank=True)
    GF = models.IntegerField(null=True, blank=True)
    R = models.IntegerField(default=0)
    "Sacrifices by opposing batters"
    SH = models.IntegerField(null=True, blank=True)
    "Sacrifice flies"
    SF = models.IntegerField(null=True, blank=True)
    GIDP = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Pitching season:: player:{self.player} year:{self.yearID}"


class Fielding(models.Model):

    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    yearID = models.IntegerField(default=0)
    stint = models.IntegerField(default=0)
    teamID = models.CharField(max_length=5)
    lgID = models.CharField(max_length=10)
    Pos = models.CharField(max_length=5)
    G = models.IntegerField(default=0)
    GS = models.IntegerField(null=True, blank=True)
    InnOuts = models.IntegerField(null=True, blank=True)
    "Putouts"
    PO = models.IntegerField(null=True, blank=True)
    "Assists"
    A = models.IntegerField(default=0)
    "Errors"
    E = models.IntegerField(null=True, blank=True)
    "Double plays"
    DP = models.IntegerField(default=0)
    "Passed Balls"
    PB = models.IntegerField(null=True, blank=True)
    "Wild Pitches"
    WP = models.IntegerField(null=True, blank=True)
    "Stolen Bases"
    SB = models.IntegerField(null=True, blank=True)
    "Caught Stealing"
    CS = models.IntegerField(null=True, blank=True)
    "Zone Rating"
    ZR = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Fielding season:: player:{self.player} year:{self.yearID}"
