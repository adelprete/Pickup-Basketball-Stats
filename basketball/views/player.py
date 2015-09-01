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
    return render(request, 'players_home.html', context)


def player_page(request, id):
    """This generates an individual player's page
    -A dictionary of the player's averages are passed to the template
    -All statlines for the player are passed to the template
    """
    player = get_object_or_404(bmodels.Player, id=id)

    statlines = player.statline_set.all().order_by('-game__date', 'game__title')

    has_top_plays = False
    if bmodels.PlayByPlay.objects.filter(top_play_players=player):
        has_top_plays = True

    averages_dict = OrderedDict()
    averages_dict["All Time"] = player.get_averages()
    averages_dict["5v5"] = player.get_averages('5v5')

    seasons = bmodels.Season.objects.all()
    for season in seasons:
        for game_type in bmodels.GAME_TYPES:
            if bmodels.StatLine.objects.filter(Q(player=player),
                                               Q(game__date__range=(season.start_date, season.end_date)) & Q(game__game_type=game_type[0])):
                averages_dict[season.title + " - " + game_type[0]
                              ] = player.get_averages(game_type[0], season.id)

    context = {
        'player': player,
        'has_top_plays': has_top_plays,
        'statlines': statlines,
        'averages_dict': averages_dict,
        'seasons': seasons,
    }
    return render(request, 'player_detail.html', context)


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

    return render(request, 'player_form.html', {'form': form})

