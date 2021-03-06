import itertools
import json
import operator, datetime
from collections import OrderedDict

from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Q
from django.views.generic.edit import FormView
from django.http import HttpResponse

from base.models import Group
from basketball.serializers import StatlineSerializer
from basketball import models as bmodels
from basketball import forms as bforms
from basketball import helpers


def games_home(request, group_id, template='games/home.html'):
    """Currently only passes a list of all the games to the template"""
    group=Group.objects.get(id=group_id)
    players = bmodels.Player.objects.filter(group=group)
    prefix = ""

    if 'create_game' in request.GET:
        return redirect('create_game', group_id=group_id)
    elif 'unpublished_list' in request.GET:
        games = bmodels.Game.objects.filter(group=group, published=False)
        prefix = 'Unpublished '
    else:
        games = bmodels.Game.objects.filter(group=group, published=True)

    if not games:
        context = {
            'group': group,
            'players': players,
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
        'group': group,
        'players': players,
        'prefix': prefix,
        'games_list': games_tuple_list,
    }
    return render(request, template, context)


def recap(request, group_id, game_id, template='games/recap.html'):
    """View for our recap pages for each set of games"""
    group = Group.objects.get(id=group_id)
    game = get_object_or_404(bmodels.Game, id=game_id)

    game_set = bmodels.Game.objects.filter(group=game.group, date=game.date, published=game.published).order_by('title')
    top_plays = bmodels.PlayByPlay.objects.filter(game__in=game_set, top_play_rank__startswith='t').order_by('top_play_rank')
    not_top_plays = bmodels.PlayByPlay.objects.filter(game__in=game_set, top_play_rank__startswith='nt').order_by('top_play_rank')

	#if we are sorting a table we want to bring the relevant tab up after page reload.
    default_tab = request.GET.get('default_tab')

    if not top_plays and not not_top_plays:
        default_tab = "totals"

    context = {
        'group': group,
        'games': game_set,
        'top_plays': top_plays,
        'not_top_plays': not_top_plays,
	    'default_tab': default_tab
    }

    return render(request, template, context)

@login_required
def game_basics(request, group_id=None, game_id=None, form_class=bforms.GameForm, template='games/form.html'):
    """Our game form where we can create or edit a games details"""
    group = Group.objects.get(id=group_id)
    model = None

    if group.checkUserPermission(request.user, 'edit') == False and \
        group.checkUserPermission(request.user, 'admin') == False:
        return redirect('/group/%s/games/' % (group.id))

    if game_id:
        model = get_object_or_404(bmodels.Game, id=game_id)
        form = form_class(instance=model, group_id=group_id)
    else:
        initial_data={
            'score_type': group.score_type,
            'game_type': group.game_type,
            'points_to_win': group.points_to_win
            }

        form = form_class(initial=initial_data, group_id=group_id)

    if request.POST:
        form = form_class(request.POST, instance=model, group_id=group_id)
        if "delete" in request.POST:
            model.delete()
            return redirect('/group/%s/games/' % (group.id))
        if form.is_valid():

            game_record = form.save(commit=False)
            game_record.group = group
            game_record.save()
            form.save_m2m()
            for player in game_record.team1.iterator():
                if not bmodels.StatLine.objects.filter(game=game_record, player=player):
                    bmodels.StatLine.objects.create(game=game_record, player=player)

            for player in game_record.team2.iterator():
                if not bmodels.StatLine.objects.filter(game=game_record, player=player):
                    bmodels.StatLine.objects.create(game=game_record, player=player)
            game_record.calculate_statlines()
            return redirect(game_record.get_absolute_url())

    return render(request, template, {'group': group, 'form': form})


def box_score(request, group_id, id, template="games/box_score.html"):
    """Generates the boxscore page of each game
    -A Play form is on this page to add individual plays to the game
    -A Play upload form is available for uploading a .csv file full of plays
    -With each new play by play sheet uploaded the stats are recalculated.
    """
    group = Group.objects.get(id=group_id)
    game = get_object_or_404(bmodels.Game, id=id)
    #if game.outdated:
    #    game.calculate_statlines()
    #    game.outdated = False
    #    game.save()

    # finding the previous and next game on the list for navigation purposes
    game_set = bmodels.Game.objects.filter(group=game.group, date=game.date).order_by('title')
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
        'group': group,
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


def ajax_add_play(request, group_id, pk):
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


def ajax_filter_plays(request, group_id, pk):
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

import csv
from rest_framework.decorators import api_view
@api_view()
def export_plays(request, pk):
    """Called when a play is deleted from a game's page."""
    game = get_object_or_404(bmodels.Game, id=pk)
    response = HttpResponse(content_type='text/csv')
    filename = "%s_%s" % (game.date.strftime('%m%d%Y'), game.title)
    response['Content-Disposition'] = 'attachment;filename=%s.csv' % (filename.replace(' ', ''))
    writer = csv.writer(response)
    for play in game.playbyplay_set.all().order_by('time'):
        hours = play.time.seconds // 3600
        minutes = play.time.seconds // 60
        seconds = play.time.seconds % 60

        row = [
            '%02d:%02d:%02d' % (hours, minutes, seconds),
            play.get_primary_play_display(),
            play.primary_player.first_name,
            play.primary_player.last_name,
        ]

        if play.secondary_play:
            secondary = [play.get_secondary_play_display(), play.secondary_player.first_name, play.secondary_player.last_name]
        else:
            secondary = ['','','']
        row += secondary

        if play.assist:
            assist = [play.get_assist_display(), play.assist_player.first_name, play.assist_player.last_name]
        else:
            assist = ['','','']
        row += assist
        writer.writerow(row)
    return response

"""
@login_required
def game_basics(request, group_id, game_id, play_id):
    Our game form where we can create or edit a games details
    group = Group.objects.get(id=group_id)
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
            game_record = form.save(commit=False)
"""
class PlayByPlayFormView(FormView):
    """Our PlaybyPlayform for editing or deleting plays"""

    template_name = "games/playbyplay_form.html"
    model = bmodels.PlayByPlay
    form_class = bforms.PlayByPlayForm

    def get_context_data(self, *args, **kwargs):
        context = super(PlayByPlayFormView, self).get_context_data(**kwargs)
        context['group'] = Group.objects.get(id=self.kwargs['group_id'])
        return context

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

# Angularjs view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from basketball.serializers import (
    PlayCreateUpdateSerializer, PlayRetrieveListSerializer,
    DailyStatlineSerializer, GameSerializer, GameSnippetSerializer, PlayerSerializer,
    SeasonStatlineSerializer, PlayerCreateUpdateSerializer, AwardSerializer
)
from basketball import filters
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, list_route
from django.db.models import Sum
from django_filters import rest_framework as drf_filters
import django_filters

@api_view()
def game_box_score(request, pk):
    game = bmodels.Game.objects.get(id=pk)

    team_statlines = {
        "team1_statlines": bmodels.StatLine.objects.filter(game=game, player__in=game.team1.all()).order_by('-points'),
        "team2_statlines": bmodels.StatLine.objects.filter(game=game, player__in=game.team2.all()).order_by('-points')
    }

    data = {}
    for key, statlines in team_statlines.items():
        team_totals = {}
        for play in bmodels.ALL_PLAY_TYPES:
            if play[0] not in ['sub_out', 'sub_in', 'misc']:
                x = statlines.all().aggregate(Sum(play[0]))
                team_totals.update(x)
        team_totals.update(statlines.aggregate(Sum('points'), Sum('total_rebounds')))
        data[key] = {
            'statlines': StatlineSerializer(statlines.exclude(player__first_name__contains='Team'), many=True).data,
            'team': StatlineSerializer(statlines.get(player__first_name__contains='Team')).data,
            'team_totals': team_totals
        }

    return Response(data)

@api_view()
def game_adv_box_score(request, pk):
    game = bmodels.Game.objects.get(id=pk)

    team_statlines = {
        "team1_statlines": bmodels.StatLine.objects.filter(game=game, player__in=game.team1.all()).order_by('-points'),
        "team2_statlines": bmodels.StatLine.objects.filter(game=game, player__in=game.team2.all()).order_by('-points')
    }

    data = {}
    for key, statlines in team_statlines.items():
        team_totals = {}
        for stat in ['pga','pgm', 'fastbreak_points', 'ast_fgm', 'ast_fga',
            'unast_fgm', 'unast_fga', 'ast_points', 'second_chance_points']:
            x = statlines.all().aggregate(Sum(stat))
            team_totals.update(x)

        data[key] = {
            'statlines': StatlineSerializer(statlines.exclude(player__first_name__contains='Team'), many=True).data,
            'team': StatlineSerializer(statlines.get(player__first_name__contains='Team')).data,
            'team_totals': team_totals,
        }

    return Response(data)

class GameViewSet(viewsets.ModelViewSet):
    queryset = bmodels.Game.objects.all()
    serializer_class = GameSerializer
    filter_backend = (drf_filters.DjangoFilterBackend,)
    filter_fields = ('date', 'group')

    def retrieve(self, request, pk=None):
        game = get_object_or_404(bmodels.Game, pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        if "currentPage" in request.GET:
            if 'true' == request.GET['published']:
                published = True
            else:
                published = False
            games = bmodels.Game.objects.filter(group__id=kwargs['group_id'], published=published).order_by('-date')
            grouped_games = [{k: list(g)} for k, g in itertools.groupby(games, lambda game: game.date)]

            pager = Paginator(grouped_games, request.GET['numPerPage'])
            page_games = pager.page(request.GET['currentPage']).object_list

            # Serialize games for each date
            serialized_page = []
            for dates_games in page_games:
                date = list(dates_games.keys())[0]
                serialized_page.append({
                    "date": date.strftime("%b-%d-%Y"),
                    "games": GameSnippetSerializer(sorted(dates_games[date], key=lambda game: game.title), many=True).data
                })

            results = {
                "items": serialized_page,
                "totalItems": len(grouped_games),
                "currentPage": request.GET['currentPage']
            }
            return Response(results)

        response = super(GameViewSet, self).list(request, *args, **kwargs)
        return response


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = bmodels.Player.objects.all()
    serializer_class = PlayerCreateUpdateSerializer
    filter_backend = (drf_filters.DjangoFilterBackend,)
    filter_fields = ('group', 'first_name')

    action_serializers = {
        'list': PlayerSerializer,
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super(PlayerViewSet, self).get_serializer_class()

    def list(self, request, group_id=None):
        if group_id:
            players = bmodels.Player.objects.filter(group__id=group_id)
            serializer = PlayerSerializer(players, many=True)
            return Response(serializer.data)
        return super().list(request)

class AwardViewSet(viewsets.ModelViewSet):
    queryset = bmodels.Award.objects.all()
    serializer_class = AwardSerializer
    filter_backend = (drf_filters.DjangoFilterBackend,)
    filter_fields = ('category', 'player')


class StatlineViewSet(viewsets.ModelViewSet):
    queryset = bmodels.StatLine.objects.all()
    serializer_class = StatlineSerializer
    filter_backend = (drf_filters.DjangoFilterBackend,)
    filter_class = filters.StatlineFilter

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        queryset = bmodels.StatLine.objects.all()
        player_id = self.request.query_params.get('player_id', None)
        if player_id:
            queryset = queryset.filter(player__id=player_id)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date and end_date:
            queryset = queryset.filter(game__date__gte=start_date, game__date__lte=end_date)
        return queryset


class DailyStatlineViewSet(viewsets.ModelViewSet):
    queryset = bmodels.DailyStatline.objects.all()
    serializer_class = DailyStatlineSerializer
    filter_backend = (drf_filters.DjangoFilterBackend,)
    filter_class = filters.DailyStatlineFilter


class SeasonStatlineViewSet(viewsets.ModelViewSet):
    serializer_class = SeasonStatlineSerializer
    filter_backend = (drf_filters.DjangoFilterBackend,)
    filter_class = filters.SeasonStatlineFilter

    def get_queryset(self):
        query = {
            'player__group__id': self.request.GET['group_id']
        }
        if self.request.GET.get('player_id'):
            query['player__id'] = self.request.GET['player_id']
        return bmodels.SeasonStatline.objects.filter(**query)

@api_view(['GET'])
def calculate_statlines(request, pk):
    game = bmodels.Game.objects.get(pk=pk)
    try:
        game.calculate_statlines()
    except Exception as e:
        Response({'errorMessage': e}, status=400)
    return Response({'message': 'Done'})


class PlaysViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    queryset = bmodels.PlayByPlay.objects.all()
    serializer_class = PlayCreateUpdateSerializer
    filter_fields = ('top_play_players', 'top_play_rank')

    action_serializers = {
        'retrieve': PlayRetrieveListSerializer,
        'list': PlayRetrieveListSerializer,
    }

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            if self.action in self.action_serializers:
                return self.action_serializers[self.action]
        return super(PlaysViewSet, self).get_serializer_class()

    def get_queryset(self, *args, **kwargs):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = super(PlaysViewSet, self).get_queryset(*args, **kwargs)
        #if self.action == 'list':
        #    self.request.get['gameid']
        if 'gameid' in self.request.GET:
            queryset = queryset.filter(game__id=self.request.GET['gameid'])
        if 'top_play_rank__startswith' in self.request.GET:
            queryset = queryset.filter(
                top_play_rank__startswith=self.request.GET['top_play_rank__startswith'],
                game__exhibition=False,
                game__published=True)
        #username = self.request.query_params.get('username', None)
        #if username is not None:
        #    queryset = queryset.filter(purchaser__username=username)
        return queryset

    def create(self, request, *args, **kwargs):
        response = super(PlaysViewSet, self).create(request, *args, **kwargs)
        serializer = PlayRetrieveListSerializer(bmodels.PlayByPlay.objects.get(id=response.data['id']))
        return Response(serializer.data)

    #def destroy(self, request, *args, **kwargs):
    #    super(PlaysViewSet, self).destroy(request, *args, **kwargs)

    #def retrieve(self, request, pk=None):
    #    queryset = User.objects.all()
    #    user = get_object_or_404(queryset, pk=pk)
    #    serializer = UserSerializer(user)
    #    return Response(serializer.data)

#class GetPlaysView(APIView):

#    def get(self, request):
#        return JSONResponse(output)
