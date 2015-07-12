from django import template
from basketball import models as bmodels
from django.db.models import Sum

register = template.Library()

@register.inclusion_tag('box_score.html')
def box_score(statlines,bgcolor="white"):
        team_totals = {}
        for play in bmodels.ALL_PLAY_TYPES:
            if play[0] not in ['sub_out','sub_in']:
                x = statlines.exclude(player__first_name__contains='Team').aggregate(Sum(play[0]))
                team_totals.update(x)
        team_totals.update(statlines.aggregate(Sum('points'),Sum('total_rebounds')))
        return {'statlines': statlines.exclude(player__first_name__contains='Team'),
                'team': statlines.get(player__first_name__contains='Team'),
                'team_totals':team_totals,
                'bgcolor':bgcolor}

@register.inclusion_tag('player_box_score.html')
def player_box_score(statlines,bgcolor="white"):
	return {'statlines': statlines,'bgcolor':bgcolor}

def top_stat_players(game_type,stat):
    players = bmodels.Player.objects.all()
    player_list = []
    for player in players:
        result = player.statline_set.filter(game__game_type=game_type).aggregate(Sum(stat),Sum('off_pos'))
        if result['off_pos__sum'] is not 0:
            percentage = (result[stat + '__sum']/result['off_pos__sum']) * 100
        else:
            percentage = 0.0
        player_list.append((player.first_name,percentage))
    return sorted(player_list,key=lambda x: x[1],reverse=True)

@register.inclusion_tag('5on5_possessions.html')
def five_on_five_pos():
    
    players = bmodels.Player.objects.all().exclude(first_name__in=["Team1","Team2"])

    dreb = top_stat_players('5v5','dreb')
    oreb = top_stat_players('5v5','oreb')  
    total_rebounds = top_stat_players('5v5','total_rebounds')
    asts = top_stat_players('5v5','asts')
    pot_ast = top_stat_players('5v5','pot_ast')
    stls = top_stat_players('5v5','stls')
    to = top_stat_players('5v5','to')
    points = top_stat_players('5v5','points')

    #these need special attention
    fgm_percent = []
    for player in players:
        result = player.statline_set.filter(game__game_type='5v5').aggregate(Sum('fgm'),Sum('fga'),Sum('off_pos'))
        if result['fga__sum'] is not 0 and result['off_pos__sum'] is not 0:
            percentage = ( (result['fgm__sum']/result['fga__sum']) / result['off_pos__sum'] ) * 100
        else:
            percentage = 0.0
        fgm_percent.append((player.first_name,percentage))
    fgm_percent = sorted(fgm_percent,key=lambda x: x[1],reverse=True)
   
    three_percent = []
    for player in players:
        result = player.statline_set.filter(game__game_type='5v5').aggregate(Sum('threepm'),Sum('threepa'),Sum('off_pos'))
        if result['threepa__sum'] is not 0 and result['off_pos__sum'] is not 0:
            percentage = ( (result['threepm__sum']/result['threepa__sum']) / result['off_pos__sum'] ) * 100
        else:
            percentage = 0.0
        three_percent.append((player.first_name,percentage))
    three_percent = sorted(three_percent,key=lambda x: x[1],reverse=True)

    dreb_percent = []
    for player in players:
        result = player.statline_set.filter(game__game_type='5v5').aggregate(Sum('dreb'),Sum('total_rebounds'),Sum('def_pos'))
        if result['total_rebounds__sum'] is not 0 and result['def_pos__sum'] is not 0:
            percentage = ( (result['dreb__sum']/result['total_rebounds__sum']) / result['def_pos__sum'] ) * 100
        else:
            percentage = 0.0
        dreb_percent.append((player.first_name,percentage))
    dreb_percent = sorted(dreb_percent,key=lambda x: x[1],reverse=True)

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
    }
    return context

@register.inclusion_tag('top_stat_table.html')
def top_players_table(player_list,title,bgcolor='white'):
    return {'player_list':player_list,'title':title,'bgcolor':bgcolor}
