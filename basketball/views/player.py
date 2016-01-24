import datetime
from collections import OrderedDict
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from basketball import models as bmodels
from basketball import forms as bforms
from basketball import headers


def players_home(request, template="players/home.html"):
	"""Generates a list of all the players on the site"""

	players = bmodels.Player.player_objs.order_by('first_name')

	season=None
	if 'submit' in request.GET:
		form = bforms.PlayerFilterForm(request.GET)
		if form.is_valid():
			season_id = form.data.get('season', None)
			if season_id:
				season = bmodels.Season.objects.get(id=season_id)
	else:
		try:
			#get current season if there is one
			season = bmodels.Season.objects.get(start_date__lt=datetime.datetime.today(), end_date__gt=datetime.datetime.today())
		except:
			#if not in a current season, grab last season.
			season = bmodels.Season.objects.filter(start_date__lt=datetime.datetime.today()).order_by('-start_date')[0]
		
		form = bforms.PlayerFilterForm(initial={'season': season.id})

	if season:
		players = bmodels.Player.player_objs.filter(statline__game__date__range=(season.start_date, season.end_date)).distinct()

	context = {
		'players': players,
		'season': season,
		'form': form,
	}
	
	return render(request, template, context)

def player_page(request, id, template="players/detail.html"):
    """This generates an individual player's page"""

    player = get_object_or_404(bmodels.Player, id=id)

    has_top_plays = False
    if bmodels.PlayByPlay.objects.filter(game__exhibition=False, top_play_players=player):
        has_top_plays = True

    seasons = bmodels.Season.objects.all().order_by('-start_date')
   
    game_log_form = bforms.PlayerGameLogForm()
    context = {
        'player': player,
        'has_top_plays': has_top_plays,
        'game_log_form': game_log_form
    }
    return render(request, template, context)


@login_required
def player_basics(request, id=None, form_class=bforms.PlayerForm, template='players/form.html'):
    """The View handles editing and deleting play profiles"""
    model = None
    if id:
        model = get_object_or_404(bmodels.Player, id=id)

    form = form_class(instance=model)
    if request.POST:
        form = form_class(request.POST, instance=model)
        if "delete" in request.POST:
            model.delete()
            messages.success(request, 'Player Deleted')
            return redirect('/player/')
        if form.is_valid():
            p_record = form.save()

            if model:
                messages.success(request, "Player Saved")
            else:
                messages.success(request, "Player Created")
            return redirect(p_record.get_absolute_url())

    return render(request, template, {'form': form})

def ajax_game_log(request):
	"""Filters a players game log by season"""
	
	season = get_object_or_404(bmodels.Season,id=request.GET['season_id'])

	statlines = bmodels.StatLine.objects.filter(player__id=request.GET['player_id'], game__date__range=(season.start_date,season.end_date)).order_by('-game__date', 'game__title')

	return render_to_response('players/game_log.html', {'statlines': statlines})
