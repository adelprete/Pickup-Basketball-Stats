import _thread
from django.db import models
from django.db.models import F, Sum, Q, Avg, signals
from django.core.urlresolvers import reverse
from django.core.exceptions import FieldError
from saturdayball import settings

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
    ('5v5', '5on5'),
    ('4v4', '4on4'),
    ('3v3', '3on3'),
    ('2v2', '2on2'),
    ('1v1', '1on1'),
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

STATS = [
    ('points', 'Points'),
    ('asts', 'Assists'),
    ('total_rebounds', 'Rebounds'),
    ('dreb', 'Defensive Rebounds'),
    ('oreb', 'Offensive Rebounds'),
    ('stls', 'Steals'),
    ('blk', 'Blocks'),
    ('fgm', 'Field Goals Made'),
    ('fga', 'Field Goals Attempted'),
    ('threepm', '3 Pointers Made'),
    ('threepa', '3 Pointers Attempted'),
    ('pot_ast', 'Potential Assists'),
    ('ba', 'Blocks Against'),
    ('pf', 'Personal Fouls'),
    ('fd', 'Fouls Drawn'),
    ('to', 'Turnovers'),
    ('ast_points', 'Assisted Points'),
    ('ast_fgm', 'Assisted Field Goals Made'),
    ('ast_fga', 'Assisted Field Goal Attempts'),
    ('unast_fgm', 'Unassisted Field Goals Made'),
    ('unast_fga', 'Unassisted Field Goal Attempts'),
    ('pgm', 'Putbacks Made'),
    ('pga', 'Putbacks Attempted'),
    ('fastbreaks', 'Fastbreaks'),
    ('fastbreak_points', 'Fastbreak Points'),
    ('second_chance_points', 'Second Chance Points'),
    ('def_pos','Defensive Possessions'),
    ('off_pos', 'Offensive Possessions'),
    ('total_pos', 'Total Possessions'),
    ('dreb_opp', 'Dreb Opportunities'),
    ('oreb_opp', 'Oreb Opportunities'),
]

class RealPlayerManager(models.Manager):
    def get_queryset(self):
        return super(RealPlayerManager, self).get_queryset().all().exclude(first_name__in=['Team1', 'Team2'])

class AllPlayerManager(models.Manager):
    use_for_related_field = True

class Player(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True)
    height = models.CharField(max_length=30, blank=True)
    weight = models.CharField(max_length=30, blank=True)
    image_src = models.ImageField(upload_to='player_images/', blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    position = models.CharField(max_length=30, blank=True)

    objects = AllPlayerManager()
    player_objs = RealPlayerManager()

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return '%s %s' % (self.first_name, self.last_name)

    def get_abbr_name(self):
        if self.last_name:
            return "%s %s." % (self.first_name, self.last_name[0])
        return "%s" % (self.first_name)

    def get_absolute_url(self):
        return reverse("player_page", kwargs={'id': self.id})

    def total_games(self, season=None):

        if season:
            return Game.objects.filter(Q(team1=self) | Q(team2=self), date__range=(season.start_date, season.end_date), exhibition=False).distinct().count()

        return Game.objects.filter(Q(team1=self) | Q(team2=self), exhibition=False).distinct().count()

    def total_wins(self, season=None):

        if season:
            return self.winning_players_set.filter(date__range=(season.start_date, season.end_date),exhibition=False).count()

        return self.winning_players_set.filter(exhibition=False).count()

    def total_losses(self, season=None):

        losses = self.total_games(season=season) - self.total_wins(season=season)

        if losses < 0:
            losses = 0

        return losses

    def get_possessions_count(self, game_type=None, season_id=None, date=None, out_of_season=False):

        season=None
        if season_id:
            season = Season.objects.get(id=season_id)

        statlines = self.statline_set.all()
        if game_type:
            statlines = statlines.filter(game__game_type=game_type)

        if season:
            statlines = statlines.filter(game__date__range=(season.start_date, season.end_date))

        if date:
            statlines = statlines.filter(game__date=date)
        else:
            statlines = statlines.filter(game__exhibition=False)

        if out_of_season:
            for season in Season.objects.all():
                statlines = statlines.exclude(game__date__range=(season.start_date, season.end_date))

        pos_count = statlines.aggregate(Sum('off_pos'))

        return pos_count['off_pos__sum'] or 0

    def get_per_100_possessions_data(self, stats_list, game_type, season_id=None, out_of_season=False, fga_min=1):
        """Returns per 100 possessions data"""
        season=None
        if season_id:
            season = Season.objects.get(id=season_id)

        data_dict = {}
        simple_statistics = [
                'dreb',
                'oreb',
                'total_rebounds',
                'asts',
                'pot_ast',
                'stls',
                'to',
                'points',
                'blk',
                'ast_fga',
                'ast_fgm',
        ]
        statlines = self.statline_set.filter(game__exhibition=False,game__game_type=game_type)
        if season:
            statlines = statlines.filter(game__date__range=(season.start_date, season.end_date))
        if out_of_season:
            for season in Season.objects.all():
                statlines = statlines.exclude(game__date__range=(season.start_date, season.end_date))

        for stat in stats_list:
            percentage = 0.0
            """Statistics from the list are calculated the same way."""
            #(stat total / offensive possessions totals) x 100
            if stat in simple_statistics:

                result = statlines.aggregate(Sum(stat), Sum('off_pos'))

                if result['off_pos__sum'] and result['off_pos__sum'] is not 0:
                    percentage = (result[stat + '__sum'] / result['off_pos__sum']) * 100


            #The following statistics have unique calculations

            #Field Goals Made % = (Field Goal Makes / Field Goal Attempts) x 100
            elif stat == "fgm_percent":
                result = statlines.aggregate(Sum('fgm'), Sum('fga'))
                if result['fga__sum'] and result['fga__sum'] is not 0 and result['fga__sum'] >= fga_min:
                    percentage = result['fgm__sum'] / result['fga__sum'] * 100

            #Assisted Field Goals Made % = (Assisted Field Goal Attempts / Field Goal Attempts) x 100
            elif stat == "ast_fga_percent":
                result = statlines.aggregate(Sum('ast_fga'), Sum('fga'))
                if result['fga__sum'] and result['fga__sum'] is not 0:
                    percentage = result['ast_fga__sum'] / result['fga__sum'] * 100

            #Assisted Field Goals Made Shooting % = (Assisted Field Goal Made / Field goal attempts) x 100
            elif stat == "ast_fgm_percent":
                result = statlines.aggregate(Sum('ast_fgm'), Sum('ast_fga'))
                if result['ast_fga__sum'] and result['ast_fga__sum'] is not 0:
                    percentage = result['ast_fgm__sum'] / result['ast_fga__sum'] * 100

            #Unassisted Field Goals Made % = (Unassisted Field Goal Attempts / Field Goal Attempts) x 100
            elif stat == "unast_fga_percent":
                result = statlines.aggregate(Sum('unast_fga'), Sum('fga'), Sum('pga'))
                if result['fga__sum'] and result['fga__sum'] is not 0:
                    percentage = (result['unast_fga__sum'] - result['pga__sum']) / result['fga__sum'] * 100

            #Unassisted Field Goals Made Shooting % = (Unassisted Field Goal Made / Field Goal Attempts) x 100
            elif stat == "unast_fgm_percent":
                result = statlines.aggregate(Sum('unast_fgm'), Sum('unast_fga'), Sum('pgm'), Sum('pga'))
                if result.get('unast_fga__sum') is not 0 and (result['unast_fga__sum'] != result['pga__sum']):
                            percentage = (result['unast_fgm__sum'] - result['pgm__sum']) / (result['unast_fga__sum'] - result['pga__sum']) * 100

            #Putback Attempt % = (Putback Attempts / Field Goals Attempts) x 100
            elif stat == 'pga_percent':
                result = statlines.aggregate(Sum('pga'), Sum('fga'))
                if result['fga__sum']:
                    percentage = result['pga__sum'] / result['fga__sum'] * 100

            #Putback Shooting % = (Putback Makes / Putbacks Attempted) x 100
            elif stat == 'pgm_percent':
                result = statlines.aggregate(Sum('pgm'), Sum('pga'))
                if result['pga__sum']:
                    percentage = result['pgm__sum'] / result['pga__sum'] * 100

            #3 Pointers Made % = (3 pointers made / 3 pointers attempts) x 100
            elif stat == 'threepm_percent':
                result = statlines.aggregate(Sum('threepm'), Sum('threepa'), Sum('off_pos'))
                if result['threepa__sum'] and result['threepa__sum'] is not 0 and result['threepa__sum'] >= fga_min:
                    percentage = result['threepm__sum'] / result['threepa__sum'] * 100

            #Defensive Rebound % = (Defensive Rebounds / Defensive Opportunities) x 100
            elif stat == 'dreb_percent':
                result = statlines.aggregate(Sum('dreb'), Sum('dreb_opp'))
                if result['dreb_opp__sum'] and result['dreb_opp__sum'] is not 0:
                    percentage = result['dreb__sum'] / result['dreb_opp__sum'] * 100

            #Offensive Rebound % = (Offensive Rebounds / Offensive Opportunities) x 100
            elif stat == 'oreb_percent':
                result = statlines.aggregate(Sum('oreb'), Sum('oreb_opp'))
                if result['oreb_opp__sum'] and result['oreb_opp__sum'] is not 0:
                    percentage = result['oreb__sum'] / result['oreb_opp__sum'] * 100

            #Total Rebound % = (Total Rebounds / (Offensive Opportunities + Defensive Opportunities)) x 100
            elif stat == 'treb_percent':
                result = statlines.aggregate(Sum('total_rebounds'), Sum('dreb_opp'), Sum('oreb_opp'))
                if result['dreb_opp__sum']:
                    percentage = result['total_rebounds__sum'] / \
                                (result['oreb_opp__sum'] + result['dreb_opp__sum']) * 100

            #True Shooting % = (Points / Field Goals Attempted) x 100
            elif stat == 'ts_percent':
                result = statlines.aggregate(Sum('points'), Sum('fga'))
                if result['fga__sum'] and result['fga__sum'] >= fga_min:
                    percentage = result['points__sum'] / result['fga__sum'] * 100

            #True Passing % = (Assisted Points / Assisted Shots) x 100
            elif stat == 'tp_percent':
                result = statlines.aggregate(Sum('ast_points'), Sum('asts'), Sum('pot_ast'))
                if result['ast_points__sum']:
                    percentage = result['ast_points__sum'] / (result['asts__sum'] + result['pot_ast__sum']) * 100

            #Offensive Rating = (Total Team Points / Offensive Possessions) x 100
            #Defensive Rating = (Total Team Points / Defensive Possessions) x 100
            elif stat == 'off_rating' or stat == 'def_rating':
                result = statlines.aggregate(Sum('off_pos'), Sum('def_pos'))

                if stat == 'off_rating':
                    team1_games = Game.objects.filter(team1=self)
                    team2_games = Game.objects.filter(team2=self)
                else:
                    team1_games = Game.objects.filter(team2=self)
                    team2_games = Game.objects.filter(team1=self)

                if season:
                    team1_games = team1_games.filter(date__range=(season.start_date, season.end_date))
                    team2_games = team2_games.filter(date__range=(season.start_date, season.end_date))

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
                print(stat)
                raise ValueError('First argument must be either dreb, oreb, asts, pot_ast, stls, to, blk, points, total_rebounds, fgm_percent, threepm_percent, dreb_percent, oreb_percent, treb_percent, ts_percent, tp_percent, pga_percent, pgm_percent, off_rating, def_rating')
            data_dict[stat] = round(percentage, 1)
        return data_dict

    def get_averages(self, stats_list, game_type=None, season=None, date=None, out_of_season=False, points_to_win=None):
        """Returns a dictionary of the player's averages"""
        return self.get_player_data(stats_list, report_type='Avg', game_type=game_type, season=season, date=date, out_of_season=out_of_season, points_to_win=points_to_win)

    def get_totals(self, stats_list, game_type=None, season=None, date=None, out_of_season=False, points_to_win=None):
        """Returns a dictionary of the player's totals"""
        return self.get_player_data(stats_list, report_type='Sum', game_type=game_type, season=season, date=date, out_of_season=out_of_season, points_to_win=points_to_win)

    def get_player_data(self, stats_list, report_type='Sum', game_type=None, season=None, date=None, out_of_season=False, points_to_win=None):

        qs = self.statline_set.all()
        if game_type:
            qs = qs.filter(game__game_type=game_type)

        if points_to_win:
            qs = qs.filter(game__points_to_win=points_to_win)

        if date:
            qs = qs.filter(game__date=date)
        else:
            qs = qs.filter(game__exhibition=False)

        if season:
            qs = qs.filter(game__date__range=(season.start_date, season.end_date))

        if out_of_season:
            for season in Season.objects.all():
                qs = qs.exclude(game__date__range=(season.start_date,season.end_date))

        data_dict = {}
        if report_type=='Sum':
            temp_data = qs.aggregate(*[Sum(stat) for stat in stats_list])
        else:
            temp_data = qs.aggregate(*[Avg(stat) for stat in stats_list])

        for stat in stats_list:
            if report_type=='Sum':
                data_dict[stat] = temp_data[stat+'__sum'] or 0
            else:
                data_dict[stat] = temp_data[stat+'__avg'] or 0

        return data_dict

    class Meta():
        ordering = ['first_name']

def update_game_record_statlines(game):

    statlines = game.statline_set.all()
    game_type = statlines[0].game.game_type

    for statline in statlines:
        record_statline = RecordStatline.objects.get_or_create(
            player=statline.player,
            game_type=game_type,
            record_type='game',
            points_to_win=game.points_to_win)[0]

        for stat in STATS:
            if getattr(statline,stat[0],0) > getattr(record_statline, stat[0], 0):
                setattr(record_statline,stat[0], getattr(statline,stat[0],0))

        record_statline.save()

    TableMatrix.objects.filter(title='day_records').update(out_of_date=True)

def update_daily_statlines(game):

    statlines = game.statline_set.all()
    date = statlines[0].game.date
    game_type = statlines[0].game.game_type

    for statline in statlines:

        stats = StatLine._meta.get_all_field_names()

        stats.remove('game')
        stats.remove('game_id')
        stats.remove('player');
        stats.remove('player_id')

        player_data = statline.player.get_totals(stats, date=date, game_type=game_type, points_to_win=game.points_to_win)

        player_data['gp'] = StatLine.objects.filter(game__date=date,
                                                    player=statline.player,
                                                    game__game_type=game.game_type,
                                                    game__points_to_win=game.points_to_win
                                                    ).count()
        player_data['player'] = statline.player
        player_data['date'] = date
        player_data['game_type'] = game_type
        player_data.pop('id', None)

        DailyStatline.objects.update_or_create(
            defaults=player_data,
            player=statline.player,
            date=date,
            game_type=game_type,
            points_to_win = game.points_to_win
        )

    TableMatrix.objects.filter(title='game_records').update(out_of_date=True)


class Game(models.Model):
    date = models.DateField(null=True)
    title = models.CharField(max_length=30)
    exhibition = models.BooleanField("Exhibition Game?", default=False, help_text="Stats for Exhibition games are NOT counted.")
    points_to_win = models.CharField(max_length=30, choices=(('11','11'), ('30','30'), ('other','Other')), default='11')
    team1 = models.ManyToManyField('basketball.Player', related_name='team1_set')
    team2 = models.ManyToManyField('basketball.Player', related_name='team2_set')
    team1_score = models.PositiveIntegerField(default=0, help_text="Leave 0 if entering plays")
    team2_score = models.PositiveIntegerField(default=0, help_text="Leave 0 if entering plays")
    winning_players = models.ManyToManyField('basketball.Player', related_name='winning_players_set', blank=True)
    youtube_id = models.CharField("Youtube Video ID", max_length=2000, blank=True)
    game_type = models.CharField(max_length=30, choices=GAME_TYPES, null=True)
    top_player = models.ForeignKey('basketball.Player', related_name='top_player_set', null=True, blank=True)

    def __str__(self):
        return "%s: %s" % (self.date.isoformat(), self.title)

    def get_full_title(self):
        title = self.title
        if self.exhibition:
            title += " (E)"
        return title

    def get_absolute_url(self):
        return reverse("box_score", kwargs={'id': self.id})

    def calculate_game_score(self):
        """Calculates a game's score by finding the sum of points for each team's statlines"""
        team1_statlines = StatLine.objects.filter(
            game=self, player__in=self.team1.all())
        team2_statlines = StatLine.objects.filter(
            game=self, player__in=self.team2.all())

        self.team1_score = team1_statlines.aggregate(Sum('points'))['points__sum']
        self.team2_score = team2_statlines.aggregate(Sum('points'))['points__sum']

        if self.team1_score > self.team2_score:
            self.winning_players = self.team1.all()
        elif self.team1_score < self.team2_score:
            self.winning_players = self.team2.all()

        self.top_player = self.get_top_player()
        self.save()

    def get_top_player(self):
        statlines = StatLine.objects.filter(game=self, player__in=self.winning_players.all()).order_by('-points','fga','to','player__first_name')
        return statlines[0].player if statlines else None

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
            line.ast_points = 0
            line.total_rebounds = 0
            line.def_pos = 0
            line.off_pos = 0
            line.dreb_opp = 0
            line.oreb_opp = 0
            line.total_pos = 0
            line.ast_fgm = 0
            line.ast_fga = 0
            line.unast_fgm = 0
            line.unast_fga = 0
            line.pgm = 0
            line.pga = 0
            line.fastbreaks = 0
            line.fastbreak_points = 0
            line.second_chance_points = 0
            line.save()

    def get_bench(self):
        """Returns a list of players that start on the bench for a game.
        It does so by analyzing the subsitution plays
        """
        playbyplays = self.playbyplay_set.filter(primary_play="sub_out").order_by("time")
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
        second_chance_window = False
        prev_play = prev_prev_play = None  #will store store previsous plays for putback and fastbreak data
        for play in playbyplays:
            if play.primary_play not in ['sub_out', 'sub_in', 'misc']:
                primary_line = StatLine.objects.get(game=self, player=play.primary_player)
                orig_val = getattr(primary_line, play.primary_play)
                setattr(primary_line, play.primary_play, orig_val + 1)

                # Analyze primary play
                if play.primary_play == 'fgm':
                    if prev_play and ((play.time - prev_play.time).seconds <= settings.PUTBACK_TIME) \
                        and prev_play.secondary_play == 'oreb' and prev_play.secondary_player == play.primary_player:
                            primary_line.pgm += 1
                            primary_line.pga += 1
                    primary_line.fga += 1
                    primary_line.points += 1
                    if second_chance_window:
                        primary_line.second_chance_points += 1
                elif play.primary_play == 'fga':
                    if prev_play and ((play.time - prev_play.time).seconds <= settings.PUTBACK_TIME) \
                        and prev_play.secondary_play == 'oreb' and prev_play.secondary_player == play.primary_player:
                            primary_line.pga += 1
                elif play.primary_play == 'threepa':
                    primary_line.fga += 1
                elif play.primary_play == 'threepm':
                    primary_line.threepa += 1
                    primary_line.fga += 1
                    primary_line.fgm += 1
                    primary_line.points += 2
                    if second_chance_window:
                        primary_line.second_chance_points += 2

                #Analyze fast breaks
                #If the previous play ended on a DREB check if a goal is made in a certain amount of time seconds
                #in case of a BLK we have to look 2 plays back for the DREB
                if (prev_play and prev_play.secondary_play in ['dreb', 'stls']) \
                    or (prev_prev_play and prev_play.primary_play == ['BLK'] and prev_prev_play.secondary_play in ['dreb']):
                        if ((play.time - prev_play.time).seconds <= settings.FASTBREAK_TIME) and play.primary_play in ['fgm', 'threepm']:
                            primary_line.fastbreaks += 1
                            if play.primary_play == 'fgm':
                                primary_line.fastbreak_points += 1
                            elif play.primary_play == 'threepm':
                                primary_line.fastbreak_points += 2

                primary_line.save()
                if play.primary_play in ['threepm', 'fgm', 'to']:
                    second_chance_window = False
                    if primary_line.player in self.team1.all():
                        team1_statlines.exclude(player__pk__in=bench).update(off_pos=F('off_pos') + 1)
                        team2_statlines.exclude(player__pk__in=bench).update(def_pos=F('def_pos') + 1)
                    else:
                        team1_statlines.exclude(player__pk__in=bench).update(def_pos=F('def_pos') + 1)
                        team2_statlines.exclude(player__pk__in=bench).update(off_pos=F('off_pos') + 1)

                if play.primary_play in ['fga', 'threepa']:
                    if primary_line.player in self.team1.all():
                        team1_statlines.exclude(player__pk__in=bench).update(oreb_opp=F('oreb_opp') + 1)
                        team2_statlines.exclude(player__pk__in=bench).update(dreb_opp=F('dreb_opp') + 1)
                    else:
                        team1_statlines.exclude(player__pk__in=bench).update(dreb_opp=F('dreb_opp') + 1)
                        team2_statlines.exclude(player__pk__in=bench).update(oreb_opp=F('oreb_opp') + 1)

                # secondary play
                if play.secondary_play:
                    secondary_line = StatLine.objects.get(game=self, player=play.secondary_player)
                    orig_val = getattr(secondary_line, play.secondary_play)
                    setattr(secondary_line, play.secondary_play, orig_val + 1)

                    if play.secondary_play == 'dreb' or play.secondary_play == 'oreb':
                        secondary_line.total_rebounds += 1
                        if play.secondary_play == 'oreb':
                            second_chance_window = True

                    secondary_line.save()
                    if play.secondary_play == 'dreb':
                        second_chance_window = False
                        if primary_line.player in self.team1.all():
                            team1_statlines.exclude(player__pk__in=bench).update(off_pos=F('off_pos') + 1)
                            team2_statlines.exclude(player__pk__in=bench).update(def_pos=F('def_pos') + 1)
                        else:
                            team1_statlines.exclude(player__pk__in=bench).update(def_pos=F('def_pos') + 1)
                            team2_statlines.exclude(player__pk__in=bench).update(off_pos=F('off_pos') + 1)

                # assist play
                if play.assist:
                    assist_line = StatLine.objects.get(game=self, player=play.assist_player)
                    orig_val = getattr(assist_line, play.assist)
                    setattr(assist_line, play.assist, orig_val + 1)

                    StatLine.objects.filter(game=self, player=play.primary_player).update(ast_fga=F('ast_fga') + 1)
                    if play.assist == 'asts':
                        StatLine.objects.filter(game=self, player=play.primary_player).update(ast_fgm=F('ast_fgm') + 1)

                        if play.primary_play == 'fgm':
                            assist_line.ast_points += 1
                        elif play.primary_play == 'threepm':
                            assist_line.ast_points += 2

                    assist_line.save()

                elif play.primary_play in ['fgm', 'threepm']:
                    StatLine.objects.filter(game=self, player=play.primary_player).update(unast_fga=F('unast_fga') + 1,unast_fgm=F('unast_fgm') + 1)
                elif play.primary_play in ['fga','threepa']:
                    StatLine.objects.filter(game=self, player=play.primary_player).update(unast_fga=F('unast_fga') + 1)

            elif play.primary_play in ['sub_out', 'sub_in']:
                bench.append(play.primary_player.pk)
                bench.remove(play.secondary_player.pk)

            prev_prev_play = prev_play
            prev_play = play

        statlines.update(total_pos=F('off_pos') + F('def_pos'))
        self.calculate_game_score()

        _thread.start_new_thread(update_daily_statlines, (self,))
        _thread.start_new_thread(update_game_record_statlines, (self,))

    def save(self):
        super(Game, self).save()

        #Delete Statlines for the those players that are no longer on either team
        game_statlines = StatLine.objects.filter(game=self)
        for statline in game_statlines:
            if statline.player not in self.team1.all() and statline.player not in self.team2.all():
                statline.delete()


    class Meta():
        ordering = ['-date', 'title']

class BaseStatline(models.Model):
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

    # advanced stats
    ast_points = models.PositiveIntegerField(default=0)
    def_pos = models.PositiveIntegerField(default=0)
    off_pos = models.PositiveIntegerField(default=0)
    total_pos = models.PositiveIntegerField(default=0)
    dreb_opp = models.PositiveIntegerField(default=0)
    oreb_opp = models.PositiveIntegerField(default=0)
    ast_fgm = models.PositiveIntegerField(default=0)
    ast_fga = models.PositiveIntegerField(default=0)
    unast_fgm = models.PositiveIntegerField(default=0)
    unast_fga = models.PositiveIntegerField(default=0)
    pga = models.PositiveIntegerField(default=0)
    pgm = models.PositiveIntegerField(default=0)
    fastbreaks = models.PositiveIntegerField(default=0)
    fastbreak_points = models.PositiveIntegerField(default=0)
    second_chance_points = models.PositiveIntegerField(default=0)

    class Meta():
        abstract=True

class StatLine(BaseStatline):
    game = models.ForeignKey('basketball.Game')

    def __str__(self):
        return '%s - %s - %s' % (self.player.first_name, self.game.title, self.game.date.isoformat())

class DailyStatline(BaseStatline):
    date = models.DateField()
    game_type = models.CharField(max_length=30, choices=GAME_TYPES)
    points_to_win = models.CharField(max_length=30, choices=(('11','11'), ('30','30'), ('other','Other')), default='11')
    gp = models.PositiveIntegerField("Games Played", default=0)

    def __str__(self):
        return '%s - %s - %s' % (self.player.first_name, "Day ", self.date)

class SeasonStatline(BaseStatline):
    season = models.ForeignKey('basketball.Season')
    game_type = models.CharField(max_length=30, choices=GAME_TYPES)
    gp = models.PositiveIntegerField("Games Played", default=0)
    points_to_win = models.CharField(max_length=30, choices=(('11', '11'), ('30', '30'), ('other', 'Other')), default='11')

    def __str__(self):
        return '%s - %s - %s' % (self.player.first_name, "Season ", self.season)

class RecordStatline(BaseStatline):
    game_type = models.CharField(max_length=30, choices=GAME_TYPES)
    record_type = models.CharField(max_length=30, choices=(('game','Game'), ('day','day'), ('season','Season')))
    points_to_win = models.CharField(max_length=30, choices=(('11','11'), ('30','30'), ('other','Other')), default='11')

    def __str__(self):
        return "%s - Game Records" % (self.player.get_full_name(),)


class PlayByPlay(models.Model):
    game = models.ForeignKey('basketball.Game')
    time = models.DurationField()
    primary_play = models.CharField(max_length=30, choices=PRIMARY_PLAY)
    primary_player = models.ForeignKey('basketball.Player', related_name='primary_plays')
    secondary_play = models.CharField(max_length=30, choices=SECONDARY_PLAY, blank=True)
    secondary_player = models.ForeignKey('basketball.Player', related_name='secondary_plays', blank=True, null=True)
    assist = models.CharField(max_length=30, choices=ASSIST_PLAY, blank=True)
    assist_player = models.ForeignKey('basketball.Player', related_name='+', blank=True, null=True)
    top_play_rank = models.CharField(help_text="Refers to weekly rank", max_length=30, choices=RANKS, blank=True)
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


class TableMatrix(models.Model):
    title = models.CharField(max_length=30)
    out_of_date = models.BooleanField(default=True)

class Cell(models.Model):
    matrix = models.ForeignKey('basketball.TableMatrix')
    row = models.PositiveIntegerField(null=True)
    column = models.PositiveIntegerField(null=True)
    value = models.CharField(max_length=80, null=True)
