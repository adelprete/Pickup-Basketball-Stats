import itertools
import operator
from collections import OrderedDict
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from django.views.generic.edit import FormView
from django.http import HttpResponse

from basketball import models as bmodels
from basketball import forms as bforms
from basketball import helpers


def games_home(request, template='games/home.html'):
    """Currently only passes a list of all the games to the template"""
    latest_games = bmodels.Game.objects.all()

    keyfunc = operator.attrgetter('date')

    latest_games = sorted(latest_games, key=keyfunc)
    group_list = [{k.strftime('%m-%d-%Y'): list(g)} for k, g in itertools.groupby(latest_games, keyfunc)]

    keys_list = []
    group_dict = {}
    for d in group_list:
        group_dict.update(d)
        keys_list += d.keys()
    keys_list.sort(reverse=True)
    sorted_dict = OrderedDict()
    for key in keys_list:
        sorted_dict[key] = sorted(group_dict[key], key=lambda game: game.title)

    context = {
        'group_list': sorted_dict,
    }
    return render(request, template, context)


def recap(request, game_id, template='games/recap.html'):
    """View for our recap pages for each set of games"""
    game = get_object_or_404(bmodels.Game, id=game_id)

    game_set = bmodels.Game.objects.filter(date=game.date).order_by('title')

    top_plays = bmodels.PlayByPlay.objects.filter(game__in=game_set, top_play_rank__startswith='t').order_by('top_play_rank')
    not_top_plays = bmodels.PlayByPlay.objects.filter(game__in=game_set, top_play_rank__startswith='nt').order_by('top_play_rank')

    context = {
        'games': game_set,
        'top_plays': top_plays,
        'not_top_plays': not_top_plays,
    }

    return render(request, template, context)


def game_basics(request, game_id=None, form_class=bforms.GameForm, template='games/form.html'):
    """Our game form where we can create or edit a games details"""
    model = None
    if game_id:
        model = get_object_or_404(bmodels.Game, id=game_id)

    form = form_class(instance=model)
    if request.POST:
        form = form_class(request.POST, instance=model)
        if "delete" in request.POST:
            model.delete()
            messages.success(request, 'Game Deleted')
            return redirect('/games/')
        if form.is_valid():
            game_record = form.save()

            for player in game_record.team1.iterator():
                if not bmodels.StatLine.objects.filter(game=game_record, player=player):
                    bmodels.StatLine.objects.create(game=game_record, player=player)

            for player in game_record.team2.iterator():
                if not bmodels.StatLine.objects.filter(game=game_record, player=player):
                    bmodels.StatLine.objects.create(game=game_record, player=player)
            if model:
                messages.success(request, "Game Saved")
            else:
                messages.success(request, "Game Created")
            return redirect(game_record.get_absolute_url())

    return render(request, template, {'form': form})


def box_score(request, id, template="games/box_score.html"):
    """Generates the boxscore page of each game
    -A PlayByPlay form is on this page to add individual plays to the game
    -A PlayByPlay upload form is available for uploading a .csv file full of plays
    -With each new play by play sheet uploaded the stats are recalculated.
    """
    if id:
        game = get_object_or_404(bmodels.Game, id=id)

    pbp_form = bforms.PlayByPlayForm(game)
    pbp_filter = bforms.PlayByPlayFilter(request.GET, queryset=bmodels.PlayByPlay.objects.filter(game=game).order_by('time'), game=game)
    
    team1_statlines = bmodels.StatLine.objects.filter(game=game, player__in=game.team1.all()).order_by('-points')
    team2_statlines = bmodels.StatLine.objects.filter(game=game, player__in=game.team2.all()).order_by('-points')
    
    if request.POST:
        helpers.create_plays(game.pk, request.FILES['pbpFile'])
        game.reset_statlines()
        game.calculate_statlines()
        game.calculate_game_score()

    context = {
        'game': game,
        'team1_statlines': team1_statlines,
        'team2_statlines': team2_statlines,
        'form': pbp_form,
        'file_form': bforms.PlayByPlayFileForm(),
        'pbp_filter': pbp_filter,
    }
    return render(request, template, context)


def ajax_add_play(request, pk):
    """
        Called when an individual play is submitted on a game's page.
        Allows for multiple games to be added without having to wait for a page refresh.
    """
    game = get_object_or_404(bmodels.Game, pk=pk)
    play_form = bforms.PlayByPlayForm(game, request.POST)
    if play_form.is_valid():
        play_record = play_form.save(commit=False)
        play_record.game = game
        play_record.save()
        game.calculate_statlines()
        return HttpResponse("<br><font style='color:green'>" + play_record.get_primary_play_display() + " Play added.<br>You can add more plays if you'd like.<br>Refresh page to see changes.</font><br><br>")
    elif play_form.errors:
        html_response = "<br><font style='color:red;'>"

        for field, error in play_form.errors.items():
            html_response += "%s: %s" % (field, error)
        html_response += "</font><br>"
        return HttpResponse(html_response)
    return HttpResponse("<br><font style='color:red;'>Failed to Add play</font><br><br>")


def ajax_filter_plays(request, pk):
    """Called when an some wants to filter the play by plays of a game"""
    game = get_object_or_404(bmodels.Game, pk=pk)
    pbp_filter = bforms.PlayByPlayFilter(request.GET, queryset=bmodels.PlayByPlay.objects.filter(game=game).order_by('time'), game=game)

    return render(request, 'games/playbyplay_list.html', {'pbp_filter': pbp_filter})


def delete_play(request, pk):
    """Called when a play is deleted from a game's page."""

    play = get_object_or_404(bmodels.PlayByPlay, pk=pk)
    play.delete()
    play.game.calculate_statlines()
    messages.success(request, "Play deleted")

    return redirect(play.game.get_absolute_url())


class PlayByPlayFormView(FormView):
    """Our PlaybyPlayform for editing or deleting plays"""

    template_name = "games/playbyplay_form.html"
    model = bmodels.PlayByPlay
    form_class = bforms.PlayByPlayForm

    def post(self, request, *args, **kwargs):
        if 'delete' in request.POST:
            bmodels.PlayByPlay.objects.get(id=self.kwargs['play_id']).delete()
            messages.success(request, 'Play deleted')
            game = self.get_game(self.kwargs['game_id'])
            game.calculate_statlines()
            return redirect(game.get_absolute_url())
        return super(PlayByPlayFormView, self).post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(PlayByPlayFormView, self).get_form_kwargs()
        play = self.get_play(self.kwargs['play_id'])
        game = self.get_game(self.kwargs['game_id'])
        self.success_url = game.get_absolute_url()
        kwargs.update({'game': game, 'instance': play})
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        game = self.get_game(self.kwargs['game_id'])
        game.calculate_statlines()
        messages.success(self.request, "Play saved")
        return super(PlayByPlayFormView, self).form_valid(form)

    def get_game(self, id):
        return bmodels.Game.objects.get(id=id)

    def get_play(self, id):
        return bmodels.PlayByPlay.objects.get(id=id)



