import datetime
from collections import OrderedDict
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404
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
	elif group.getSeasons():
		season = group.getSeasons()[0]
		players = bmodels.Player.player_objs.filter(group=group, statline__game__date__range=(season.start_date, season.end_date)).distinct()
	else:
		players = bmodels.Player.player_objs.filter(group=group).order_by('first_name')

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
	player = get_object_or_404(bmodels.Player, id=id)

	has_top_plays = False
	if bmodels.PlayByPlay.objects.filter(game__exhibition=False, top_play_players=player):
		has_top_plays = True

	game_log_form = bforms.PlayerGameLogForm(group=group)
	context = {
		'group': group,
		'player': player,
		'has_top_plays': has_top_plays,
		'game_log_form': game_log_form
	}
	return render(request, template, context)


@login_required
def player_basics(request, group_id, id=None, form_class=bforms.PlayerForm, template='players/form.html'):
	"""The View handles editing and deleting play profiles"""
	model = None
	group = Group.objects.get(id=group_id)

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

	return render_to_response('players/game_log.html', {'statlines': statlines})
