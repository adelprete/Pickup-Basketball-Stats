from collections import OrderedDict
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q
from basketball import models as bmodels
from basketball import forms as bforms
from basketball import headers


def players_home(request, template="players/home.html"):
    """Generates a list of all the players on the site"""

    players = bmodels.Player.player_objs.order_by('first_name')

    context = {
        'players': players,
    }
    return render(request, template, context)

def player_page(request, id, template="players/detail.html"):
    """This generates an individual player's page"""

    player = get_object_or_404(bmodels.Player, id=id)
    all_statistics = [stat[0] for stat in bmodels.ALL_PLAY_TYPES] + ['total_rebounds', 'points', 'def_pos', 'off_pos', 'dreb_opp', 'oreb_opp']
    statlines = player.statline_set.all().order_by('-game__date', 'game__title')

    has_top_plays = False
    if bmodels.PlayByPlay.objects.filter(top_play_players=player):
        has_top_plays = True

    seasons = bmodels.Season.objects.all().order_by('-start_date')

    #Loop over each season a calculate both averages and totals
    #Then store values in a dictionary by game types(5v5,4v4,etc)
    stats_list = [header['stat'] for header in headers.totals_statistics if header['stat'] != 'gp' ]

    game_type_totals = OrderedDict()
    game_type_averages = OrderedDict()
    for season in seasons:

        player_statlines = player.statline_set.filter(game__date__range=(season.start_date, season.end_date))
        
        for game_type in bmodels.GAME_TYPES:
            if player_statlines.filter(game__game_type=game_type[0]):
                player_totals, player_averages = {}, {}
                games_played = player.statline_set.filter(game__game_type=game_type[0], game__date__range=(season.start_date, season.end_date)).count()
                
                player_totals.update(player.get_totals(stats_list, game_type=game_type[0], season=season))
                player_averages.update(player.get_averages(stats_list, game_type=game_type[0], season=season))
                
                player_totals['season'] = season.title
                player_totals['gp'] = games_played

                player_averages['season'] = season.title
                player_averages['gp'] = games_played

                if game_type_totals.get(game_type[1]):
                    game_type_totals[game_type[1]].append(player_totals)
                    game_type_averages[game_type[1]].append(player_averages)
                else:
                    game_type_totals[game_type[1]] = [player_totals]
                    game_type_averages[game_type[1]] = [player_averages]

    #calculate totals and averages for each game_type
    totals = {}
    averages = {}
    for game_type in bmodels.GAME_TYPES:
        if player.get_possessions_count(game_type=game_type[0]):
            
            overall_totals = player.get_totals(stats_list, game_type=game_type[0])
            overall_averages = player.get_averages(stats_list, game_type=game_type[0])
            overall_totals['gp'] = player.statline_set.filter(game__game_type=game_type[0]).count()
            overall_averages['gp'] = player.statline_set.filter(game__game_type=game_type[0]).count()

            totals[game_type[1]] = overall_totals
            averages[game_type[1]] = overall_averages
    
    context = {
        'player': player,
        'has_top_plays': has_top_plays,
        'statlines': statlines,
        'averages': averages,
        'game_type_averages': game_type_averages,
        'totals': totals,
        'game_type_totals': game_type_totals,
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

