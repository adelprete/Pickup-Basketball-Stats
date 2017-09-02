from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    name = models.CharField(max_length=60, blank=False)
    admin = models.ManyToManyField('auth.User', related_name='admin_groups', blank=True, null=True)
    members = models.ManyToManyField('auth.User', related_name='member_groups', blank=True, null=True)

    #leaderboard settings
    possessions_min = models.PositiveIntegerField(default=100)
    fga_min = models.PositiveIntegerField(default=15)

    def __str__(self):
        return "%s" % (self.name)


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
