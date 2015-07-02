from django.db import models
from django.db.models import signals
from django.core.urlresolvers import reverse

PRIMARY_PLAY = [
        ('fgm','FGM'),
        ('fga','FGA'),
        ('threepm','3PM'),
        ('threepa','3PA'),
        ('stls','STL'),
        ('blk','BLK'),
        ('to','TO'),
]

SECONDARY_PLAY = [
        ('dreb','DREB'),
        ('oreb','OREB'),
        ('ba','BA'),
]

ASSIST_PLAY = [
        ('pot_ast','POT'),
        ('asts','AST')
]

class Player(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30,blank=True)
    height = models.CharField(max_length=30,blank=True)
    weight = models.CharField(max_length=30,blank=True)
    image_src = models.ImageField(upload_to ='player_images/',blank=True,null=True)
	
    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '%s %s' % (self.first_name,self.last_name)

class Game(models.Model):
    date = models.DateField(blank=True,null=True)
    title = models.CharField(max_length=30,blank=True)
    team1 = models.ManyToManyField('basketball.Player',related_name='team1_set')
    team2 = models.ManyToManyField('basketball.Player',related_name='team2_set')
    team1_score = models.PositiveIntegerField(default=0)
    team2_score = models.PositiveIntegerField(default=0)
    team1_off_rebounds = models.PositiveIntegerField(default=0)
    team1_def_rebounds = models.PositiveIntegerField(default=0)
    team2_off_rebounds = models.PositiveIntegerField(default=0)
    team2_def_rebounds = models.PositiveIntegerField(default=0)
    youtube_url = models.URLField(max_length=2000,blank=True)

    def __str__(self):
        return "%s: %s" % (self.date.isoformat(),self.title)

    def get_absolute_url(self):
        return reverse("box_score",kwargs={'id':self.id})

class StatLine(models.Model):
    game = models.ForeignKey('basketball.Game')
    player = models.ForeignKey('basketball.Player')
    fgm = models.PositiveIntegerField(default=0)
    fga = models.PositiveIntegerField(default=0)
    threepm = models.PositiveIntegerField(default=0)
    threepa = models.PositiveIntegerField(default=0)
    dreb = models.PositiveIntegerField(default=0)
    oreb = models.PositiveIntegerField(default=0)
    total_rebounds = models.PositiveIntegerField(default=0)
    asts = models.PositiveIntegerField(default=0)
    pot_ast = models.PositiveIntegerField(default=0)
    blk = models.PositiveIntegerField(default=0)
    ba = models.PositiveIntegerField(default=0)
    stls = models.PositiveIntegerField(default=0)
    to = models.PositiveIntegerField(default=0)
    fd = models.PositiveIntegerField(default=0)
    pf = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '%s - %s - %s' % (self.player.first_name,self.game.title,self.game.date.isoformat())

class PlayByPlay(models.Model):
    game = models.ForeignKey('basketball.Game')
    time = models.TimeField()
    primary_play = models.CharField(max_length=30,choices=PRIMARY_PLAY)
    primary_player = models.ForeignKey('basketball.Player',related_name='primary_plays')
    secondary_play = models.CharField(max_length=30,choices=SECONDARY_PLAY,blank=True)
    secondary_player= models.ForeignKey('basketball.Player',related_name='secondary_plays',blank=True,null=True)
    assist = models.CharField(max_length=30,choices=ASSIST_PLAY,blank=True)
    assist_player = models.ForeignKey('basketball.Player',related_name='+',blank=True,null=True)

    def __str__(self):
    	return "%s - %s - %s" % (self.primary_play,self.primary_player.first_name,self.game.title)
