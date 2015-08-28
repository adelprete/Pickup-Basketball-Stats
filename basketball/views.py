import datetime
import itertools
import operator
from collections import OrderedDict
from datetime import time, timedelta

from django.views.generic.edit import FormView
from django.contrib import messages
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from basketball import models as bmodels
from basketball.models import ALL_PLAY_TYPES, TOP_PLAY_RANKS, NOT_TOP_PLAY_RANKS
from basketball import forms as bforms
from basketball import helpers
from django.http import HttpResponse
from django.db.models import F, Q, Sum, Avg

def root(request):
    """Our Homepage
    -Currently prints out a list of games grouped by the dates that they were played on
    """
    #latest_game will help us find the latest set of games.
    latest_game = bmodels.Game.objects.all().latest('date')
    game_set = bmodels.Game.objects.filter(date=latest_game.date).order_by('title')

    top_plays = bmodels.PlayByPlay.objects.filter(game__in=game_set,top_play_rank__startswith='t').order_by('top_play_rank')
    not_top_plays = bmodels.PlayByPlay.objects.filter(game__in=game_set,top_play_rank__startswith='nt').order_by('top_play_rank')
    
    standings = sorted(bmodels.Player.objects.all().exclude(first_name__contains="Team"),key=lambda player: player.total_wins,reverse=True)

    context ={
        'games':game_set,
        'top_plays':top_plays,
        'not_top_plays':not_top_plays,
        'standings':standings,
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
    return render(request,'player_detail.html',context)

def games_home(request):
    """Currently only passes a list of all the games to the template
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
    season_id = None
    season = None
    possessions_min = 100
    form = bforms.SeasonForm(initial={'possessions_min':100})
    if request.GET != {}:
        form = bforms.SeasonForm(request.GET)
        if form.is_valid():
            season_id = form.data.get('season',None)
            if season_id:
                season = bmodels.Season.objects.get(id=season_id)
            possessions_min = form.data.get('possessions_min',100)

    return render(request,'leaderboard.html',{'form':form,'season_id':season_id,'possessions_min':possessions_min,'season':season})

def player_basics(request,id=None,form_class=bforms.PlayerForm):
    
    model = None
    if id:
        model = get_object_or_404(bmodels.Player,id=id)

    form = form_class(instance=model)
    if request.POST:
        form = form_class(request.POST,instance=model)
        if "delete" in request.POST:
            model.delete()
            messages.success(request,'Player Deleted')
            return redirect('/players-home/')
        if form.is_valid():
            p_record = form.save()
            
            if model:
                messages.success(request,"Player Saved")
            else:
                messages.success(request,"Player Created")
            return redirect(p_record.get_absolute_url())

    return render(request,'player_form.html',{'form':form})

def game_basics(request,game_id=None,form_class=bforms.GameForm):
    
    model = None
    if game_id:
        model = get_object_or_404(bmodels.Game,id=game_id)

    form = form_class(instance=model)
    if request.POST:
        form = form_class(request.POST,instance=model)
        if "delete" in request.POST:
            model.delete()
            messages.success(request,'Game Deleted')
            return redirect('/games-home/')
        if form.is_valid():
            game_record = form.save()
            
            for player in game_record.team1.iterator():
                if not bmodels.StatLine.objects.filter(game=game_record,player=player):
                    bmodels.StatLine.objects.create(game=game_record,player=player)

            for player in game_record.team2.iterator():
                if not bmodels.StatLine.objects.filter(game=game_record,player=player):
                    bmodels.StatLine.objects.create(game=game_record,player=player)
            if model:
                messages.success(request,"Game Saved")
            else:
                messages.success(request,"Game Created")
            return redirect(game_record.get_absolute_url())

    return render(request,'game_form.html',{'form':form})

class PlayByPlayFormView(FormView):
    template_name = "playbyplay_form.html"
    model = bmodels.PlayByPlay
    form_class = bforms.PlayByPlayForm

    def post(self,request,*args,**kwargs):
        if 'delete' in request.POST:
            bmodels.PlayByPlay.objects.get(id=self.kwargs['play_id']).delete()
            messages.success(request,'Play deleted')
            game = self.get_game(self.kwargs['game_id'])
            game.calculate_statlines()
            return redirect(game.get_absolute_url())
        return super(PlayByPlayFormView,self).post(request,*args,**kwargs)
    
    def get_form_kwargs(self):
        kwargs = super(PlayByPlayFormView,self).get_form_kwargs()
        play = self.get_play(self.kwargs['play_id'])
        game=self.get_game(self.kwargs['game_id'])
        self.success_url = game.get_absolute_url()
        kwargs.update({'game': game,'instance':play})
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        game = self.get_game(self.kwargs['game_id'])
        game.calculate_statlines()
        messages.success(self.request,"Play saved")
        return super(PlayByPlayFormView, self).form_valid(form)

    def get_game(self,id):
        return bmodels.Game.objects.get(id=id)
    
    def get_play(self,id):
        return bmodels.PlayByPlay.objects.get(id=id)

def recap(request,game_id): 
    game = bmodels.Game.objects.get(id=game_id)

    game_set = bmodels.Game.objects.filter(date=game.date).order_by('title')

    top_plays = bmodels.PlayByPlay.objects.filter(game__in=game_set,top_play_rank__startswith='t').order_by('top_play_rank')
    not_top_plays = bmodels.PlayByPlay.objects.filter(game__in=game_set,top_play_rank__startswith='nt').order_by('top_play_rank')

    context ={
        'games':game_set,
        'top_plays':top_plays,
        'not_top_plays':not_top_plays,
    }

    return render(request,'recap.html',context)
