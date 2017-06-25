import itertools
import operator, datetime
from collections import OrderedDict

from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
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
    prefix = ""

    if 'create_game' in request.GET:
        return redirect('create_game')
    elif 'unpublished_list' in request.GET:
        games = bmodels.Game.objects.filter(published=False)
        prefix = 'Unpublished '
    else:
        games = bmodels.Game.objects.filter(published=True)

    if not games:
        context = {
            'prefix': prefix,
            'games_list': None,
        }
        return render(request, template, context)


    keyfunc = operator.attrgetter('date')

    #group games by date where key is datime obj and value is games list
    group_list = [{k: list(g)} for k, g in itertools.groupby(games, keyfunc)]

    #merge list of dictionaries into one dictionary
    group_dict = { key: value for d in group_list for key, value in d.items() }

    #convert dictionary into list of tuples (key, value)
    games_tuple_list = []
    for key, value in iter(group_dict.items()):
        games_tuple_list.append((key, value))

    games_tuple_list = sorted(games_tuple_list, key=lambda date: date, reverse=True)

    #use Django paginator to paginate
    paginator = Paginator(games_tuple_list, 25)

    page = request.GET.get('page')
    try:
        games_tuple_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        games_tuple_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        games_tuple_list = paginator.page(paginator.num_pages)

    context = {
        'prefix': prefix,
        'games_list': games_tuple_list,
    }
    return render(request, template, context)


def recap(request, game_id, template='games/recap.html'):
    """View for our recap pages for each set of games"""
    game = get_object_or_404(bmodels.Game, id=game_id)

    game_set = bmodels.Game.objects.filter(date=game.date, published=game.published).order_by('title')
    top_plays = bmodels.PlayByPlay.objects.filter(game__in=game_set, top_play_rank__startswith='t').order_by('top_play_rank')
    not_top_plays = bmodels.PlayByPlay.objects.filter(game__in=game_set, top_play_rank__startswith='nt').order_by('top_play_rank')

	#if we are sorting a table we want to bring the relevant tab up after page reload.
    default_tab = request.GET.get('default_tab')

    if not top_plays and not not_top_plays:
        default_tab = "totals"

    context = {
        'games': game_set,
        'top_plays': top_plays,
        'not_top_plays': not_top_plays,
	    'default_tab': default_tab
    }

    return render(request, template, context)

@login_required
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
    game = get_object_or_404(bmodels.Game, id=id)

    # finding the previous and next game on the list for navigation purposes
    game_set = bmodels.Game.objects.filter(date=game.date).order_by('title')
    prev_game, next_game = None, None
    for i, g in enumerate(game_set):
        if g.id == game.id:
            if i+1 != game_set.count():
                next_game = game_set[i+1]
            if i != 0:
                prev_game = game_set[i-1]

    # forms and filters
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
        'prev_game': prev_game,
        'next_game': next_game,
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
        game.calculate_meta_statlines()
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
            game = bmodels.Game.objects.get(id=self.kwargs['game_id'])
            game.calculate_statlines()
            return redirect(game.get_absolute_url())
        return super(PlayByPlayFormView, self).post(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(PlayByPlayFormView, self).get_form_kwargs()
        game = bmodels.Game.objects.get(id=self.kwargs['game_id'])
        play = bmodels.PlayByPlay.objects.get(id=self.kwargs['play_id'])
        self.success_url = game.get_absolute_url()
        kwargs.update({'game': game, 'instance': play})
        return kwargs

    def form_valid(self, form):
        self.object = form.save()
        game = bmodels.Game.objects.get(id=self.kwargs['game_id'])
        game.calculate_statlines()
        messages.success(self.request, "Play saved")
        return super(PlayByPlayFormView, self).form_valid(form)
