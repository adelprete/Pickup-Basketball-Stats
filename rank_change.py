import sys, os
sys.path.append('/home/live/Pickup-Basketball-Stats')
os.environ['DJANGO_SETTINGS_MODULE'] = 'saturdayball.settings'

from basketball import models as bmodels

for play in bmodels.PlayByPlay.objects.all().exclude(top_play_rank=''):
    if play.top_play_rank == 't1':
        play.top_play_rank = 't01'
    if play.top_play_rank == 't2':
        play.top_play_rank = 't02'
    if play.top_play_rank == 't3':
        play.top_play_rank = 't03'
    if play.top_play_rank == 't4':
        play.top_play_rank = 't04'
    if play.top_play_rank == 't5':
        play.top_play_rank = 't05'
    if play.top_play_rank == 't6':
        play.top_play_rank = 't06'
    elif play.top_play_rank == 't7':
        play.top_play_rank = 't07'
    elif play.top_play_rank == 't8':
        play.top_play_rank = 't08'
    elif play.top_play_rank == 't9':
        play.top_play_rank = 't09'
    elif play.top_play_rank == 't10':
        play.top_play_rank = 't10'
    elif play.top_play_rank == 'nt1':
        play.top_play_rank = 'nt01'
    elif play.top_play_rank == 'nt2':
        play.top_play_rank = 'nt02'
    elif play.top_play_rank == 'nt3':
        play.top_play_rank = 'nt03'
    elif play.top_play_rank == 'nt4':
        play.top_play_rank = 'nt04'
    elif play.top_play_rank == 'nt5':
        play.top_play_rank = 'nt05'
    elif play.top_play_rank == 'nt6':
        play.top_play_rank = 'nt06'
    elif play.top_play_rank == 'nt7':
        play.top_play_rank = 'nt07'
    elif play.top_play_rank == 'nt8':
        play.top_play_rank = 'nt08'
    elif play.top_play_rank == 'nt9':
        play.top_play_rank = 'nt09'
    elif play.top_play_rank == 'nt10':
        play.top_play_rank = 'nt10'
    print(play.top_play_rank)
    play.save()
