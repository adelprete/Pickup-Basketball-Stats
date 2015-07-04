from django.shortcuts import render, redirect
from basketball import models as bmodels
from basketball.models import ALL_PLAY_TYPES
from basketball import forms as bforms
from django.http import HttpResponse
import datetime

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
    team1_statlines = bmodels.StatLine.objects.filter(game=game,player__in=game.team1.all()).exclude(player__first_name='Team1').order_by('-points')
    team2_statlines = bmodels.StatLine.objects.filter(game=game,player__in=game.team2.all()).exclude(player__first_name='Team2').order_by('-points')
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
        'team1_totals':team1_totals,
        'team2_totals':team2_totals,
        'form':pbp_form,
        'file_form':bforms.PlayByPlayFileForm(),
        'playbyplays':playbyplays,
    }
    return render(request,"game_box_score.html",context)

def players_home(request):

    players = bmodels.Player.objects.exclude(first_name__in=['Team1','Team2'])
    
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

def create_plays(pk,f):
    game = bmodels.Game.objects.get(pk=pk)
    game.playbyplay_set.all().delete()
    #pbp_file_form = bforms.PlayByPlayFileForm(request.POST,request.FILES)
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
            if play_type[1] == line[1]:
                play_dict['primary_play'] = play_type[0]
                break

        #primary player
        play_dict['primary_player'] = bmodels.Player.objects.get(first_name=line[2])

        #secondary play
        if len(line[3].strip()) > 0:
            for play_type in bmodels.SECONDARY_PLAY:
                if play_type[1] == line[3]:
                    play_dict['secondary_play'] = play_type[0]
                    break

            #seconday player
            play_dict['secondary_player'] = bmodels.Player.objects.get(first_name=line[4])

        #assist play
        if len(line[5].strip()) > 0:
            for play_type in bmodels.ASSIST_PLAY:
                if play_type[1] == line[5]:
                    play_dict['assist'] = play_type[0]
                    break

            #assist player
            play_dict['assist_player'] = bmodels.Player.objects.get(first_name=line[6].strip())
        
        bmodels.PlayByPlay.objects.create(game=game,**play_dict)

def initialize_statlines(pk):
    game = bmodels.Game.objects.get(pk=pk)
    statlines = game.statline_set.all()
    plays = bmodels.PRIMARY_PLAY + bmodels.SECONDARY_PLAY + bmodels.ASSIST_PLAY
    for line in statlines:
        for play in plays:
            setattr(line,play[0],0)
        line.points = 0
        line.total_rebounds = 0
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
            primary_line.fgm += 1
            primary_line.points += 2
        primary_line.save()

        #secondary play
        if play.secondary_play:
            secondary_line = bmodels.StatLine.objects.get(game=game,player=play.secondary_player)
            orig_val = getattr(secondary_line,play.secondary_play)
            setattr(secondary_line,play.secondary_play,orig_val+1)
            
            if play.secondary_play == 'dreb' or play.secondary_play == 'oreb':
                secondary_line.total_rebounds += 1
            
            secondary_line.save()
        
        #assist play
        if play.assist:
            assist_line = bmodels.StatLine.objects.get(game=game,player=play.assist_player)
            orig_val = getattr(assist_line,play.assist)
            setattr(assist_line,play.assist,orig_val+1)
            assist_line.save()

    calculate_game_score(game.pk)

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

"""
def translatePlayCSV(request):
    if request.POST:
        form = bforms.PlayByPlayFileForm(request.POST, request.FILES)
        f = request.FILES['pbpFile']
        import csv
        #Allows for seperation by comma or semicolon, depending on encoding
        dialect = csv.Sniffer().sniff(f.read(1024), delimiters=";,")
        f.seek(0)
        reader = csv.reader(f, dialect)
        i = 0
        for row in reader:
            pass

    else:
        pass
"""
