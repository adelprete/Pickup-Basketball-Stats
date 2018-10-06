import datetime
import itertools
import operator
from collections import OrderedDict
from datetime import time, timedelta

from django.views.decorators.cache import cache_page
from django.views.generic.edit import FormView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response, get_object_or_404
from base.models import Group
from basketball import models as bmodels
from basketball.models import ALL_PLAY_TYPES, TOP_PLAY_RANKS
from basketball.models import NOT_TOP_PLAY_RANKS
from basketball import forms as bforms
from basketball import helpers
from django.http import HttpResponse
from django.db.models import F, Q, Sum, Avg
import datetime


def root(request, group_id, template="base.html"):
    """
    Our Homepage
    Currently prints out a list of games grouped by the dates that they were played on
    """
    group = Group.objects.get(id=group_id)
    # latest_game will help us find the latest set of games.
    try:
        latest_game = bmodels.Game.objects.filter(group=group, published=True).latest('date')
    except:
        context = {
            'group': group,
            'games': []
        }
        return render(request, template, context)
    game_set = bmodels.Game.objects.filter(group=group, date=latest_game.date, published=True).order_by('title')

    # top plays and not top plays
    top_plays = bmodels.PlayByPlay.objects.filter(game__in=game_set, top_play_rank__startswith='t').order_by('top_play_rank')
    not_top_plays = bmodels.PlayByPlay.objects.filter(game__in=game_set, top_play_rank__startswith='nt').order_by('top_play_rank')

    players = bmodels.Player.player_objs.filter(group=group)

    try:
        season = bmodels.Season.objects.get(start_date__lt=datetime.datetime.today(), end_date__gt=datetime.datetime.today())
    except:
        season = bmodels.Season.objects.filter(start_date__lt=datetime.datetime.today()).order_by('-start_date')[0]

    player_tuples = []
    for player in players:
        if player.total_games(season=season):
            player_tuples.append((player.first_name, player.total_wins(season=season), player.total_losses(season=season)))

    player_standings = sorted(player_tuples, key=lambda player: player[1], reverse=True)

    #if we are sorting a table we want to bring the relevant tab up after page reload.
    default_tab = request.GET.get('default_tab')

    if not default_tab and (not top_plays or not top_plays[0].game.youtube_id):
        default_tab = 'totals'

    context = {
        'group': group,
        'games': game_set,
        'top_plays': top_plays,
        'not_top_plays': not_top_plays,
        'standings': player_standings,
        'default_season': season,
        'default_tab': default_tab,
        'seasons': group.getSeasons()
    }
    return render(request, template, context)


def leaderboard_home(request, group_id, template="leaderboard/home.html"):
    """
    Generates the leaderboard page.
    This page uses tabs that load different templatetags that display different information
    """
    group = get_object_or_404(Group,id=group_id)
    season_id = None
    season = None
    possessions_min = group.possessions_min
    if 'submit' in request.GET:
        form = bforms.LeaderboardForm(request.GET)
        if form.is_valid():
            season_id = form.data.get('season', None)
            if season_id:
                season = bmodels.Season.objects.get(id=season_id)
            possessions_min = form.data.get('possessions_min', possessions_min)
    else:
        try:
            season = bmodels.Season.objects.get(start_date__lt=datetime.datetime.today(), end_date__gt=datetime.datetime.today())
        except:
            season = bmodels.Season.objects.filter(start_date__lt=datetime.datetime.today()).order_by('-start_date')[0]

        form = bforms.LeaderboardForm(initial={'possessions_min': possessions_min, 'season': season.id})

    #if we are sorting a table we want to bring the relevant tab up after page reload.
    default_tab = request.GET.get('default_tab')

    context = {
            'group': group,
			'form': form,
			'season_id': season_id,
			'possessions_min': possessions_min,
			'season': season,
			'default_tab': default_tab
		}
    return render(request, template, context)

def records_home(request, group_id, template="records/home.html"):
    """
    Generates the Records page
    This page uses tabs that loads various templatetags that display different record information
    """
    group = Group.objects.get(id=group_id)

    points_to_win = group.points_to_win
    season = None
    if 'submit' in request.GET:
        form = bforms.RecordForm(request.GET, group=group)
        if form.is_valid():
            points_to_win = form.data.get('points_to_win', group.points_to_win)
            try:
                season = bmodels.Season.objects.get(id=form.data.get('season', None))
            except:
                season = None
    else:
        form = bforms.RecordForm(group=group, initial={'points_to_win':group.points_to_win,'season':''})

    context = {
        'group': group,
        'form': form,
        'points_to_win':points_to_win,
        'season':season
    }
    return render(request, template, context)


def login(request, template="login.html"):
    username = None
    password = None
    if request.POST:
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            messages.success("Successfully logged in")
            return redirect("/")
        else:
            messages.error(request, "User account is a disabled")
    else:
        messages.error(request, "Invalid login")

    return render(request, template, {"form": bforms.LoginForm})


def ajax_standings(request):
    """Shows the standings for the chosen season on the home page"""
    season = None
    if request.GET['season_id'] != 'All':
        season = get_object_or_404(bmodels.Season,id=request.GET['season_id'])

    players = bmodels.Player.player_objs.all()

    player_tuples = []
    for player in players:
        if player.total_games(season=season):
            player_tuples.append((player.first_name, player.total_wins(season=season), player.total_losses(season=season)))

    player_standings = sorted(player_tuples, key=lambda player: player[1], reverse=True)

    return render_to_response('players/standings.html', {'standings': player_standings})
