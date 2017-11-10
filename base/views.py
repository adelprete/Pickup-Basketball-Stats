from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from django.conf import settings
from django.db.models import Q
from django.contrib.auth import get_user_model # If used custom user model
from .serializers import UserSerializer
from base.models import Group
from base.serializers import GroupSerializer
from basketball.models import Season, Game
from basketball.serializers import SeasonSerializer
import json

class CreateUserView(CreateAPIView):

    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        betacode = request.data.pop('betacode', None)
        if betacode != settings.BETACODE:
            return Response("Invalid Beta Code", 406)
        memberprofile = request.data.pop('memberprofile', None)
        response = super(CreateUserView, self).create(request, *args, **kwargs)
        return Response(response.data)

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def create(self, request):
        request.data['admin'] = [request.user.id]
        return super().create(request)

@api_view(['GET'])
def current_user(request):
    user = request.user
    if not request.user.is_anonymous():
        admin_groups = Group.objects.filter(admin=request.user).values_list('id', 'name')
        member_groups = Group.objects.filter(members=request.user).values_list('id', 'name')
    else:
        admin_groups = []
        member_groups = []

    return Response({
        'username': user.username,
        'admin_groups': admin_groups,
        'member_groups': member_groups
    })

@api_view(['GET'])
def verify_group_admin(request, pk):
    group = Group.objects.get(pk=pk)
    if group in request.user.admin_groups.all():
        return Response({'message': True})
    else:
        return Response({'message': False})

@api_view(['GET'])
def group_seasons(request, pk):
    seasons = Season.objects.all().order_by('start_date');
    group_season_ids = []
    for season in seasons:
        if Game.objects.filter(group__id=pk, date__gte=season.start_date, date__lte=season.end_date).count():
            group_season_ids.append(season.id);

    queryset = Season.objects.filter(id__in=group_season_ids)
    serializer = SeasonSerializer(queryset, many=True)
    return Response({'seasons': serializer.data})
