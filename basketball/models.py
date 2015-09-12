from django.db import models
from django.db.models import F, Sum, Q, Avg, signals
from django.core.urlresolvers import reverse

PRIMARY_PLAY = [
    ('fgm', 'FGM'),
    ('fga', 'FGA'),
    ('threepm', '3PM'),
    ('threepa', '3PA'),
    ('blk', 'BLK'),
    ('to', 'TO'),
    ('pf', 'FOUL'),
    ('sub_out', 'OUT'),
    ('misc', 'Misc')
]

SECONDARY_PLAY = [
    ('dreb', 'DREB'),
    ('oreb', 'OREB'),
    ('stls', 'STL'),
    ('ba', 'BA'),
    ('fd', 'FD'),
    ('sub_in', 'IN'),
]

ASSIST_PLAY = [
    ('pot_ast', 'Pot'),
    ('asts', 'Ast')
]

GAME_TYPES = [
    ('5v5', '5v5'),
    ('4v4', '4v4'),
    ('3v3', '3v3'),
    ('2v2', '2v2'),
    ('1v1', '1v1'),
]

ALL_PLAY_TYPES = PRIMARY_PLAY + SECONDARY_PLAY + ASSIST_PLAY

TOP_PLAY_RANKS = [
    ('t01', 'T1'),
    ('t02', 'T2'),
    ('t03', 'T3'),
    ('t04', 'T4'),
    ('t05', 'T5'),
    ('t06', 'T6'),
    ('t07', 'T7'),
    ('t08', 'T8'),
    ('t09', 'T9'),
    ('t10', 'T10'),
]

NOT_TOP_PLAY_RANKS = [
    ('nt01', 'NT1'),
    ('nt02', 'NT2'),
    ('nt03', 'NT3'),
    ('nt04', 'NT4'),
    ('nt05', 'NT5'),
    ('nt06', 'NT6'),
    ('nt07', 'NT7'),
    ('nt08', 'NT8'),
    ('nt09', 'NT9'),
    ('nt10', 'NT10'),
]
RANKS = TOP_PLAY_RANKS + NOT_TOP_PLAY_RANKS


class Player(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True)
    height = models.CharField(max_length=30, blank=True)
    weight = models.CharField(max_length=30, blank=True)
    image_src = models.ImageField(
        upload_to='player_images/', blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    position = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return reverse("player_page", kwargs={'id': self.id})

    def total_games(self, season=None):
        
        if season:
            return Game.objects.filter(
                    Q(team1=self) | Q(team2=self), 
                    date__range=(season.start_date, season.end_date)).distinct().count()

        return Game.objects.filter(Q(team1=self) | Q(team2=self)).distinct().count()

    def total_wins(self, season=None):
        
        if season:
            return self.winning_players_set.filter(date__range=(season.start_date, season.end_date)).count()
        
        return self.winning_players_set.all().count()

    def total_losses(self, season=None):
        
        losses = self.total_games(season=season) - self.total_wins(season=season)
        
        if losses < 0:
            losses = 0
        
        return losses

    def get_per_100_possessions_data(self, stat, game_type, season=None):
        """Returns per 100 possessions data"""
        
        percentage = 0.0
        simple_statistics = [
                'dreb',
                'oreb',
                'total_rebounds',
                'asts',
                'pot_ast',
                'stls',
                'to',
                'points',
                'blk'
        ]

        """statistics from the list are calculated the same way"""
        if stat in simple_statistics:
            if season:
                result = self.statline_set.filter(game__game_type=game_type, game__date__range=(
                    season.start_date, season.end_date)).aggregate(Sum(stat), Sum('off_pos'))
            else:
                result = self.statline_set.filter(
                    game__game_type=game_type).aggregate(Sum(stat), Sum('off_pos'))
            
            if result['off_pos__sum'] and result['off_pos__sum'] is not 0:
                percentage = (result[stat + '__sum'] /
                              result['off_pos__sum']) * 100
            return percentage

        statlines = self.statline_set.filter(game__game_type=game_type)
        if season:
            statlines = statlines.filter(game__date__range=(season.start_date, season.end_date))

        """The following statistics have unique calculations"""
        if stat == "fgm_percent":
            result = statlines.aggregate(Sum('fgm'), Sum('fga'))
            if result['fga__sum'] and result['fga__sum'] is not 0:
                percentage = result['fgm__sum'] / result['fga__sum'] * 100
            
        elif stat == 'threepm_percent':
            result = statlines.aggregate(Sum('threepm'), Sum('threepa'), Sum('off_pos'))
            if result['threepa__sum'] and result['threepa__sum'] is not 0:
                percentage = result['threepm__sum'] / result['threepa__sum'] * 100

        elif stat == 'dreb_percent':
            result = statlines.aggregate(Sum('dreb'), Sum('dreb_opp'))
            if result['dreb_opp__sum'] and result['dreb_opp__sum'] is not 0:
                percentage = result['dreb__sum'] / result['dreb_opp__sum'] * 100

        elif stat == 'oreb_percent':
            result = statlines.aggregate(Sum('oreb'), Sum('oreb_opp'))
            if result['oreb_opp__sum'] and result['oreb_opp__sum'] is not 0:
                percentage = result['oreb__sum'] / result['oreb_opp__sum'] * 100

        elif stat == 'treb_percent':
            result = statlines.aggregate(Sum('total_rebounds'), Sum('dreb_opp'), Sum('oreb_opp'))
            if result['dreb_opp__sum']:
                percentage = result['total_rebounds__sum'] / \
                            (result['oreb_opp__sum'] + result['dreb_opp__sum']) * 100

        elif stat == 'ts_percent':
            result = statlines.aggregate(Sum('points'), Sum('fga'))
            if result['fga__sum']:
                percentage = result['points__sum'] / result['fga__sum'] * 100

        elif stat == 'off_rating' or stat == 'def_rating':
            result = statlines.aggregate(Sum('off_pos'), Sum('def_pos'))
            
            if stat == 'off_rating':
                team1_games = Game.objects.filter(team1=self)
                team2_games = Game.objects.filter(team2=self)
            else:
                team1_games = Game.objects.filter(team2=self)
                team2_games = Game.objects.filter(team1=self)

            if season:
                team1_games = team1_games.filter(
                        date__range=(season.start_date, season.end_date))
                team2_games = team2_games.filter(
                        date__range=(season.start_date, season.end_date))

            team1_result = team1_games.aggregate(Sum("team1_score"))
            team2_result = team2_games.aggregate(Sum("team2_score"))

            if team1_result['team1_score__sum'] == None:
                team1_result['team1_score__sum'] = 0
            if team2_result['team2_score__sum'] == None:
                team2_result['team2_score__sum'] = 0

            total_team_points = team1_result['team1_score__sum'] + team2_result['team2_score__sum']
            if stat == 'off_rating' and result['off_pos__sum']:
                percentage = total_team_points / result['off_pos__sum'] * 100
            elif stat == 'def_rating' and result['def_pos__sum']:
                percentage = total_team_points / result['def_pos__sum'] * 100

        else:
            raise ValueError('First argument must be either dreb, oreb, asts, pot_ast, stls, to, blk, points, total_rebounds, fgm_percent, 3pm_percent, dreb_percent, oreb_percent, treb_percent, ts_percent, off_rating, def_rating')
            
        return percentage

    def get_averages(self, game_type=None, season=None):
        """Returns a dictionary of the player's averages"""
        return self.get_player_data(report_type='Avg', game_type=game_type, season=season)

    def get_totals(self, game_type=None, season=None):
        """Returns a dictionary of the player's totals"""
        return self.get_player_data(report_type='Sum', game_type=game_type, season=season)

    def get_player_data(self, report_type='Sum', game_type=None, season=None):
        
        qs = self.statline_set.all()
        if game_type:
            qs = qs.filter(game__game_type=game_type)
            if season:
                qs = qs.filter(game__date__range=(
                    season.start_date, season.end_date))
        
        player_data = {}
        for play in ALL_PLAY_TYPES:
            if play[0] not in ['sub_out', 'sub_in', 'misc']:
                if report_type == 'Avg':
                    x = qs.aggregate(Avg(play[0]))
                else:
                    x = qs.aggregate(Sum(play[0]))
                player_data.update(x)

        if report_type == 'Avg':
            player_data.update(qs.aggregate(
                Avg('points'),
                Avg('total_rebounds'),
                Avg('off_pos'),
                Avg('def_pos'),
                Avg('dreb_opp'),
                Avg('oreb_opp')))
        else:
            player_data.update(qs.aggregate(
                Sum('points'),
                Sum('total_rebounds'),
                Sum('off_pos'),
                Sum('def_pos'),
                Sum('dreb_opp'),
                Sum('oreb_opp')))

        player_data['gp'] = qs.count()
        return player_data

    class Meta():
        ordering = ['first_name']


def model_team1():
    return [Player.objects.get(first_name='Team1').pk]


def model_team2():
    return [Player.objects.get(first_name='Team2').pk]


class Game(models.Model):
    date = models.DateField(null=True)
    title = models.CharField(max_length=30)
    team1 = models.ManyToManyField(
        'basketball.Player', default=model_team1(), related_name='team1_set')
    team2 = models.ManyToManyField(
        'basketball.Player', default=model_team2(), related_name='team2_set')
    team1_score = models.PositiveIntegerField(
        default=0, help_text="Leave 0 if entering plays")
    team2_score = models.PositiveIntegerField(
        default=0, help_text="Leave 0 if entering plays")
    winning_players = models.ManyToManyField(
        'basketball.Player', related_name='winning_players_set', blank=True)
    youtube_id = models.CharField(
        "Youtube Video ID", max_length=2000, blank=True)
    game_type = models.CharField(max_length=30, choices=GAME_TYPES, null=True)

    def __str__(self):
        return "%s: %s" % (self.date.isoformat(), self.title)

    def get_absolute_url(self):
        return reverse("box_score", kwargs={'id': self.id})

    def calculate_game_score(self):
        """Calculates a game's score by finding the sum of points for each team's statlines
        """
        team1_statlines = StatLine.objects.filter(
            game=self, player__in=self.team1.all())
        team2_statlines = StatLine.objects.filter(
            game=self, player__in=self.team2.all())

        self.team1_score = team1_statlines.aggregate(Sum('points'))[
            'points__sum']
        self.team2_score = team2_statlines.aggregate(Sum('points'))[
            'points__sum']

        if self.team1_score > self.team2_score:
            self.winning_players = self.team1.all()
        elif self.team1_score < self.team2_score:
            self.winning_players = self.team2.all()

        self.save()

    def reset_statlines(self):
        """Resets the statlines for each player to zero accross all fields
        Usually used for when you're about to recalculate a game's stats
        """
        statlines = self.statline_set.all()
        for line in statlines:
            for play in ALL_PLAY_TYPES:
                if play[0] not in ['sub_out', 'sub_in', 'misc']:
                    setattr(line, play[0], 0)
            line.points = 0
            line.total_rebounds = 0
            line.def_pos = 0
            line.off_pos = 0
            line.dreb_opp = 0
            line.oreb_opp = 0
            line.total_pos = 0
            line.save()

    def get_bench(self):
        """Returns a list of players that start on the bench for a game.
        It does so by analyzing the subsitution plays
        """
        playbyplays = self.playbyplay_set.filter(
            primary_play="sub_out").order_by("time")
        team1_oncourt = self.team1.all().values_list('pk', flat=True)
        team2_oncourt = self.team2.all().values_list('pk', flat=True)

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
        bench = self.get_bench()
        statlines = self.statline_set.all()
        team1_statlines = statlines.filter(player__in=self.team1.all())
        team2_statlines = statlines.filter(player__in=self.team2.all())
        for play in playbyplays:
            if play.primary_play not in ['sub_out', 'sub_in', 'misc']:
                primary_line = StatLine.objects.get(
                    game=self, player=play.primary_player)
                orig_val = getattr(primary_line, play.primary_play)
                setattr(primary_line, play.primary_play, orig_val + 1)
                if play.primary_play == 'fgm':
                    primary_line.fga += 1
                    primary_line.points += 1
                elif play.primary_play == 'threepa':
                    primary_line.fga += 1
                elif play.primary_play == 'threepm':
                    primary_line.threepa += 1
                    primary_line.fga += 1
                    primary_line.fgm += 1
                    primary_line.points += 2
                primary_line.save()
                if play.primary_play in ['threepm', 'fgm', 'to']:
                    if primary_line.player in self.team1.all():
                        team1_statlines.exclude(player__pk__in=bench).update(
                            off_pos=F('off_pos') + 1)
                        team2_statlines.exclude(player__pk__in=bench).update(
                            def_pos=F('def_pos') + 1)
                    else:
                        team1_statlines.exclude(player__pk__in=bench).update(
                            def_pos=F('def_pos') + 1)
                        team2_statlines.exclude(player__pk__in=bench).update(
                            off_pos=F('off_pos') + 1)
                if play.primary_play in ['fga', 'threepa']:
                    if primary_line.player in self.team1.all():
                        team1_statlines.exclude(player__pk__in=bench).update(
                            oreb_opp=F('oreb_opp') + 1)
                        team2_statlines.exclude(player__pk__in=bench).update(
                            dreb_opp=F('dreb_opp') + 1)
                    else:
                        team1_statlines.exclude(player__pk__in=bench).update(
                            dreb_opp=F('dreb_opp') + 1)
                        team2_statlines.exclude(player__pk__in=bench).update(
                            oreb_opp=F('oreb_opp') + 1)
                # secondary play
                if play.secondary_play:
                    secondary_line = StatLine.objects.get(
                        game=self, player=play.secondary_player)
                    orig_val = getattr(secondary_line, play.secondary_play)
                    setattr(secondary_line, play.secondary_play, orig_val + 1)

                    if play.secondary_play == 'dreb' or play.secondary_play == 'oreb':
                        secondary_line.total_rebounds += 1

                    secondary_line.save()
                    if play.secondary_play == 'dreb':
                        if primary_line.player in self.team1.all():
                            team1_statlines.exclude(player__pk__in=bench).update(
                                off_pos=F('off_pos') + 1)
                            team2_statlines.exclude(player__pk__in=bench).update(
                                def_pos=F('def_pos') + 1)
                        else:
                            team1_statlines.exclude(player__pk__in=bench).update(
                                def_pos=F('def_pos') + 1)
                            team2_statlines.exclude(player__pk__in=bench).update(
                                off_pos=F('off_pos') + 1)

                # assist play
                if play.assist:
                    assist_line = StatLine.objects.get(
                        game=self, player=play.assist_player)
                    orig_val = getattr(assist_line, play.assist)
                    setattr(assist_line, play.assist, orig_val + 1)
                    assist_line.save()
            elif play.primary_play in ['sub_out', 'sub_in']:
                bench.append(play.primary_player.pk)
                bench.remove(play.secondary_player.pk)

        statlines.update(total_pos=F('off_pos') + F('def_pos'))
        self.calculate_game_score()

    class Meta():
        ordering = ['-date', 'title']


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
    dreb_opp = models.PositiveIntegerField(default=0)
    oreb_opp = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '%s - %s - %s' % (self.player.first_name, self.game.title, self.game.date.isoformat())


class PlayByPlay(models.Model):
    game = models.ForeignKey('basketball.Game')
    time = models.TimeField()
    primary_play = models.CharField(max_length=30, choices=PRIMARY_PLAY)
    primary_player = models.ForeignKey(
        'basketball.Player', related_name='primary_plays')
    secondary_play = models.CharField(
        max_length=30, choices=SECONDARY_PLAY, blank=True)
    secondary_player = models.ForeignKey(
        'basketball.Player', related_name='secondary_plays', blank=True, null=True)
    assist = models.CharField(max_length=30, choices=ASSIST_PLAY, blank=True)
    assist_player = models.ForeignKey(
        'basketball.Player', related_name='+', blank=True, null=True)
    top_play_rank = models.CharField(
        help_text="Refers to weekly rank", max_length=30, choices=RANKS, blank=True)
    top_play_players = models.ManyToManyField('basketball.Player', blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return "%s - %s - %s" % (self.primary_play, self.primary_player.first_name, self.game.title)


class Season(models.Model):
    title = models.CharField(max_length=30)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.title

    class Meta():
        ordering = ["-end_date"]
