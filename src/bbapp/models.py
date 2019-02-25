from django.db import models


# Create your models here.
class Master(models.Model):

    id = models.CharField(max_length=9, primary_key=True)
    birthYear = models.IntegerField()
    birthMonth = models.IntegerField()
    birthDay = models.IntegerField()
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
    weight = models.IntegerField()
    height = models.IntegerField()
    bats = models.CharField(max_length=1)
    throws = models.CharField(max_length=1)
    debut = models.DateField()
    finalGame = models.DateField(null=True, blank=True)
    retroID = models.CharField(max_length=16)
    bbrefID = models.CharField(max_length=16)

    def __str__(self):
        return f"Player:: id:{self.id}"


class Batting(models.Model):

    player = models.ForeignKey(Master, on_delete=models.DO_NOTHING)
    yearID = models.IntegerField()
    stint = models.IntegerField()
    teamID = models.IntegerField()
    lgID = models.CharField(max_length=10)

    def __str__(self):
        return f"Batting season:: player:{self.player} year:{self.yearID}"


class Pitching(models.Model):

    player = models.ForeignKey(Master, on_delete=models.DO_NOTHING)
    yearID = models.IntegerField()
    stint = models.IntegerField()
    teamID = models.IntegerField()
    lgID = models.CharField(max_length=10)
    W = models.IntegerField()
    L = models.IntegerField()
    G = models.IntegerField()
    GS = models.IntegerField()
    CG = models.IntegerField()
    SHO = models.IntegerField()
    SV = models.IntegerField()
    IPOuts = models.IntegerField()
    H = models.IntegerField()
    ER = models.IntegerField()
    HR = models.IntegerField()
    BB = models.IntegerField()
    SO = models.IntegerField()
    BAOpp = models.FloatField()
    ERA = models.FloatField()
    IBB = models.IntegerField()
    WP = models.IntegerField()
    HBP = models.IntegerField()
    BK = models.IntegerField()
    BFP = models.IntegerField()
    GF = models.IntegerField()
    R = models.IntegerField()
    SH = models.IntegerField()
    SF = models.IntegerField()
    GIDP = models.IntegerField()

    def __str__(self):
        return f"Pitching season:: player:{self.player} year:{self.yearID}"
