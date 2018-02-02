import datetime
from django import template
from basketball import models as bmodels
from basketball import helpers, headers
from django.db.models import Sum, Q
from collections import OrderedDict
register = template.Library()


@register.filter(name='access')
def access(value, arg):
    return value[arg]

@register.filter(name='getattribute')
def getattribute(obj, attr):
	return getattr(obj,attr)

@register.filter
def formattime(time):
    time_str = "%02d:%02d" % (int((time.seconds / 60) % 60), int(time.seconds % 60))
    hour = ""
    if time.seconds/3600 >= 1:
        hour = "%02d:" % (int(time.seconds / 3600))
    return hour + time_str

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

@register.inclusion_tag('games/game_snippet.html')
def game_snippet(game):

    top_statline = bmodels.StatLine.objects.filter(game=game,player=game.top_player)

    context = {
        'game': game,
        'statline': top_statline[0] if top_statline else None
    }
    return context

@register.inclusion_tag('games/box_scores_table.html')
def box_score(statlines, bgcolor="white"):
    """
    Passes a team's statlines to a template that will display them in a box score format
    """
    team_totals = {}
    for play in bmodels.ALL_PLAY_TYPES:
        if play[0] not in ['sub_out', 'sub_in', 'misc']:
            x = statlines.all().aggregate(Sum(play[0]))
            team_totals.update(x)
    team_totals.update(statlines.aggregate(Sum('points'), Sum('total_rebounds')))
    return {'statlines': statlines.exclude(player__first_name__contains='Team'),
            'team': statlines.get(player__first_name__contains='Team'),
            'team_totals': team_totals,
            'bgcolor': bgcolor}

@register.inclusion_tag('games/adv_box_scores_table.html')
def adv_box_score(statlines, bgcolor="white"):
    """
    Passes a team's statlines to a template that will display them in a box score format
    """
    team_totals = {}
    for stat in ['pga','pgm', 'fastbreak_points', 'ast_fgm', 'ast_fga',
		'unast_fgm', 'unast_fga', 'ast_points', 'second_chance_points']:
        x = statlines.all().aggregate(Sum(stat))
        team_totals.update(x)

    return {'statlines': statlines.exclude(player__first_name__contains='Team'),
            'team': statlines.get(player__first_name__contains='Team'),
            'team_totals': team_totals,
            'bgcolor': bgcolor}

@register.inclusion_tag('leaderboard/overview.html', takes_context=True)
def lb_overview(context, game_type="5v5", player_pk=None):
        """Returns many lists of tuples for each statistical category"""
        overview_statistics = ['dreb', 'oreb', 'asts', 'pot_ast', 'stls', 'to', 'blk',
            'points', 'total_rebounds', 'fgm_percent', 'threepm_percent',
            'dreb_percent', 'oreb_percent', 'treb_percent', 'ts_percent',
            'off_rating', 'def_rating', 'tp_percent']

        group = context.get('group', None)
        season_id = None
        season = None
        if context.get('season', None):
            season = context['season']
            season_id = season.id
        possessions_min = int(context.get('possessions_min', group.possessions_min))

        excluded_pks = []
        if player_pk:
                players = bmodels.Player.objects.filter(pk=player_pk)
        else:
                players = bmodels.Player.player_objs.filter(group=group)

                # exclude players that dont meet the minimum 100 possessions requirement
                for player in players:
                        if player.get_possessions_count(game_type=game_type, season_id=season_id) < possessions_min:
                                excluded_pks.append(player.pk)

                players = players.exclude(pk__in=excluded_pks)

        top5_leaderboard = {}
        for stat in overview_statistics:

            player_data_list = [
                    (player.get_abbr_name(),
                    round(player.get_per_100_possessions_data([stat], game_type, season_id=season_id, fga_min=group.fga_min)[stat],1)) for player in players
                    ]
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
        for stat in overview_statistics:
            context.update({stat: top5_leaderboard[stat][:5]})

        return context

def calculate_lb_possessions_dictionaries(context, headers, season_id=None, sort_column=""):

    group = context.get('group', None)

    players = bmodels.Player.player_objs.filter(group__id=group.id).order_by('first_name')
    season = None
    if season_id:
        season = bmodels.Season.objects.get(id=season_id)

    possessions_tables = OrderedDict()
    possessions_min = int(context.get('possessions_min', group.possessions_min))

    # For each game type we create a list of each player's per 100 stats
    for game_type in bmodels.GAME_TYPES:

        possessions_tables[game_type[1]] = []

        for player in players:

            if player.get_possessions_count(game_type=game_type[0], season_id=season_id) >= possessions_min:
                player_data = {'player_obj': player}
                stats_list = [header['stat'] for header in headers if header['stat'] != 'gp']
                player_data.update(player.get_per_100_possessions_data(stats_list, game_type[0], season_id=getattr(season,'id',None)))

                # Lastly, count how many games the player played
                statlines = player.statline_set.filter(game__exhibition=False, game__game_type=game_type[0], game__published=True)
                if season:
                    statlines = statlines.filter(game__date__range=(season.start_date, season.end_date))
                player_data['gp'] = statlines.count()

                possessions_tables[game_type[1]].append(player_data)

        if sort_column:
            possessions_tables[game_type[1]].sort(key=lambda d: d[sort_column], reverse=True)

        if not possessions_tables[game_type[1]]:
            del possessions_tables[game_type[1]];

    return possessions_tables


@register.inclusion_tag('leaderboard/adv_possessions.html', takes_context=True)
def lb_adv_possessions(context, season=None):
    """Returns every players per 100 stats for each game type"""
    sort_column = context['request'].GET.get('adv_pos_sort')

    possessions_tables = calculate_lb_possessions_dictionaries(context,headers.adv_per_100_statistics, season_id=getattr(season,'id',None),sort_column=sort_column)

    # we use this variable in our template for template readability sake
    get_string = "&default_tab=adv_possessions&possessions_min=" + str(context['possessions_min']) + "&submit=&season="
    if season:
        get_string += str(season.id)

    context = {
        'tables': possessions_tables,
        'get_string': get_string,
        'pos_sort_col': sort_column,
        'active_pill': context['request'].GET.get('adv_pos_active_pill') or '5on5',
        'headers': headers.adv_per_100_statistics,
    }
    return context

@register.inclusion_tag('leaderboard/possessions.html', takes_context=True)
def lb_possessions(context, season=None):
    """Returns every players per 100 stats for each game type"""
    sort_column = context['request'].GET.get('pos_sort')

    possessions_tables = calculate_lb_possessions_dictionaries(context,headers.per_100_statistics, season_id=getattr(season,'id',None),sort_column=sort_column)

    # we use this variable in our template for template readability sake
    get_string = "&default_tab=possessions&possessions_min=" + str(context['possessions_min']) + "&submit=&season="
    if season:
        get_string += str(season.id)

    context = {
        'tables': possessions_tables,
        'get_string': get_string,
        'pos_sort_col': sort_column,
        'active_pill': context['request'].GET.get('pos_active_pill') or '5on5',
        'headers': headers.per_100_statistics,
    }

    return context

def calculate_lb_totals_dictionaries(context, statistics, season_id=None, sort_column="",):

        group = context.get('group', None)

        players = bmodels.Player.player_objs.filter(group__id=group.id).order_by('first_name')

        season = None
        if season_id:
            season = bmodels.Season.objects.get(id=season_id)
        totals_tables = OrderedDict()
        totals_footer = {}
        # For each game type we create a list of each player's total stats
        for game_type in bmodels.GAME_TYPES:
            totals_tables[game_type[1]] = []
            totals = {}
            for player in players:

                if player.get_possessions_count(game_type=game_type[0], season_id=season_id) > 0:
                    player_data = {'player_obj': player}

                    stats_list = [header['stat'] for header in statistics if header['stat'] != 'gp']
                    player_data.update(player.get_totals(stats_list, game_type=game_type[0], season=season))

                    # Lastly, count how many games the player played
                    statlines = player.statline_set.filter(game__game_type=game_type[0],game__exhibition=False, game__published=True)
                    if season:
                        statlines = statlines.filter(game__date__range=(season.start_date, season.end_date))
                    player_data['gp'] = statlines.count()

                    totals_tables[game_type[1]].append(player_data)
                    for key, value in player_data.items():
                        if key is not 'player_obj':
                            if key in totals:
                                totals[key] += value
                            else:
                                totals[key] = value
            if not totals_tables[game_type[1]]:
                del totals_tables[game_type[1]];
            totals_footer[game_type[1]] = totals

            if sort_column:
                totals_tables[game_type[1]].sort(key=lambda d: d[sort_column], reverse=True)

        return totals_tables, totals_footer

@register.inclusion_tag('leaderboard/adv_totals.html', takes_context=True)
def lb_adv_totals(context, game_type="5v5", season=None):
    """Returns a dictionary of advanced totals for all players"""
    sort_column = context['request'].GET.get('adv_tot_sort')

    totals_tables, totals_footer = calculate_lb_totals_dictionaries(context,headers.adv_totals_statistics[1:],season_id=getattr(season,'id',None),sort_column=sort_column)

    # we use this variable in our template for template readability sake
    get_string = "&default_tab=adv_totals&possessions_min=" + str(context['possessions_min']) + "&submit=&season="
    if season:
        get_string += str(season.id)

    active_pill = context['request'].GET.get('adv_tot_active_pill') or '5on5'

    context = {
        'tables': totals_tables,
        'totals_footer': totals_footer,
        'get_string': get_string,
        'tot_sort_col': sort_column,
        'active_pill': active_pill,
        'headers': headers.adv_totals_statistics
        }
    return context

#@register.inclusion_tag('games/recap_totals.html', takes_context=True)
@register.inclusion_tag('games/recap_totals.html', takes_context=True)
def recap_totals(context, games):
    """
    Calculates and displays the totals for the day on recap pages.
    """
    group = context.get('group', None)
    sort_column = context['request'].GET.get('tot_sort')

    date = games[0].date

    player_ids = set(list(games.values_list('team1', flat=True)) + list(games.values_list('team2', flat=True)))
    team_ids = bmodels.Player.objects.filter(first_name__in=["Team1", "Team2"]).values_list('id', flat=True)
    player_ids = filter(lambda id: id not in team_ids, player_ids)
    totals_tables, totals_footer = helpers.recap_totals_dictionaries(headers.totals_statistics, player_ids,
                                                                          date=date, sort_column=sort_column, published=games[0].published)

    # find first active game type for our tab navigation
    active_pill =  context['request'].GET.get('tot_active_pill', None)
    if not active_pill:
        for key, value in totals_tables.items():
            if value:
                active_pill = key
                break

    context = {
        #'tables': statlines_by_type,
        #'totals_footer': totals_by_type,
        'tables': totals_tables,
        'totals_footer': totals_footer,
        'headers': headers.totals_statistics,
        'tot_sort_col': sort_column,
        'active_pill': active_pill
        }
    return context

@register.inclusion_tag('leaderboard/totals.html', takes_context=True)
def lb_totals(context, game_type="5v5", season=None):
        """Returns a dictionary of totals for all players"""

        sort_column = context['request'].GET.get('tot_sort')

        totals_tables, totals_footer = calculate_lb_totals_dictionaries(context,headers.totals_statistics[1:],season_id=getattr(season,'id',None),sort_column=sort_column)

        # we use this variable in our template for template readability sake
        get_string = "&default_tab=totals&possessions_min=" + str(context['possessions_min']) + "&submit=&season="
        if season:
            get_string += str(season.id)

        active_pill = context['request'].GET.get('tot_active_pill') or '5on5'

        context = {
            'tables': totals_tables,
            'totals_footer': totals_footer,
            'get_string': get_string,
            'tot_sort_col': sort_column,
            'active_pill': active_pill,
            'headers': headers.totals_statistics
            }
        return context

@register.inclusion_tag('leaderboard/top_stat_table.html')
def top_players_table(player_list, title, bgcolor='white'):
    """
    Returns the top 5 players for the requested stat category.
    """
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
        tooltip_desc = "True Shooting Percentage. Percentage of Field Goals made with the 3 pointers weighed higher.  Formula is (Points) / (FGA)"
    elif title == "BLKS":
        tooltip_desc = "Blocks"
    elif title == "TP%":
        tooltip_desc = "True Passing Percentage.  Percentage of assists and potential assists that lead to points.  Formula is (Points assisted by you) / (Your passes that lead to shots) "

    return {'player_list': player_list, 'title': title, 'tooltip_desc': tooltip_desc, 'bgcolor': bgcolor}
