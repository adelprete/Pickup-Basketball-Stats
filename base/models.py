import uuid
from django.db import models
from django.contrib.auth.models import User
from basketball.models import GAME_TYPES, SCORE_TYPES

PERMISSION_TYPES = [
    ('read', 'Read'),
    ('edit', 'Edit'),
    ('admin', 'Admin')
]

class Group(models.Model):
    name = models.CharField(max_length=60, blank=False)
    admin = models.ManyToManyField('auth.User', related_name='admin_groups', blank=True, null=True)
    members = models.ManyToManyField('auth.User', related_name='member_groups', blank=True, null=True)

    # default game settings
    game_type = models.CharField(max_length=30, choices=GAME_TYPES, null=True)
    score_type = models.CharField(max_length=30, choices=SCORE_TYPES, null=True)
    points_to_win = models.CharField(max_length=30, choices=(('11','11'), ('30','30'), ('other','Other')) ,null=True)

    #leaderboard settings
    possessions_min = models.PositiveIntegerField(default=100)
    fga_min = models.PositiveIntegerField(default=15)

    def __str__(self):
        return "%s" % (self.name)


class MemberPermission(models.Model):
    group = models.ForeignKey(Group, blank=True, null=True)
    user = models.ForeignKey('auth.User', related_name='group_permissions')
    permission = models.CharField(max_length=30, choices=PERMISSION_TYPES, null=True)

    def __str__(self):
        return "%s - %s" % (self.group.name, self.user.username)

    class Meta():
        unique_together = ("group", "user")


class MemberProfile(models.Model):
    """Member profile is used to store some more information about the users"""
    user = models.OneToOneField('auth.User',editable=False)
    zip = models.CharField(max_length=5,null=True)

    def __str__(self):
        return "%s - %s" % (self.user.username,self.user.last_name)

    #def get_absolute_url(self):
    #    return reverse("profile_stats",kwargs={'id':self.id})

    #def save(self,*args,**kwargs):
    #    super(MemberProfile,self).save(*args,**kwargs)

class MemberInvite(models.Model):
    group = models.ForeignKey('base.Group')
    email = models.EmailField()
    permission = models.CharField(max_length=30, choices=PERMISSION_TYPES, null=True)
    code = models.UUIDField(default=uuid.uuid4, editable=False)
    active = models.BooleanField(default=True)
    creation_date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return "%s - %s" % (self.group.name, self.email)
