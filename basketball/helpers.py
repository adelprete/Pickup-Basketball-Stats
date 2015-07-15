import datetime
from django.db.models import Q, Sum
from basketball import models as bmodels

def create_plays(pk,f):
    """Reads from a .csv file with a list of plays on it and creates PlayByPlay objects from the data read.
    -Takes in a game pk and a file reader.
    -Reads the file line by line and creates playbyplays
    """
    game = bmodels.Game.objects.get(pk=pk)
    game.playbyplay_set.all().delete()
    for bline in f.readlines():
        play_dict = {}
        line = bline.decode().split(',')

        #parse time
        time_split = line[0].split(':')
        if len(time_split) == 3:
            play_dict['time'] = datetime.time(int(time_split[0]),int(time_split[1]),int(time_split[2]))
        else:
            play_dict['time'] = datetime.time(0,int(time_split[0]),int(time_split[1]))

        #primary play
        for play_type in bmodels.PRIMARY_PLAY:
            if play_type[1].lower() == line[1].lower():
                play_dict['primary_play'] = play_type[0]
                break

        #primary player
        play_dict['primary_player'] = bmodels.Player.objects.get(first_name=line[2])

        #secondary play
        if len(line[3].strip()) > 0:
            for play_type in bmodels.SECONDARY_PLAY:
                if play_type[1].lower() == line[3].lower():
                    play_dict['secondary_play'] = play_type[0]
                    break

            #seconday player
            play_dict['secondary_player'] = bmodels.Player.objects.get(first_name=line[4])

        #assist play
        if len(line[5].strip()) > 0:
            for play_type in bmodels.ASSIST_PLAY:
                if play_type[1].lower() == line[5].lower():
                    play_dict['assist'] = play_type[0]
                    break

            #assist player
            play_dict['assist_player'] = bmodels.Player.objects.get(first_name=line[6].strip())
        
        bmodels.PlayByPlay.objects.create(game=game,**play_dict)


def per100_top_stat_players(game_type,stat,excluded_pks):
    """
    A function that finds the top players for a given stat per 100 possessions.
    """
    players = bmodels.Player.objects.all().exclude(Q(first_name__contains="Team")|Q(pk__in=excluded_pks))
    player_list = []
    for player in players:
        result = player.statline_set.filter(game__game_type=game_type).aggregate(Sum(stat),Sum('off_pos'))
        if result['off_pos__sum'] is not 0:
            percentage = (result[stat + '__sum']/result['off_pos__sum']) * 100
        else:
            percentage = 0.0
        player_list.append((player.first_name,percentage))
    return sorted(player_list,key=lambda x: x[1],reverse=True)

