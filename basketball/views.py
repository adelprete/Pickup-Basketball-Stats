import datetime
import itertools
import operator
from collections import OrderedDict
from datetime import time

from django.shortcuts import render, redirect
from basketball import models as bmodels
from basketball.models import ALL_PLAY_TYPES
from basketball import forms as bforms
from django.http import HttpResponse
from django.db.models import F, Q, Sum, Avg

def root(request):
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
    if id:
        game = bmodels.Game.objects.get(id=id)
    
    pbp_form = bforms.PlayByPlayForm(game)
    team1_statlines = bmodels.StatLine.objects.filter(game=game,player__in=game.team1.all()).order_by('-points')
    team2_statlines = bmodels.StatLine.objects.filter(game=game,player__in=game.team2.all()).order_by('-points')
    if request.POST:
        create_plays(game.pk,request.FILES['pbpFile'])
        initialize_statlines(game.pk)
        calculate_statlines(game.pk)
        calculate_game_score(game.pk)
    
    playbyplays = game.playbyplay_set.all().order_by('time')
    
    context = {
        'game':game,
        'team1_statlines':team1_statlines,
        'team2_statlines':team2_statlines,
        'form':pbp_form,
        'file_form':bforms.PlayByPlayFileForm(),
        'playbyplays':playbyplays,
    }
    return render(request,"game_box_score.html",context)

def players_home(request):

    players = bmodels.Player.objects.exclude(first_name__in=['Team1','Team2']).order_by('first_name')
    
    context = {
        'players':players,
    }
    return render(request,'players_home.html',context)

def player(request,id):

    player = bmodels.Player.objects.get(id=id)

    statlines = player.statline_set.all().order_by('-game__date','game__title')

    pergame_averages = player_pergame_averages(player.id)
    
    context = {
        'player':player,
        'statlines':statlines,
        'averages':pergame_averages,
    }
    return render(request,'player.html',context)

def games_home(request):

    games = bmodels.Game.objects.all().order_by('-date')

    context = {
        'games':games,
    }
    return render(request,'games_home.html',context)

def create_plays(pk,f):
    game = bmodels.Game.objects.get(pk=pk)
    game.playbyplay_set.all().delete()
    for bline in f.readlines():
        play_dict = {}
        line = bline.decode().split(',')

        #parse time
        time_split = line[0].split(':')
        if len(time_split) == 3:
            play_dict['time'] = datetime.time(int(time_split[0]),int(time_split[1]),int(time_split[2]))
        else:
            play_dict['time'] = datetime.time(0,int(time_split[0]),int(time_split[1]))

        #primary play
        for play_type in bmodels.PRIMARY_PLAY:
            if play_type[1].lower() == line[1].lower():
                play_dict['primary_play'] = play_type[0]
                break

        #primary player
        play_dict['primary_player'] = bmodels.Player.objects.get(first_name=line[2])

        #secondary play
        if len(line[3].strip()) > 0:
            for play_type in bmodels.SECONDARY_PLAY:
                if play_type[1].lower() == line[3].lower():
                    play_dict['secondary_play'] = play_type[0]
                    break

            #seconday player
            play_dict['secondary_player'] = bmodels.Player.objects.get(first_name=line[4])

        #assist play
        if len(line[5].strip()) > 0:
            for play_type in bmodels.ASSIST_PLAY:
                if play_type[1].lower() == line[5].lower():
                    play_dict['assist'] = play_type[0]
                    break

            #assist player
            play_dict['assist_player'] = bmodels.Player.objects.get(first_name=line[6].strip())
        
        bmodels.PlayByPlay.objects.create(game=game,**play_dict)

import decimal
def player_pergame_averages(id):

    player = bmodels.Player.objects.get(id=id)

    player_averages = {}
    for play in ALL_PLAY_TYPES:
        if play[0] not in ['sub_out','sub_in']:
            x = player.statline_set.all().aggregate(Avg(play[0]))
            player_averages.update(x)
    player_averages.update(player.statline_set.all().aggregate(Avg('points'),Avg('total_rebounds')))

    return player_averages

def initialize_statlines(pk):
    game = bmodels.Game.objects.get(pk=pk)
    statlines = game.statline_set.all()
    for line in statlines:
        for play in ALL_PLAY_TYPES:
            if play[0] not in ['sub_out','sub_in']:
                setattr(line,play[0],0)
        line.points = 0
        line.total_rebounds = 0
        line.def_pos = 0
        line.off_pos = 0
        line.total_pos = 0
        line.save()

def calculate_game_score(pk):
    game= bmodels.Game.objects.get(pk=pk)
    team1_statlines = bmodels.StatLine.objects.filter(game=game,player__in=game.team1.all())
    team2_statlines = bmodels.StatLine.objects.filter(game=game,player__in=game.team2.all())

    game.team1_score = team1_statlines.aggregate(Sum('points'))['points__sum']
    game.team2_score = team2_statlines.aggregate(Sum('points'))['points__sum']

    game.save()


def calculate_statlines(pk):
    game = bmodels.Game.objects.get(pk=pk)
    initialize_statlines(game.pk)
    playbyplays = game.playbyplay_set.all().order_by('time')
    statlines = game.statline_set.all()
    bench = players_on_bench(game.pk)
    for play in playbyplays:
        
        if play.primary_play not in ['sub_out','sub_in']:
            #import pdb;pdb.set_trace()
            primary_line = bmodels.StatLine.objects.get(game=game,player=play.primary_player)
            orig_val = getattr(primary_line,play.primary_play)
            setattr(primary_line,play.primary_play,orig_val+1)
            if play.primary_play == 'fgm':
                primary_line.fga += 1
                primary_line.points += 1
            if play.primary_play == 'threepa':
                primary_line.fga += 1
            if play.primary_play == 'threepm':
                primary_line.threepa += 1
                primary_line.fga += 1
                primary_line.fgm += 1
                primary_line.points += 2

            primary_line.save()
            if play.primary_play in ['threepm','fgm','to']:
                if primary_line.player in game.team1.all():
                    statlines.filter(player__in=game.team1.all()).exclude(player__pk__in=bench).update(off_pos=F('off_pos')+1)
                    statlines.filter(player__in=game.team2.all()).exclude(player__pk__in=bench).update(def_pos=F('def_pos')+1)
                else:
                    statlines.filter(player__in=game.team1.all()).exclude(player__pk__in=bench).update(def_pos=F('def_pos')+1)
                    statlines.filter(player__in=game.team2.all()).exclude(player__pk__in=bench).update(off_pos=F('off_pos')+1)
                    #import pdb;pdb.set_trace()

            #secondary play
            if play.secondary_play:
                secondary_line = bmodels.StatLine.objects.get(game=game,player=play.secondary_player)
                orig_val = getattr(secondary_line,play.secondary_play)
                setattr(secondary_line,play.secondary_play,orig_val+1)
                
                if play.secondary_play == 'dreb' or play.secondary_play == 'oreb':
                    secondary_line.total_rebounds += 1
                
                secondary_line.save()
                if play.secondary_play == 'dreb':
                    if primary_line.player in game.team1.all():
                        statlines.filter(player__in=game.team1.all()).exclude(player__pk__in=bench).update(off_pos=F('off_pos')+1)
                        statlines.filter(player__in=game.team2.all()).exclude(player__pk__in=bench).update(def_pos=F('def_pos')+1)
                    else:
                        #import pdb;pdb.set_trace()
                        statlines.filter(player__in=game.team1.all()).exclude(player__pk__in=bench).update(def_pos=F('def_pos')+1)
                        statlines.filter(player__in=game.team2.all()).exclude(player__pk__in=bench).update(off_pos=F('off_pos')+1)

            
            #assist play
            if play.assist:
                assist_line = bmodels.StatLine.objects.get(game=game,player=play.assist_player)
                orig_val = getattr(assist_line,play.assist)
                setattr(assist_line,play.assist,orig_val+1)
                assist_line.save()
        else:
            bench.append(play.primary_player.pk)
            bench.remove(play.secondary_player.pk)
    statlines.update(total_pos=F('off_pos')+F('def_pos'))
    calculate_game_score(game.pk)

def players_on_bench(pk):
    game = bmodels.Game.objects.get(pk=pk)
    playbyplays = game.playbyplay_set.filter(primary_play="sub_out").order_by("time")
    playes_out = []
    team1_oncourt = game.team1.all().values_list('pk',flat=True)
    team2_oncourt = game.team2.all().values_list('pk',flat=True)
    
    been_in = []
    bench = []
    for play in playbyplays:
        
        if play.primary_player.pk not in been_in:
            been_in.append(play.primary_player.pk)

        if play.secondary_player.pk not in been_in:
            bench.append(play.secondary_player.pk)
    
    return bench

def ajax_add_play(request,pk):
    game = bmodels.Game.objects.get(pk=pk)
    play_form = bforms.PlayByPlayForm(game,request.POST)
    if play_form.is_valid():
        play_record = play_form.save(commit=False)
        play_record.game = game
        play_record.save()
        calculate_statlines(game.pk)
        return HttpResponse("<br><font style='color:green'>" + play_record.get_primary_play_display() + " Play added.<br>You can add more plays if you'd like.<br>Refresh page to see changes.</font><br><br>")
    return HttpResponse("<br><font style='color:red;'>Failed to Add play</font><br><br>")

def delete_play(request,pk):
    
    play = bmodels.PlayByPlay.objects.get(pk=pk)
    game = play.game
    play.delete()
    calculate_statlines(game.pk)
    
    return redirect(game.get_absolute_url())

def leaderboard_home(request):
    

    context = {

    }
    return render(request,'leaderboard.html',context)
