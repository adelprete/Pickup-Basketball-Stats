import datetime
from django import template
from basketball import models as bmodels
from basketball import helpers
from django.db.models import Sum, Q
from collections import OrderedDict
register = template.Library()


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
    return lb_five_on_five_pos(context, game_type=game_type, player_pk=player_pk)


@register.inclusion_tag('lb_5on5_possessions.html', takes_context=True)
def lb_five_on_five_pos(context, game_type="5v5", player_pk=None):
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

		# exclude players that dont meet the minimum 100 possessions
		# requirement
		for player in players:
			if season:
				pos_count = player.statline_set.filter(game__game_type=game_type, game__date__range=(
					season.start_date, season.end_date)).aggregate(Sum('off_pos'))
			else:
				pos_count = player.statline_set.filter(
					game__game_type=game_type).aggregate(Sum('off_pos'))

			if not pos_count['off_pos__sum'] or pos_count['off_pos__sum'] < possessions_min:
				excluded_pks.append(player.pk)

		players = players.exclude(pk__in=excluded_pks)

	dreb = helpers.per100_top_stat_players(
		game_type, 'dreb', player_pk, excluded_pks, season=season)
	oreb = helpers.per100_top_stat_players(
		game_type, 'oreb', player_pk, excluded_pks, season=season)
	total_rebounds = helpers.per100_top_stat_players(
		game_type, 'total_rebounds', player_pk, excluded_pks, season=season)
	asts = helpers.per100_top_stat_players(
		game_type, 'asts', player_pk, excluded_pks, season=season)
	pot_ast = helpers.per100_top_stat_players(
		game_type, 'pot_ast', player_pk, excluded_pks, season=season)
	stls = helpers.per100_top_stat_players(
		game_type, 'stls', player_pk, excluded_pks, season=season)
	to = helpers.per100_top_stat_players(
		game_type, 'to', player_pk, excluded_pks, season=season)
	points = helpers.per100_top_stat_players(
		game_type, 'points', player_pk, excluded_pks, season=season)
	blk = helpers.per100_top_stat_players(
		game_type, 'blk', player_pk, excluded_pks, season=season)

	# these need special attention
	fgm_percent = []
	for player in players:

		statlines = player.statline_set.filter(game__game_type=game_type)
		if season:
			statlines = statlines.filter(game__date__range=(
				season.start_date, season.end_date))

		result = statlines.aggregate(Sum('fgm'), Sum('fga'))

		if result['fga__sum'] and result['fga__sum'] is not 0:
			percentage = result['fgm__sum'] / result['fga__sum'] * 100
		else:
			percentage = 0.0

		fgm_percent.append((player.first_name, percentage))
	fgm_percent = sorted(fgm_percent, key=lambda x: x[1], reverse=True)

	three_percent = []
	for player in players:

		statlines = player.statline_set.filter(game__game_type=game_type)
		if season:
			statlines = statlines.filter(game__date__range=(
				season.start_date, season.end_date))

		result = statlines.aggregate(
			Sum('threepm'), Sum('threepa'), Sum('off_pos'))

		if result['threepa__sum'] and result['threepa__sum'] is not 0:
			percentage = result['threepm__sum'] / result['threepa__sum'] * 100
		else:
			percentage = 0.0
		three_percent.append((player.first_name, percentage))
	three_percent = sorted(three_percent, key=lambda x: x[1], reverse=True)

	dreb_percent = []
	for player in players:

		statlines = player.statline_set.filter(game__game_type=game_type)
		if season:
			statlines = statlines.filter(game__date__range=(
				season.start_date, season.end_date))

		result = statlines.aggregate(Sum('dreb'), Sum('dreb_opp'))

		if result['dreb_opp__sum'] and result['dreb_opp__sum'] is not 0:
			percentage = result['dreb__sum'] / result['dreb_opp__sum'] * 100
		else:
			percentage = 0.0
		dreb_percent.append((player.first_name, percentage))
	dreb_percent = sorted(dreb_percent, key=lambda x: x[1], reverse=True)

	oreb_percent = []
	for player in players:

		statlines = player.statline_set.filter(game__game_type=game_type)
		if season:
			statlines = statlines.filter(game__date__range=(
				season.start_date, season.end_date))

		result = statlines.aggregate(Sum('oreb'), Sum('oreb_opp'))

		if result['oreb_opp__sum'] and result['oreb_opp__sum'] is not 0:
			percentage = result['oreb__sum'] / result['oreb_opp__sum'] * 100
		else:
			percentage = 0.0
		oreb_percent.append((player.first_name, percentage))
	oreb_percent = sorted(oreb_percent, key=lambda x: x[1], reverse=True)

	treb_percent = []
	for player in players:

		statlines = player.statline_set.filter(game__game_type=game_type)
		if season:
			statlines = statlines.filter(game__date__range=(
				season.start_date, season.end_date))

		result = statlines.aggregate(
			Sum('total_rebounds'), Sum('dreb_opp'), Sum('oreb_opp'))

		if result['dreb_opp__sum']:
			percentage = result['total_rebounds__sum'] / \
				(result['oreb_opp__sum'] + result['dreb_opp__sum']) * 100
		else:
			percentage = 0.0
		treb_percent.append((player.first_name, percentage))
	treb_percent = sorted(treb_percent, key=lambda x: x[1], reverse=True)

	ts_percent = []
	for player in players:

		statlines = player.statline_set.filter(game__game_type=game_type)
		if season:
			statlines = statlines.filter(game__date__range=(
				season.start_date, season.end_date))

		result = statlines.aggregate(Sum('points'), Sum('fga'))
		if result['fga__sum']:
			percentage = result['points__sum'] / result['fga__sum'] * 100
		else:
			percentage = 0.0
		ts_percent.append((player.first_name, percentage))
	ts_percent = sorted(ts_percent, key=lambda x: x[1], reverse=True)

	orating_percent = []
	for player in players:

		statlines = player.statline_set.filter(game__game_type=game_type)
		if season:
			statlines = statlines.filter(game__date__range=(
				season.start_date, season.end_date))

		result = statlines.aggregate(Sum('off_pos'))

		team1_games = bmodels.Game.objects.filter(team1=player)
		team2_games = bmodels.Game.objects.filter(team2=player)
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

		if result['off_pos__sum']:
			percentage = (team1_result[
						  'team1_score__sum'] + team2_result['team2_score__sum']) / result['off_pos__sum'] * 100
		else:
			percentage = 0.0
		orating_percent.append((player.first_name, percentage))
	orating_percent = sorted(orating_percent, key=lambda x: x[1], reverse=True)

	drating_percent = []
	for player in players:
		statlines = player.statline_set.filter(game__game_type=game_type)

		if season:
			statlines = statlines.filter(game__date__range=(
				season.start_date, season.end_date))

		result = statlines.aggregate(Sum('def_pos'))

		team1_games = bmodels.Game.objects.filter(team2=player)
		team2_games = bmodels.Game.objects.filter(team1=player)
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

		if result['def_pos__sum']:
			percentage = (team1_result[
						  'team1_score__sum'] + team2_result['team2_score__sum']) / result['def_pos__sum'] * 100
		else:
			percentage = 0.0
		drating_percent.append((player.first_name, percentage))
	drating_percent = sorted(drating_percent, key=lambda x: x[1])

	context = {
		"dreb": dreb[:5],
		"oreb": oreb[:5],
		"total_rebounds": total_rebounds[:5],
		"asts": asts[:5],
		"pot_ast": pot_ast[:5],
		"stls": stls[:5],
		"to": to[:5],
		"points": points[:5],
		"fgm_percent": fgm_percent[:5],
		"three_percent": three_percent[:5],
		"dreb_percent": dreb_percent[:5],
		"oreb_percent": oreb_percent[:5],
		"treb_percent": treb_percent[:5],
		"ts_percent": ts_percent[:5],
		"orating_percent": orating_percent[:5],
		"drating_percent": drating_percent[:5],
		"blk": blk[:5],
		"form": context.get('form', None),
		"possessions_min": possessions_min,
		"season": season,
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
        
        context = {
                'player_totals_list': player_totals_list,
                "season": season,
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
        tooltip_desc = "True Shooting Percentage. Percentage of Field Goals made with the 3pointers weighed higher.  Formula is Points / FGA"
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
