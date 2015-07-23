import datetime
import itertools
import operator
from collections import OrderedDict
from datetime import time

from django.contrib import messages
from django.shortcuts import render, redirect, render_to_response
from basketball import models as bmodels
from basketball.models import ALL_PLAY_TYPES
from basketball import forms as bforms
from basketball import helpers
from django.http import HttpResponse
from django.db.models import F, Q, Sum, Avg

def root(request):
    """Our Homepage
    -Currently prints out a list of games grouped by the dates that they were played on
    """
    latest_games = bmodels.Game.objects.all()
    
    keyfunc = operator.attrgetter('date')

    latest_games = sorted(latest_games, key = keyfunc)
    group_list = [{ k.strftime('%m-%d-%Y') : list(g)} for k, g in itertools.groupby(latest_games, keyfunc)]

    keys_list = []
    group_dict = {}
    for d in group_list:
        group_dict.update(d)
        keys_list += d.keys()
    keys_list.sort(reverse=True)
    sorted_dict = OrderedDict()
    for key in keys_list:
        sorted_dict[key] = sorted(group_dict[key],key=lambda game: game.title)
    context = {
        'group_list':sorted_dict,
            }
    return render(request,"base.html",context)

def box_score(request,id):
    """Generates the boxscore page of each game
    -A PlayByPlay form is on this page to add individual plays to the game
    -A PlayByPlay upload form is available for uploading a .csv file full of plays
    -With each new play by play sheet uploaded the stats are recalculated.
    """
    if id:
        game = bmodels.Game.objects.get(id=id)
    
    pbp_form = bforms.PlayByPlayForm(game)
    pbp_filter = bforms.PlayByPlayFilter(request.GET,queryset=bmodels.PlayByPlay.objects.filter(game=game).order_by('time'),game=game)
    team1_statlines = bmodels.StatLine.objects.filter(game=game,player__in=game.team1.all()).order_by('-points')
    team2_statlines = bmodels.StatLine.objects.filter(game=game,player__in=game.team2.all()).order_by('-points')
    if request.POST:
        helpers.create_plays(game.pk,request.FILES['pbpFile'])
        game.reset_statlines()
        game.calculate_statlines()
        game.calculate_game_score()
    
    context = {
        'game':game,
        'team1_statlines':team1_statlines,
        'team2_statlines':team2_statlines,
        'form':pbp_form,
        'file_form':bforms.PlayByPlayFileForm(),
        'pbp_filter':pbp_filter,
    }
    return render(request,"game_box_score.html",context)

def players_home(request):
    """Generates a list of all the players on the site
    """
    players = bmodels.Player.objects.exclude(first_name__in=['Team1','Team2']).order_by('first_name')
    
    context = {
        'players':players,
    }
    return render(request,'players_home.html',context)

def player(request,id):
    """This generates an individual player's page
    -A dictionary of the player's averages are passed to the template
    -All statlines for the player are passed to the template
    """
    player = bmodels.Player.objects.get(id=id)

    statlines = player.statline_set.all().order_by('-game__date','game__title')

    context = {
        'player':player,
        'statlines':statlines,
        'averages':player.get_averages(),
        'averages_5v5':player.get_averages('5v5'),
        'averages_4v4':player.get_averages('4v4')
    }
    return render(request,'player.html',context)

def games_home(request):
    """Currently only passes a list of all the games to the template
    """
    games = bmodels.Game.objects.all().order_by('-date')

    context = {
        'games':games,
    }
    return render(request,'games_home.html',context)

def ajax_add_play(request,pk):
    """Called when an individual play is submitted on a game's page.
    Allows for multiple games to be added without having to wait for a page refresh.
    """
    game = bmodels.Game.objects.get(pk=pk)
    play_form = bforms.PlayByPlayForm(game,request.POST)
    if play_form.is_valid():
        play_record = play_form.save(commit=False)
        play_record.game = game
        play_record.save()
        game.calculate_statlines()
        return HttpResponse("<br><font style='color:green'>" + play_record.get_primary_play_display() + " Play added.<br>You can add more plays if you'd like.<br>Refresh page to see changes.</font><br><br>")
    elif play_form.errors:
        html_response = "<br><font style='color:red;'>"

        for field,error in play_form.errors.items():
            html_response += "%s: %s" % (field,error)
        html_response += "</font><br>"
        return HttpResponse(html_response)
    return HttpResponse("<br><font style='color:red;'>Failed to Add play</font><br><br>")

def ajax_filter_plays(request,pk):
    """Called when an some wants to filter the play by plays of a game
    """
    game = bmodels.Game.objects.get(pk=pk)
    pbp_filter = bforms.PlayByPlayFilter(request.GET,queryset=bmodels.PlayByPlay.objects.filter(game=game).order_by('time'),game=game)
    
    return render_to_response('playbyplay_list.html',{'pbp_filter':pbp_filter})

def delete_play(request,pk):
    """
    Called when a play is deleted from a game's page.
    """
    
    play = bmodels.PlayByPlay.objects.get(pk=pk)
    play.delete()
    play.game.calculate_statlines()
    messages.success(request,"Play deleted")

    return redirect(play.game.get_absolute_url())

def leaderboard_home(request):
    """
    Generates the leaderboard page.
    This page uses tabs that load different templatetags that display different information
    """
    return render(request,'leaderboard.html',{})
