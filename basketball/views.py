from django.shortcuts import render, redirect
from basketball import models as bmodels
from basketball import forms as bforms
from django.http import HttpResponse

# Create your views here.
def root(request):
    latest_games = bmodels.Game.objects.all()

    context = {
        'latest_games':latest_games,
            }
    return render(request,"base.html",context)

def box_score(request,id):
    if id:
        game = bmodels.Game.objects.get(id=id)
    
    pbp_form = bforms.PlayByPlayForm(game)
    team1_statlines = bmodels.StatLine.objects.filter(game=game,player__in=game.team1.all()).order_by('-points')
    team2_statlines = bmodels.StatLine.objects.filter(game=game,player__in=game.team2.all()).order_by('-points')
  
    playbyplays = game.playbyplay_set.all().order_by('time')
    context = {
        'game':game,
        'team1_statlines':team1_statlines,
        'team2_statlines':team2_statlines,
        'form':pbp_form,
        'playbyplays':playbyplays,
    }
    return render(request,"game_box_score.html",context)

def players_home(request):

    players = bmodels.Player.objects.all()

    context = {
        'players':players,
    }
    return render(request,'players_home.html',context)

def player(request,id):

    player = bmodels.Player.objects.get(id=id)

    statlines = player.statline_set.all().order_by('game__date')

    context = {
        'player':player,
        'statlines':statlines,
    }
    return render(request,'player.html',context)

def games_home(request):

    games = bmodels.Game.objects.all().order_by('-date')

    context = {
        'games':games,
    }
    return render(request,'games_home.html',context)

def initialize_statlines(game):
    statlines = game.statline_set.all()
    plays = bmodels.PRIMARY_PLAY + bmodels.SECONDARY_PLAY + bmodels.ASSIST_PLAY
    for line in statlines:
        for play in plays:
            setattr(line,play[0],0)
        line.points = 0
        line.save()


def calculate_statlines(game):
    initialize_statlines(game)
    playbyplays = game.playbyplay_set.all()
    statlines = game.statline_set.all()
    for play in playbyplays:
        
        #primary play
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
            primary_line.points += 2
        primary_line.save()

        #secondary play
        if play.secondary_play:
            secondary_line = bmodels.StatLine.objects.get(game=game,player=play.secondary_player)
            orig_val = getattr(secondary_line,play.secondary_play)
            setattr(secondary_line,play.secondary_play,orig_val+1)
            secondary_line.total_rebounds += 1
            secondary_line.save()
        
        #assist play
        if play.assist:
            assist_line = bmodels.StatLine.objects.get(game=game,player=play.assist_player)
            orig_val = getattr(assist_line,play.assist)
            setattr(assist_line,play.assist,orig_val+1)
            assist_line.save()

def ajax_add_play(request,pk):
    game = bmodels.Game.objects.get(pk=pk)
    play_form = bforms.PlayByPlayForm(game,request.POST)
    if play_form.is_valid():
        play_record = play_form.save(commit=False)
        play_record.game = game
        play_record.save()
        calculate_statlines(game)
        return HttpResponse("<br><font style='color:green'>" + play_record.get_primary_play_display() + " Play added.<br>You can add more plays if you'd like.<br>Refresh page to see changes.</font><br><br>")
    return HttpResponse("<br><font style='color:red;'>Failed to Add play</font><br><br>")

def delete_play(request,pk):
    
    play = bmodels.PlayByPlay.objects.get(pk=pk)
    game = play.game
    play.delete()
    calculate_statlines(game)
    
    return redirect(game.get_absolute_url())
