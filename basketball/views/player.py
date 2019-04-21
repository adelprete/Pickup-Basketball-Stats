import datetime
from collections import OrderedDict
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from base.models import Group
from basketball import models as bmodels
from basketball import forms as bforms
from basketball import headers


def players_home(request, group_id, template="players/home.html"):
	"""Generates a list of all the players on the site"""

	group = Group.objects.get(id=group_id)

	season=None
	if 'submit' in request.GET:
		form = bforms.PlayerFilterForm(request.GET, group=group)
		if form.is_valid():
			season_id = form.data.get('season', None)
			if season_id:
				season = bmodels.Season.objects.get(id=season_id)
	else:
		form = bforms.PlayerFilterForm(group=group)

	if season:
		players = bmodels.Player.player_objs.filter(group=group, statline__game__date__range=(season.start_date, season.end_date)).distinct()
	elif (not season and 'submit' in request.GET) or not group.getSeasons():
		players = bmodels.Player.player_objs.filter(group=group).order_by('first_name')
	else:
		season = group.getSeasons()[0]
		players = bmodels.Player.player_objs.filter(group=group, statline__game__date__range=(season.start_date, season.end_date)).distinct()
		
	context = {
		'group': group,
		'players': players,
		'season': season,
		'form': form,
		'canEdit': (group.checkUserPermission(request.user, 'edit') or group.checkUserPermission(request.user, 'admin'))
	}

	return render(request, template, context)

def player_page(request, group_id, id, template="players/detail.html"):
	"""This generates an individual player's page"""
	group = Group.objects.get(id=group_id)
	player = get_object_or_404(bmodels.Player, id=id, group=group)

	has_top_plays = False
	if bmodels.PlayByPlay.objects.filter(game__exhibition=False, top_play_players=player):
		has_top_plays = True

	game_log_form = bforms.PlayerGameLogForm(group=group)
	context = {
		'group': group,
		'player': player,
		'has_top_plays': has_top_plays,
		'game_log_form': game_log_form,
		'canEdit': (group.checkUserPermission(request.user, 'edit') or group.checkUserPermission(request.user, 'admin'))
	}
	return render(request, template, context)


@login_required
def player_basics(request, group_id, id=None, form_class=bforms.PlayerForm, template='players/form.html'):
	"""The View handles editing and deleting play profiles"""
	model = None
	group = Group.objects.get(id=group_id)

	if group.checkUserPermission(request.user, 'edit') == False and \
		group.checkUserPermission(request.user, 'admin') == False:
		return redirect('/group/%s/players/' % (group.id))

	if id:
		model = get_object_or_404(bmodels.Player, id=id)

	form = form_class(instance=model)
	if request.POST:
		form = form_class(request.POST, request.FILES, instance=model)
		if "delete" in request.POST:
			model.delete()
			messages.success(request, 'Player Deleted')
			return redirect('/group/%s/players/' % (group.id))
		if form.is_valid():
			p_record = form.save(commit=False)
			p_record.group = group
			p_record.save()

			if model:
				messages.success(request, "Player Saved")
			else:
				messages.success(request, "Player Created")
			return redirect(p_record.get_absolute_url())

	return render(request, template, {'group': group, 'form': form})

def ajax_game_log(request, group_id):
	"""Filters a players game log by season"""
	if request.GET['season_id']:
		season = get_object_or_404(bmodels.Season,id=request.GET['season_id'])
		statlines = bmodels.StatLine.objects.filter(player__id=request.GET['player_id'], game__date__range=(season.start_date,season.end_date)).order_by('-game__date', 'game__title')
	else:
		statlines = []

	return render('players/game_log.html', {'statlines': statlines})

###################
###### API ########
###################

from rest_framework.response import Response
from rest_framework.decorators import api_view
from basketball.templatetags.player_tags import (
	calculate_player_overall_dictionaries,
	calculate_player_possessions_dictionaries
)
from basketball import headers


@api_view(['GET'])
def player_overall_averages(request, player_id):
	averages_tables, overall_footer = calculate_player_overall_dictionaries('','averages',headers.totals_statistics[1:],player_id=player_id)
	data = {
		'averages': averages_tables,
		'overall': overall_footer
	}
	return Response(data)

@api_view(['GET'])
def player_overall_totals(request, player_id):
	totals_tables, overall_footer = calculate_player_overall_dictionaries('','totals',headers.totals_statistics[1:],player_id=player_id)
	data = {
		'totals': totals_tables,
		'overall': overall_footer
	}
	return Response(data)

@api_view(['GET'])
def player_overall_adv_totals(request, player_id):
	totals_tables, overall_footer = calculate_player_overall_dictionaries('','totals',headers.adv_totals_statistics[1:],player_id=player_id)
	data = {
		'totals': totals_tables,
		'overall': overall_footer
	}
	return Response(data)

@api_view(['GET'])
def player_overall_per100(context, player_id):
    """Return a player's per 100 stats for each season"""
    possessions_tables, overall_footer = calculate_player_possessions_dictionaries(context,headers.per_100_statistics, player_id=player_id)
    data = {
        'per100': possessions_tables,
        'overall': overall_footer,
    }
    return Response(data)

@api_view(['GET'])
def player_overall_adv_per100(context, player_id):
    """Return a player's per 100 stats for each season"""
    possessions_tables, overall_footer = calculate_player_possessions_dictionaries(context,headers.adv_per_100_statistics, player_id=player_id)
    data = {
        'per100': possessions_tables,
        'overall': overall_footer,
    }
    return Response(data)
