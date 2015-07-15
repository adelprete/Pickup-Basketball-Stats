from django.db import models
from django.db.models import F, Sum, Avg, signals
from django.core.urlresolvers import reverse

PRIMARY_PLAY = [
        ('fgm','FGM'),
        ('fga','FGA'),
        ('threepm','3PM'),
        ('threepa','3PA'),
        ('blk','BLK'),
        ('to','TO'),
        ('pf','FOUL'),
        ('sub_out','OUT'),
]

SECONDARY_PLAY = [
        ('dreb','DREB'),
        ('oreb','OREB'),
        ('stls','STL'),
        ('ba','BA'),
        ('fd','FD'),
        ('sub_in','IN'),
]

ASSIST_PLAY = [
        ('pot_ast','Pot'),
        ('asts','Ast')
]

GAME_TYPES = [
    ('5v5','5v5'),
    ('4v4','4v4'),
    ('3v3','3v3'),
    ('2v2','2v2'),
    ('1v1','1v1'),
]

ALL_PLAY_TYPES = PRIMARY_PLAY + SECONDARY_PLAY + ASSIST_PLAY

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
    
    def get_absolute_url(self):
        return reverse("player_page",kwargs={'id':self.id})

    def get_averages(self):
        """
        Returns a dictionary of the player's averages
        """
        player_averages = {}
        for play in ALL_PLAY_TYPES:
            if play[0] not in ['sub_out','sub_in']:
                x = self.statline_set.all().aggregate(Avg(play[0]))
                player_averages.update(x)
        player_averages.update(self.statline_set.all().aggregate(Avg('points'),Avg('total_rebounds')))
        return player_averages

    class Meta():
        ordering = ['first_name']


def model_team1():
    return [Player.objects.get(first_name='Team1').pk]

def model_team2():
    return [Player.objects.get(first_name='Team2').pk]

class Game(models.Model):
    date = models.DateField(blank=True,null=True)
    title = models.CharField(max_length=30,blank=True)
    team1 = models.ManyToManyField('basketball.Player',default=model_team1(),related_name='team1_set')
    team2 = models.ManyToManyField('basketball.Player',default=model_team2(),related_name='team2_set')
    team1_score = models.PositiveIntegerField(default=0)
    team2_score = models.PositiveIntegerField(default=0)
    youtube_url = models.URLField(max_length=2000,blank=True)
    game_type = models.CharField(max_length=30,choices=GAME_TYPES,null=True)

    def __str__(self):
        return "%s: %s" % (self.date.isoformat(),self.title)

    def get_absolute_url(self):
        return reverse("box_score",kwargs={'id':self.id})
    
    def calculate_game_score(self):
        """Calculates a game's score by finding the sum of points for each team's statlines
        """
        team1_statlines = StatLine.objects.filter(game=self,player__in=self.team1.all())
        team2_statlines = StatLine.objects.filter(game=self,player__in=self.team2.all())

        self.team1_score = team1_statlines.aggregate(Sum('points'))['points__sum']
        self.team2_score = team2_statlines.aggregate(Sum('points'))['points__sum']

        self.save()
    
    def reset_statlines(self):
        """Resets the statlines for each player to zero accross all fields
        Usually used for when you're about to recalculate a game's stats
        """
        statlines = self.statline_set.all()
        for line in statlines:
            for play in ALL_PLAY_TYPES:
                if play[0] not in ['sub_out','sub_in']:
                    setattr(line,play[0],0)
            line.points = 0
            line.total_rebounds = 0
            line.def_pos = 0
            line.off_pos = 0
            line.total_pos = 0
            line.save()
    
    def get_bench(self):
        """Returns a list of players that start on the bench for a game.
        It does so by analyzing the subsitution plays
        """
        playbyplays = self.playbyplay_set.filter(primary_play="sub_out").order_by("time")
        team1_oncourt = self.team1.all().values_list('pk',flat=True)
        team2_oncourt = self.team2.all().values_list('pk',flat=True)
        
        been_in = []
        bench = []
        for play in playbyplays:
            if play.primary_player.pk not in been_in:
                been_in.append(play.primary_player.pk)
            if play.secondary_player.pk not in been_in:
                bench.append(play.secondary_player.pk)
        return bench
    
    def calculate_statlines(self):
        """Calculates the statlines for a game by looping through the games Play By Play
        Statlines are reset to zero before looping over the Play by Plays
        """
        self.reset_statlines()
        playbyplays = self.playbyplay_set.all().order_by('time')
        statlines = self.statline_set.all()
        bench = self.get_bench()
        for play in playbyplays:
            if play.primary_play not in ['sub_out','sub_in']:
                primary_line = StatLine.objects.get(game=self,player=play.primary_player)
                orig_val = getattr(primary_line,play.primary_play)
                setattr(primary_line,play.primary_play,orig_val+1)
                if play.primary_play == 'fgm':
                    primary_line.fga += 1
                    primary_line.points += 1
                if play.primary_play == 'threepa':
                    primary_line.fga += 1
                if play.primary_play == 'threepm':
                    primary_line.threepa += 1
                    primary_line.fga += 1
                    primary_line.fgm += 1
                    primary_line.points += 2

                primary_line.save()
                if play.primary_play in ['threepm','fgm','to']:
                    if primary_line.player in self.team1.all():
                        statlines.filter(player__in=self.team1.all()).exclude(player__pk__in=bench).update(off_pos=F('off_pos')+1)
                        statlines.filter(player__in=self.team2.all()).exclude(player__pk__in=bench).update(def_pos=F('def_pos')+1)
                    else:
                        statlines.filter(player__in=self.team1.all()).exclude(player__pk__in=bench).update(def_pos=F('def_pos')+1)
                        statlines.filter(player__in=self.team2.all()).exclude(player__pk__in=bench).update(off_pos=F('off_pos')+1)

                #secondary play
                if play.secondary_play:
                    secondary_line = StatLine.objects.get(game=self,player=play.secondary_player)
                    orig_val = getattr(secondary_line,play.secondary_play)
                    setattr(secondary_line,play.secondary_play,orig_val+1)
                    
                    if play.secondary_play == 'dreb' or play.secondary_play == 'oreb':
                        secondary_line.total_rebounds += 1
                    
                    secondary_line.save()
                    if play.secondary_play == 'dreb':
                        if primary_line.player in self.team1.all():
                            statlines.filter(player__in=self.team1.all()).exclude(player__pk__in=bench).update(off_pos=F('off_pos')+1)
                            statlines.filter(player__in=self.team2.all()).exclude(player__pk__in=bench).update(def_pos=F('def_pos')+1)
                        else:
                            statlines.filter(player__in=self.team1.all()).exclude(player__pk__in=bench).update(def_pos=F('def_pos')+1)
                            statlines.filter(player__in=self.team2.all()).exclude(player__pk__in=bench).update(off_pos=F('off_pos')+1)
                
                #assist play
                if play.assist:
                    assist_line = StatLine.objects.get(game=self,player=play.assist_player)
                    orig_val = getattr(assist_line,play.assist)
                    setattr(assist_line,play.assist,orig_val+1)
                    assist_line.save()
            else:
                bench.append(play.primary_player.pk)
                bench.remove(play.secondary_player.pk)
        statlines.update(total_pos=F('off_pos')+F('def_pos'))
        self.calculate_game_score()

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
    def_pos = models.PositiveIntegerField(default=0)
    off_pos = models.PositiveIntegerField(default=0)
    total_pos = models.PositiveIntegerField(default=0)
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
