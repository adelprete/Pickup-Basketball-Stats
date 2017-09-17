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

@api_view(['GET'])
def current_user(request):
    user = request.user
    admin_groups = Group.objects.filter(admin=request.user).values_list('id', 'name')
    member_groups = Group.objects.filter(members=request.user).values_list('id', 'name')
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
