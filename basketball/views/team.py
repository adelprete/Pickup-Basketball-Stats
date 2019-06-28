import itertools
import json
from basketball import models as bmodels

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from basketball.serializers import (
    PlayCreateUpdateSerializer, PlayRetrieveListSerializer,
    DailyStatlineSerializer, GameSerializer, GameSnippetSerializer, PlayerSerializer,
    SeasonStatlineSerializer, PlayerCreateUpdateSerializer, AwardSerializer, StatlineSerializer,
    TeamSerializer
)
from basketball import filters
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, list_route
from django.db.models import Sum
from django_filters import rest_framework as drf_filters
import django_filters

class TeamViewSet(viewsets.ModelViewSet):
    queryset = bmodels.Team.objects.all()
    serializer_class = TeamSerializer
    filter_backend = (drf_filters.DjangoFilterBackend,)
    filter_fields = ['id', 'group__id']

    #def retrieve(self, request, pk=None):
    #    team = get_object_or_404(bmodels.Team, pk=pk)
    #    serializer = TeamSerializer(team)
    #    return Response(serializer.data)

    #def list(self, request, *args, **kwargs):
    #    teams = bmodels.Team.objects.filter(group__id=kwargs['group_id'])
    #
    #    results = {
    #        "teams": TeamSerializer(teams, many=True).data,
    #    }
    #    return Response(results)
