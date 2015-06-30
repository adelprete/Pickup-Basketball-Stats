from django.shortcuts import render
from basketball import models as bmodels

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
    
    team1_statlines = bmodels.StatLine.objects.filter(game=game,player__in=game.team1.all()).order_by('points')
    team2_statlines = bmodels.StatLine.objects.filter(game=game,player__in=game.team2.all()).order_by('points')
    
    context = {
        'game':game,
        'team1_statlines':team1_statlines,
        'team2_statlines':team2_statlines,
    }
    return render(request,"game_box_score.html",context)
