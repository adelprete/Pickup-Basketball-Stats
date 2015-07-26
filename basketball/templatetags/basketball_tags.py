import datetime
from django import template
from basketball import models as bmodels
from basketball import helpers
from django.db.models import Sum, Q
from collections import OrderedDict
register = template.Library()


@register.filter
def seconds(time):
    if time != '':
        return datetime.timedelta(hours=time.hour,minutes=time.minute,seconds=time.second).total_seconds()

@register.filter
def top_play_check(rank):
    if rank and rank[0] == 't':
        return True
    else:
        return False

@register.filter
def not_top_play_check(rank):
    if rank and rank[0] == 'n':
        return True
    else:
        return False

@register.inclusion_tag('box_score.html')
def box_score(statlines,bgcolor="white"):
    """
    Passes a team's statlines to a template that will display them in a box score format
    """
    team_totals = {}
    for play in bmodels.ALL_PLAY_TYPES:
        if play[0] not in ['sub_out','sub_in','misc']:
            x = statlines.all().aggregate(Sum(play[0]))
            team_totals.update(x)
    team_totals.update(statlines.aggregate(Sum('points'),Sum('total_rebounds')))
    return {'statlines': statlines.exclude(player__first_name__contains='Team'),
            'team': statlines.get(player__first_name__contains='Team'),
            'team_totals':team_totals,
            'bgcolor':bgcolor}

@register.inclusion_tag('player_box_score.html')
def player_box_score(statlines,bgcolor="white",game_type='5v5'):
    """
    Passes a single player's statlines to a template that will display them in a table like format.
    """
    return {'statlines': statlines.filter(game__game_type=game_type),'bgcolor':bgcolor}


@register.inclusion_tag('lb_5on5_possessions.html')
def lb_five_on_five_pos(game_type="5on5"):
    
    players = bmodels.Player.objects.all().exclude(first_name__contains="Team")

    #exclude players that dont meet the minimum 100 possessions requirement
    excluded_pks = []
    for player in players:
        pos_count = player.statline_set.filter(game__game_type=game_type).aggregate(Sum('off_pos'))
        if not pos_count['off_pos__sum'] or pos_count['off_pos__sum'] < 100:
            excluded_pks.append(player.pk)

    players = players.exclude(pk__in=excluded_pks)

    dreb = helpers.per100_top_stat_players(game_type,'dreb',excluded_pks)
    oreb = helpers.per100_top_stat_players(game_type,'oreb',excluded_pks)  
    total_rebounds = helpers.per100_top_stat_players(game_type,'total_rebounds',excluded_pks)
    asts = helpers.per100_top_stat_players(game_type,'asts',excluded_pks)
    pot_ast = helpers.per100_top_stat_players(game_type,'pot_ast',excluded_pks)
    stls = helpers.per100_top_stat_players(game_type,'stls',excluded_pks)
    to = helpers.per100_top_stat_players(game_type,'to',excluded_pks)
    points = helpers.per100_top_stat_players(game_type,'points',excluded_pks)
    blk = helpers.per100_top_stat_players(game_type,'blk',excluded_pks)

    #these need special attention
    fgm_percent = []
    for player in players:
        result = player.statline_set.filter(game__game_type=game_type).aggregate(Sum('fgm'),Sum('fga'))
        if result['fga__sum'] is not 0:
            percentage = result['fgm__sum']/result['fga__sum'] * 100
        else:
            percentage = 0.0
        fgm_percent.append((player.first_name,percentage))
    fgm_percent = sorted(fgm_percent,key=lambda x: x[1],reverse=True)
   
    three_percent = []
    for player in players:
        result = player.statline_set.filter(game__game_type=game_type).aggregate(Sum('threepm'),Sum('threepa'),Sum('off_pos'))
        if result['threepa__sum'] is not 0:
            percentage = result['threepm__sum']/result['threepa__sum'] * 100
        else:
            percentage = 0.0
        three_percent.append((player.first_name,percentage))
    three_percent = sorted(three_percent,key=lambda x: x[1],reverse=True)

    dreb_percent = []
    for player in players:
        result = player.statline_set.filter(game__game_type=game_type).aggregate(Sum('dreb'),Sum('dreb_opp'))
        if result['dreb_opp__sum'] is not 0:
            percentage = result['dreb__sum']/result['dreb_opp__sum'] * 100
        else:
            percentage = 0.0
        dreb_percent.append((player.first_name,percentage))
    dreb_percent = sorted(dreb_percent,key=lambda x: x[1],reverse=True)
    
    oreb_percent = []
    for player in players:
        result = player.statline_set.filter(game__game_type=game_type).aggregate(Sum('oreb'),Sum('oreb_opp'))
        if result['oreb_opp__sum'] is not 0:
            percentage = result['oreb__sum']/result['oreb_opp__sum'] * 100
        else:
            percentage = 0.0
        oreb_percent.append((player.first_name,percentage))
    oreb_percent = sorted(oreb_percent,key=lambda x: x[1],reverse=True)

    treb_percent = []
    for player in players:
        result = player.statline_set.filter(game__game_type=game_type).aggregate(Sum('total_rebounds'),Sum('dreb_opp'),Sum('oreb_opp'))
        percentage = result['total_rebounds__sum']/(result['oreb_opp__sum']+result['dreb_opp__sum']) * 100
        treb_percent.append((player.first_name,percentage))
    treb_percent = sorted(treb_percent,key=lambda x: x[1],reverse=True)

    ts_percent = []
    for player in players:
        result = player.statline_set.filter(game__game_type=game_type).aggregate(Sum('points'),Sum('fga'))
        percentage = result['points__sum']/result['fga__sum'] * 100
        ts_percent.append((player.first_name,percentage))
    ts_percent = sorted(ts_percent,key=lambda x: x[1],reverse=True)

    orating_percent = []
    for player in players:
        result = player.statline_set.filter(game__game_type=game_type).aggregate(Sum('off_pos'))
        team1_result = bmodels.Game.objects.filter(team1=player).aggregate(Sum('team1_score'))
        team2_result = bmodels.Game.objects.filter(team2=player).aggregate(Sum('team2_score'))
        if team1_result['team1_score__sum'] == None:
            team1_result['team1_score__sum'] = 0
        if team2_result['team2_score__sum'] == None:
            team2_result['team2_score__sum'] = 0
        percentage = (team1_result['team1_score__sum']+team2_result['team2_score__sum'])/result['off_pos__sum'] * 100
        orating_percent.append((player.first_name,percentage))
    orating_percent = sorted(orating_percent,key=lambda x: x[1],reverse=True)

    drating_percent = []
    for player in players:
        result = player.statline_set.filter(game__game_type=game_type).aggregate(Sum('def_pos'))
        team1_result = bmodels.Game.objects.filter(team2=player).aggregate(Sum('team1_score'))
        team2_result = bmodels.Game.objects.filter(team1=player).aggregate(Sum('team2_score'))
        if team1_result['team1_score__sum'] == None:
            team1_result['team1_score__sum'] = 0
        if team2_result['team2_score__sum'] == None:
            team2_result['team2_score__sum'] = 0
        percentage = (team1_result['team1_score__sum']+team2_result['team2_score__sum'])/result['def_pos__sum'] * 100
        drating_percent.append((player.first_name,percentage))
    drating_percent = sorted(drating_percent,key=lambda x: x[1])

    context = {
            "dreb":dreb[:5],
            "oreb":oreb[:5],
            "total_rebounds":total_rebounds[:5],
            "asts":asts[:5],
            "pot_ast":pot_ast[:5],
            "stls":stls[:5],
            "to":to[:5],
            "points":points[:5],
            "fgm_percent":fgm_percent[:5],
            "three_percent":three_percent[:5],
            "dreb_percent":dreb_percent[:5],
            "oreb_percent":oreb_percent[:5],
            "treb_percent":treb_percent[:5],
            "ts_percent":ts_percent[:5],
            "orating_percent":orating_percent[:5],
            "drating_percent":drating_percent[:5],
            "blk":blk[:5],
    }
    return context

@register.inclusion_tag('lb_totals.html')
def lb_5on5_totals():
    
    players = bmodels.Player.objects.all().exclude(first_name__contains="Team").order_by('first_name')
    player_dict = OrderedDict()
    for player in players:
        player_total = player.statline_set.filter(game__game_type='5v5').aggregate(\
                Sum('fga'),Sum('fgm'),Sum('threepm'),Sum('threepa'),\
                Sum('dreb'),Sum('oreb'),Sum('total_rebounds'),Sum('asts'),\
                Sum('pot_ast'),Sum('blk'),Sum('ba'),Sum('stls'),\
                Sum('to'),Sum('fd'),Sum('pf'),Sum('def_pos'),\
                Sum('off_pos'),Sum('points'),Sum('dreb_opp'),Sum('oreb_opp'))
        player_dict[player.get_full_name()] = player_total

    context = {
            'player_dict':player_dict,
    }
    return context

@register.inclusion_tag('top_stat_table.html')
def top_players_table(player_list,title,bgcolor='white'):
    return {'player_list':player_list,'title':title,'bgcolor':bgcolor}
