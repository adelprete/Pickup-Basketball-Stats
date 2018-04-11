from rest_framework import permissions, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets
from registration.backends.simple.views import RegistrationView
from django.core.mail import send_mail
from django_filters import rest_framework as drf_filters
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model # If used custom user model
from .serializers import UserSerializer
from base.models import Group, MemberPermission, MemberInvite, MemberProfile, Contact
from base.filters import MemberPermissionFilter
from base.serializers import (
    GroupSerializer,
    MemberPermissionSerializer,
    MemberInviteSerializer,
    ContactSerializer
)
from basketball.models import Season, Game
from basketball.serializers import SeasonSerializer
import json

class CreateUserView(CreateAPIView):

    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        member_profile_data = request.data.pop('memberprofile', None)
        if User.objects.filter(email=request.data['email']):
            return Response({'email': 'Email is already in use'}, status=status.HTTP_400_BAD_REQUEST)
        response = super(CreateUserView, self).post(request, *args, **kwargs)
        member_profile_data['user'] = User.objects.get(id=response.data['id'])
        member_profie = MemberProfile.objects.create(**member_profile_data)

        send_mail(
            "New user",
            "New user created %s." % (User.objects.get(id=response.data['id']).username),
            "no-reply@saturdayball.com",
            ["adelprete87@gmail.com"])

        return Response(response.data)

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def create(self, request):
        betacode = request.data.pop('betacode', None)
        if betacode != settings.BETACODE:
            return Response("Invalid Beta Code", 406)
        request.data['admin'] = [request.user.id]
        response = super().create(request)
        group = Group.objects.get(id=response.data['id'])
        MemberPermission.objects.create(group=group, user=request.user, permission='admin')
        return response

class MemberPermissionViewSet(viewsets.ModelViewSet):
    queryset = MemberPermission.objects.all()
    serializer_class = MemberPermissionSerializer
    filter_backend = (drf_filters.DjangoFilterBackend,)
    filter_fields = ['group', 'permission', 'user']

class MemberInviteViewSet(viewsets.ModelViewSet):
    queryset = MemberInvite.objects.all()
    serializer_class = MemberInviteSerializer
    lookup_field = 'code'

    def create(self, request, *args, **kwargs):
        if MemberPermission.objects.filter(group__id=request.data['group'], user__email=request.data['email']):
            response = {
                'message': 'Member is already a part of this group.'
            }
            return Response(response, status=403)
        response = super(MemberInviteViewSet, self).create(request, *args, **kwargs)
        url = settings.APP_URL + "accept-invite/" + response.data['code']
        text_content = "You've been invited to a group on SaturdayBall.com:\n\n%s" % (url)
        html_content = "You've been invited to a group on SaturdayBall.com:<br><br><a href={0}>{0}</a>".format(url)
        send_mail(
            'SaturdayBall.com Invitation',
            text_content,
            'no-reply@saturdayball.com',
            [request.data['email']],
            fail_silently=False,
            html_message=html_content
        )
        return Response(response.data)

    def update(self, request, *args, **kwargs):
        member_invite = MemberInvite.objects.get(code=request.data['code'])
        if member_invite.active:
            user = User.objects.get(email=member_invite.email)
            MemberPermission.objects.create(group=member_invite.group, user=user, permission=member_invite.permission)
            serializer = MemberInviteSerializer(member_invite, data={'active': False}, partial=True)
            serializer.is_valid()
            member_invite = serializer.save()
            return Response(serializer.data)
            #response = super(MemberInviteViewSet, self).update(request, *args, **kwargs)
        return Response(member_invite)


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        if not request.user.is_anonymous():
            request.data['user'] = request.user.id
        response = super().create(request)
        send_mail(
            "New Contact",
            "Someone left a new contact message on saturdayball.",
            "no-reply@saturdayball.com",
            ["adelprete87@gmail.com"])
        return response


@api_view(['GET'])
def current_user(request):
    user = request.user
    if not request.user.is_anonymous():
        group_permissions = request.user.group_permissions.all().values_list('group__id', 'group__name', 'permission')
    else:
        group_permissions = []

    return Response({
        'username': user.username,
        'group_permissions': group_permissions
    })

@api_view(['POST'])
def send_member_invite(request, pk):
    return Response({'message': 'it worked'})

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
