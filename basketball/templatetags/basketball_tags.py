import datetime
from django import template
from basketball import models as bmodels
from basketball import helpers
from django.db.models import Sum, Q
from collections import OrderedDict
register = template.Library()

statistics = ['dreb', 'oreb', 'asts', 'pot_ast', 'stls', 'to', 'blk', 
    'points', 'total_rebounds', 'fgm_percent', 'threepm_percent', 
    'dreb_percent', 'oreb_percent', 'treb_percent', 'ts_percent', 
    'off_rating', 'def_rating']

@register.filter(name='access')
def access(value, arg):
    return value[arg]


@register.filter
def seconds(time):
    if time != '':
        return datetime.timedelta(hours=time.hour, minutes=time.minute, seconds=time.second).total_seconds()


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
def box_score(statlines, bgcolor="white"):
    """
    Passes a team's statlines to a template that will display them in a box score format
    """
    team_totals = {}
    for play in bmodels.ALL_PLAY_TYPES:
        if play[0] not in ['sub_out', 'sub_in', 'misc']:
            x = statlines.all().aggregate(Sum(play[0]))
            team_totals.update(x)
    team_totals.update(statlines.aggregate(
        Sum('points'), Sum('total_rebounds')))
    return {'statlines': statlines.exclude(player__first_name__contains='Team'),
            'team': statlines.get(player__first_name__contains='Team'),
            'team_totals': team_totals,
            'bgcolor': bgcolor}


@register.inclusion_tag('player_box_score.html')
def player_box_score(statlines, bgcolor="white", game_type='5v5'):
    """
    Passes a single player's statlines to a template that will display them in a table like format.
    """
    return {'statlines': statlines.filter(game__game_type=game_type), 'bgcolor': bgcolor}


@register.inclusion_tag('player_5on5_possessions.html', takes_context=True)
def player_five_on_five_pos(context, game_type="5on5", player_pk=None):
    return lb_overview(context, game_type=game_type, player_pk=player_pk)


@register.inclusion_tag('lb_overview.html', takes_context=True)
def lb_overview(context, game_type="5v5", player_pk=None):
        """Returns many lists of tuples for each statistical category"""

        season = None
        if context.get('season', None):
                season = context['season']
        possessions_min = int(context.get('possessions_min', 100))

        excluded_pks = []
        if player_pk:
                players = bmodels.Player.objects.filter(pk=player_pk)
        else:
                players = bmodels.Player.objects.all().exclude(first_name__contains="Team")

                # exclude players that dont meet the minimum 100 possessions requirement
                for player in players:
                        if player.get_possessions_count(game_type=game_type, season=season) < possessions_min:
                                excluded_pks.append(player.pk)

                players = players.exclude(pk__in=excluded_pks)
        
        top5_leaderboard = {}
        for stat in statistics:
            player_data_list = [(player.get_full_name(), player.get_per_100_possessions_data(stat, game_type, season=season))for player in players]
            if stat == 'def_rating':
                player_data_list = sorted(player_data_list, key=lambda x: x[1])
            else:
                player_data_list = sorted(player_data_list, key=lambda x: x[1], reverse=True)
            top5_leaderboard[stat] = player_data_list
        
        context = {
                "form": context.get('form', None),
                "possessions_min": possessions_min,
                "season": season,
        }
        for stat in statistics:
            context.update({stat: top5_leaderboard[stat][:5]})

        return context

@register.inclusion_tag('lb_possessions.html', takes_context=True)
def lb_possessions(context, season=None):
    """Returns every players per 100 stats for each game type""" 
   
    # Default active pill in the template.  Changes if sorting columns.
    active_pill = "5on5"

    players = bmodels.Player.objects.all().exclude(first_name__startswith="Team").order_by('first_name') 
    possessions_tables = OrderedDict()
    sort_column = context['request'].GET.get('pos-sort')
    # For each game type we create a list of each players per 100 stats
    for game_type in bmodels.GAME_TYPES:
        
        possessions_tables[game_type[1]] = []
        
        for player in players:
            
            if player.get_possessions_count(game_type=game_type[0], season=season) >= 100:
                
                player_data = {'player_obj': player}
                
                for stat in statistics:
                    
                    player_data[stat] = player.get_per_100_possessions_data(stat, game_type[0], season=season)
                
                # Lastly, count how many games the player played
                statlines = player.statline_set.filter(game__game_type=game_type[0])
                if season:
                    statlines = statlines.filter(game__date__range=(season.start_date, season.end_date))
                player_data['gp'] = statlines.count()

                possessions_tables[game_type[1]].append(player_data)

        if sort_column:
            possessions_tables[game_type[1]].sort(key=lambda d: d[sort_column], reverse=True)

    # we use this variable in our template for template readability sake
    get_string = "&default_tab=possessions&possessions_min=" + str(context['possessions_min']) + "&submit=&season="
    if season:
        get_string += str(season.id)
    
    context = {
        'possessions_tables': possessions_tables,
        'get_string': get_string,
        'pos_sort_col': sort_column,
        'active_pill': context['request'].GET.get('active-pill') or '5on5'
    }
    
    return context

@register.inclusion_tag('lb_totals_table.html', takes_context=True)
def lb_totals(context, game_type="5v5", player_pk=None, season=None):
        """Returns a dictionary of totals for one or more players"""
        
        if player_pk:
                players = bmodels.Player.objects.filter(pk=player_pk)
        else:
                players = bmodels.Player.objects.all().exclude(
                        first_name__contains="Team").order_by('first_name')

        player_totals_list = []
        totals = {}
        for player in players:

                player_total = player.get_totals(game_type=game_type,season=season)
                player_total['player_obj'] = player

                if player_total['oreb_opp__sum']:
                        player_totals_list.append(player_total)
                        for key, value in player_total.items():
                                if key is not 'player_obj':
                                        if key in totals:
                                                totals[key] += value
                                        else:
                                                totals[key] = value
        
        sort_column = context['request'].GET.get('5on5-sort')
        if sort_column:
            player_totals_list.sort(key=lambda d: d[sort_column],reverse=True)

        # we use this variable in our template for template readability sake
        get_string = "&default_tab=totals&possessions_min=" + str(context.get('possessions_min',100)) + "&submit=&season="
        if season:
            get_string += str(season.id)
        
        context = {
                'player_totals_list': player_totals_list,
                "season": season,
                "get_string": get_string,
                "possessions_min": str(context.get('possessions_min', 100)),
                "totals": totals,
                "5on5_sort_col": sort_column,
        }
        return context


@register.inclusion_tag('top_stat_table.html')
def top_players_table(player_list, title, bgcolor='white'):

    tooltip_desc = ""
    if title == "DREB":
        tooltip_desc = "Defensive Rebounds"
    elif title == "OREB":
        tooltip_desc = "Offensive Rebounds"
    elif title == "TOTAL REB":
        tooltip_desc = "Total Rebounds"
    elif title == "POT.ASSISTS":
        tooltip_desc = "Potential Assists. A pass that would’ve lead to a score if the receiver made the shot."
    elif title == "DEF.REB %":
        tooltip_desc = "Percentage of defensive rebounds grabbed against total defensive rebounds available"
    elif title == "OFF.REB %":
        tooltip_desc = "Percentage of offensive rebounds grabbed against total offensive rebounds available"
    elif title == "TOT.REB %":
        tooltip_desc = "Percentage of all rebounds grabbed against total available"
    elif title == "OFF.RATING %":
        tooltip_desc = "Points scored per 100 possessions while you’re on the floor"
    elif title == "DEF.RATING %":
        tooltip_desc = "Points scored against your per 100 possessions while you’re on the floor"
    elif title == "FG%":
        tooltip_desc = "Field Goal Percentage.  Percentage of Field Goals made"
    elif title == "3PT%":
        tooltip_desc = "3 Point Percentage. Percentage of 3pointers made"
    elif title == "TS%":
        tooltip_desc = "True Shooting Percentage. Percentage of Field Goals made with the 3 pointers weighed higher.  Formula is Points / FGA"
    elif title == "BLKS":
        tooltip_desc = "Blocks"

    return {'player_list': player_list, 'title': title, 'tooltip_desc': tooltip_desc, 'bgcolor': bgcolor}


@register.inclusion_tag('player_highlights.html')
def player_highlights(player_pk):
    top_plays = bmodels.PlayByPlay.objects.filter(
        top_play_rank__startswith='t', top_play_players__pk=player_pk)
    not_top_plays = bmodels.PlayByPlay.objects.filter(
        top_play_rank__startswith='nt', top_play_players__pk=player_pk)

    context = {
        'top_plays': top_plays,
        'not_top_plays': not_top_plays
    }
    return context
