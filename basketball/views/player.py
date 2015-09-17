from collections import OrderedDict
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q
from basketball import models as bmodels
from basketball import forms as bforms


def players_home(request):
    """Generates a list of all the players on the site
    """
    players = bmodels.Player.objects.exclude(
        first_name__in=['Team1', 'Team2']).order_by('first_name')

    context = {
        'players': players,
    }
    return render(request, 'players/home.html', context)


def player_page(request, id):
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
    game_type_totals = OrderedDict()
    game_type_averages = OrderedDict()
    for season in seasons:

        player_statlines = player.statline_set.filter(game__date__range=(season.start_date, season.end_date))
        
        for game_type in bmodels.GAME_TYPES:
            if player_statlines.filter(game__game_type=game_type[0]):
                player_totals, player_averages = {}, {}
                games_played = player.statline_set.filter(game__game_type=game_type[0], game__date__range=(season.start_date, season.end_date)).count()

                for stat in all_statistics:
                    if stat not in ['misc', 'sub_out', 'sub_in']:
                        player_totals[stat] = player.get_totals(stat, game_type=game_type[0], season=season)
                        player_averages[stat] = player.get_averages(stat, game_type=game_type[0], season=season)
                
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
        overall_totals, overall_averages = {}, {}
        if player.get_possessions_count(game_type=game_type[0]):
            for stat in all_statistics:
                if stat not in ['misc', 'sub_in', 'sub_out']:
                    overall_totals[stat] = player.get_totals(stat, game_type=game_type[0])
                    overall_averages[stat] = player.get_averages(stat, game_type=game_type[0])
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
    return render(request, 'players/detail.html', context)


def player_basics(request, id=None, form_class=bforms.PlayerForm):

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

    return render(request, 'players/form.html', {'form': form})

