import datetime
from django.db.models import Q, Sum
from basketball import models as bmodels


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
            play_dict['time'] = datetime.time(
                int(time_split[0]), int(time_split[1]), int(time_split[2]))
        else:
            play_dict['time'] = datetime.time(
                0, int(time_split[0]), int(time_split[1]))

        # primary play
        for play_type in bmodels.PRIMARY_PLAY:
            if play_type[1].lower() == line[1].lower():
                play_dict['primary_play'] = play_type[0]
                break

        # primary player
        play_dict['primary_player'] = bmodels.Player.objects.get(first_name=line[
                                                                 2])

        # secondary play
        if len(line[3].strip()) > 0:
            for play_type in bmodels.SECONDARY_PLAY:
                if play_type[1].lower() == line[3].lower():
                    play_dict['secondary_play'] = play_type[0]
                    break

            # seconday player
            play_dict['secondary_player'] = bmodels.Player.objects.get(first_name=line[
                                                                       4])

        # assist play
        if len(line[5].strip()) > 0:
            for play_type in bmodels.ASSIST_PLAY:
                if play_type[1].lower() == line[5].lower():
                    play_dict['assist'] = play_type[0]
                    break

            # assist player
            play_dict['assist_player'] = bmodels.Player.objects.get(
                first_name=line[6].strip())

        # Top play rank
        if len(line) > 7:
            if len(line[7].strip()) > 0:
                for choice in bmodels.RANKS:
                    if choice[1].lower() == line[7].lower():
                        play_dict['top_play_rank'] = choice[0]

                # players involved(added after mode is saved cause of M2M)
                top_players_list = [player.strip()
                                    for player in line[8].strip().split('.')]
                top_play_players = bmodels.Player.objects.filter(
                    first_name__in=top_players_list)

                # description
                play_dict['description'] = line[9].strip()

        play = bmodels.PlayByPlay.objects.create(game=game, **play_dict)
        play.top_play_players = top_play_players
        play.save()


def per100_top_stat_players(game_type, stat, player_pk, excluded_pks, season_id=None):
    """
    A function that finds the top players for a given stat per 100 possessions.
    """
    season = None
    if season_id:
        season = bmodels.Season.objects.get(id=season_id)

    if player_pk:
        players = bmodels.Player.objects.filter(pk=player_pk)
    else:
        players = bmodels.Player.objects.all().exclude(
            Q(first_name__contains="Team") | Q(pk__in=excluded_pks))
    player_list = []
    for player in players:
        if season:
            result = player.statline_set.filter(game__game_type=game_type, game__date__range=(
                season.start_date, season.end_date)).aggregate(Sum(stat), Sum('off_pos'))
        else:
            result = player.statline_set.filter(
                game__game_type=game_type).aggregate(Sum(stat), Sum('off_pos'))
        if result['off_pos__sum'] and result['off_pos__sum'] is not 0:
            percentage = (result[stat + '__sum'] /
                          result['off_pos__sum']) * 100
        else:
            percentage = 0.0
        player_list.append((player.first_name, percentage))
    return sorted(player_list, key=lambda x: x[1], reverse=True)
