import uuid
from django.db import models
from django.contrib.auth.models import User
from basketball.models import GAME_TYPES, SCORE_TYPES, Season

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

    def checkUserPermission(self, user, permission):
        if user.is_anonymous:
            return False

        for group_permission in user.group_permissions.all():
            if group_permission.group_id == self.id and group_permission.permission == permission:
                return True
        return False

    def getSeasons(self):
        group_season_pks = []
        for season in Season.objects.all():
            if self.game_set.filter(date__range=(season.start_date, season.end_date)):
                group_season_pks.append(season.id)
        seasons = Season.objects.filter(pk__in=group_season_pks).order_by('-start_date')
        return seasons


class MemberPermission(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='group_permissions')
    permission = models.CharField(max_length=30, choices=PERMISSION_TYPES, null=True)
    player = models.ForeignKey('basketball.Player', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return "%s - %s" % (self.group.name, self.user.username)

    class Meta():
        unique_together = ("group", "user")


class MemberProfile(models.Model):
    """Member profile is used to store some more information about the users"""
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, editable=False)
    zip = models.CharField(max_length=5,null=True)

    def __str__(self):
        return "%s - %s" % (self.user.username,self.user.last_name)

    #def get_absolute_url(self):
    #    return reverse("profile_stats",kwargs={'id':self.id})

    #def save(self,*args,**kwargs):
    #    super(MemberProfile,self).save(*args,**kwargs)

class MemberInvite(models.Model):
    group = models.ForeignKey('base.Group', on_delete=models.CASCADE)
    email = models.EmailField()
    permission = models.CharField(max_length=30, choices=PERMISSION_TYPES, null=True)
    player = models.PositiveIntegerField(blank=True, null=True)
    code = models.UUIDField(default=uuid.uuid4, editable=False)
    active = models.BooleanField(default=True)
    creation_date = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return "%s - %s" % (self.group.name, self.email)

class Contact(models.Model):
    creation_date = models.DateField(auto_now_add=True, null=True, blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    subject = models.CharField(max_length=120)
    message = models.TextField()

    def __str__(self):
        return "%s - %s" % (self.creation_date, self.email)
