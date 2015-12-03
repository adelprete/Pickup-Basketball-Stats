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
    statlines = player.statline_set.all().order_by('-game__date', 'game__title')

    has_top_plays = False
    if bmodels.PlayByPlay.objects.filter(top_play_players=player):
        has_top_plays = True

    seasons = bmodels.Season.objects.all().order_by('-start_date')
    
    context = {
        'player': player,
        'has_top_plays': has_top_plays,
        'statlines': statlines,
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

