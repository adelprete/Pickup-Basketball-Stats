import datetime
from django.db.models import Q, Sum
from basketball import models as bmodels
from collections import OrderedDict


def create_plays(pk, f):
    """Reads from a .csv file with a list of plays on it and creates PlayByPlay objects from the data read.
    -Takes in a game pk and a file reader.
    -Reads the file line by line and creates playbyplays
    """
    game = bmodels.Game.objects.get(pk=pk)
    game.playbyplay_set.all().delete()
    top_play_players = []
    for bline in f.readlines():
        play_dict = {}
        top_play_players = []
        line = bline.decode().split(',')

        # parse time
        time_split = line[0].split(':')
        if len(time_split) == 3:
            play_dict['time'] = datetime.timedelta(0, int(time_split[2]), 0, 0, int(time_split[1]), int(time_split[0]), )
        else:
            play_dict['time'] = datetime.timedelta(0, int(time_split[1]), 0, 0, int(time_split[0]))

        # primary play
        for play_type in bmodels.PRIMARY_PLAY:
            if play_type[1].lower() == line[1].lower():
                play_dict['primary_play'] = play_type[0]
                break

        # primary player
        play_dict['primary_player'] = bmodels.Player.objects.get(first_name=line[2].strip(),last_name=line[3].strip())

        # secondary play
        if len(line[4].strip()) > 0:
            for play_type in bmodels.SECONDARY_PLAY:
                if play_type[1].lower() == line[4].lower():
                    play_dict['secondary_play'] = play_type[0]
                    break

            # seconday player
            play_dict['secondary_player'] = bmodels.Player.objects.get(first_name=line[5].strip(),last_name=line[6].strip())

        # assist play
        if len(line[7].strip()) > 0:
            for play_type in bmodels.ASSIST_PLAY:
                if play_type[1].lower() == line[7].lower():
                    play_dict['assist'] = play_type[0]
                    break

            # assist player
            play_dict['assist_player'] = bmodels.Player.objects.get(first_name=line[8].strip(),last_name=line[9].strip())

        # Top play rank
        if len(line) > 10:
            if len(line[10].strip()) > 0:
                for choice in bmodels.RANKS:
                    if choice[1].lower() == line[7].lower():
                        play_dict['top_play_rank'] = choice[0]

                # players involved(added after mode is saved cause of M2M)
                top_players_list = [player.strip()
                                    for player in line[11].strip().split('.')]
                top_play_players = bmodels.Player.objects.filter(first_name__in=top_players_list)

                # description
                play_dict['description'] = line[12].strip()

        play = bmodels.PlayByPlay.objects.create(game=game, **play_dict)
        play.top_play_players = top_play_players
        play.save()


def per100_top_stat_players(game_type, stat, player_pk, excluded_pks, season=None):
    """
    A function that finds the top players for a given stat per 100 possessions.
    """

    if player_pk:
        players = bmodels.Player.objects.filter(pk=player_pk)
    else:
        players = bmodels.Player.objects.all().exclude(pk__in=excluded_pks)
    
    player_list = []
    for player in players:
        
        if season:
            result = player.statline_set.filter(game__exhibition=False,game__game_type=game_type, game__date__range=(season.start_date, season.end_date)).aggregate(Sum(stat), Sum('off_pos'))
        else:
            result = player.statline_set.filter(game__exhibition=False,game__game_type=game_type).aggregate(Sum(stat), Sum('off_pos'))
        if result['off_pos__sum'] and result['off_pos__sum'] is not 0:
            percentage = (result[stat + '__sum'] / result['off_pos__sum']) * 100
        else:
            percentage = 0.0
        
        player_list.append((player.first_name, percentage))
    
    return sorted(player_list, key=lambda x: x[1], reverse=True)

def recap_totals_dictionaries(statistics, player_ids, date=None, sort_column=""):

    players = bmodels.Player.objects.filter(id__in=player_ids).order_by('first_name')

    totals_tables = OrderedDict()
    totals_footer = {}
    # For each game type we create a list of each player's total stats
    for game_type in bmodels.GAME_TYPES:
        totals_tables[game_type[1]] = []
        totals = {}
        for player in players:
		   
            if player.get_possessions_count(game_type=game_type[0], date=date) > 0:
                player_data = {'player_obj': player}
				
                stats_list = [header['stat'] for header in statistics if header['stat'] != 'gp']
                player_data.update(player.get_totals(stats_list, game_type=game_type[0], date=date))

                # Lastly, count how many games the player played
                statlines = player.statline_set.filter(game__game_type=game_type[0], game__date=date)
                player_data['gp'] = statlines.count()

                totals_tables[game_type[1]].append(player_data)
                for key, value in player_data.items():
                    if key is not 'player_obj':
                        if key in totals:
                            totals[key] += value
                        else:
                            totals[key] = value

        totals_footer[game_type[1]] = totals

        if sort_column:
            totals_tables[game_type[1]].sort(key=lambda d: d[sort_column], reverse=True)

    return totals_tables, totals_footer


def update_game_record_statlines(game):

    statlines = game.statline_set.all()
    game_type = statlines[0].game.game_type

    for statline in statlines:
        record_statline = bmodels.RecordStatline.objects.get_or_create(
            player=statline.player,
            game_type=game_type,
            record_type='game',
            points_to_win=game.points_to_win)[0]

        for stat in bmodels.STATS:
            if getattr(statline,stat[0],0) > getattr(record_statline, stat[0], 0):
                setattr(record_statline,stat[0], getattr(statline,stat[0],0))

        record_statline.save()

    try:
        season = bmodels.Season.objects.get(start_date__lte=game.date, end_date__gte=game.date)
        bmodels.TableMatrix.objects.filter(type='game_records', season=season).update(out_of_date=True)
    except:
        pass

    bmodels.TableMatrix.objects.filter(type='game_records', season=None).update(out_of_date=True)


def update_daily_statlines(game):

    statlines = game.statline_set.all()
    if statlines:
        date = statlines[0].game.date
        game_type = statlines[0].game.game_type

        for statline in statlines:
            stats = [stat[0] for stat in bmodels.STATS]

            player_data = statline.player.get_totals(stats, date=date, game_type=game_type, points_to_win=game.points_to_win)

            player_data['gp'] = bmodels.StatLine.objects.filter(game__date=date,
                                                        player=statline.player,
                                                        game__game_type=game.game_type,
                                                        game__points_to_win=game.points_to_win
                                                        ).count()
            player_data['player'] = statline.player
            player_data['date'] = date
            player_data['game_type'] = game_type
            player_data.pop('id', None)

            bmodels.DailyStatline.objects.update_or_create(
                defaults=player_data,
                player=statline.player,
                date=date,
                game_type=game_type,
                points_to_win = game.points_to_win
            )
        try:
            season = bmodels.Season.objects.get(start_date__lte=date, end_date__gte=date)
            bmodels.TableMatrix.objects.filter(type='day_records', season=season).update(out_of_date=True)
        except:
            pass
        bmodels.TableMatrix.objects.filter(type='day_records', season=None).update(out_of_date=True)

def update_season_statlines(game):

    statlines = game.statline_set.all()
    if statlines:
        date = statlines[0].game.date
        game_type = statlines[0].game.game_type
        try:
            season = bmodels.Season.objects.get(start_date__lte=date, end_date__gte=date)
        except:
            pass
        else:
            for statline in statlines:

                stats = [stat[0] for stat in bmodels.STATS]

                player_data = statline.player.get_totals(stats, game_type=game_type, season=season, points_to_win=game.points_to_win)

                player_data['gp'] = bmodels.StatLine.objects.filter(game__date__range=(season.start_date, season.end_date),
                                                                 player=statline.player,
                                                                 game__game_type=game.game_type,
                                                                 game__points_to_win=game.points_to_win
                                                                 ).count()

                player_data.pop('id', None)

                bmodels.SeasonStatline.objects.update_or_create(
                    defaults=player_data,
                    player=statline.player,
                    game_type=game_type,
                    season=season,
                    points_to_win = game.points_to_win
                )

            bmodels.TableMatrix.objects.filter(type='season_records').update(out_of_date=True)


def update_season_per100_statlines(game):

    statlines = game.statline_set.all()
    if statlines:
        date = statlines[0].game.date
        game_type = statlines[0].game.game_type

        try:
            season = bmodels.Season.objects.get(start_date__lte=date, end_date__gte=date)
        except:
            pass
        else:

            stats = bmodels.SeasonPer100Statline._meta.get_all_field_names()
            stats.remove('id')
            stats.remove('season')
            stats.remove('season_id')
            stats.remove('player')
            stats.remove('player_id')
            stats.remove('game_type')
            stats.remove('points_to_win')

            for statline in statlines:

                player_data = statline.player.get_per_100_possessions_data(stats, game_type=game_type, season_id=season.id, points_to_win=game.points_to_win)

                player_data['gp'] = bmodels.StatLine.objects.filter(game__date__range=(season.start_date, season.end_date),
                                                                 player=statline.player,
                                                                 game__game_type=game.game_type,
                                                                 game__points_to_win=game.points_to_win
                                                                 ).count()

                bmodels.SeasonPer100Statline.objects.update_or_create(
                    defaults=player_data,
                    player=statline.player,
                    game_type=game_type,
                    season=season,
                    points_to_win = game.points_to_win
                )

            bmodels.TableMatrix.objects.filter(type='season_per100_records',points_to_win=game.points_to_win).update(out_of_date=True)