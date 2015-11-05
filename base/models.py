from django.db import models
from django.contrib.auth.models import User

"""
class MemberProfile(models.Model):
    Member profile is used to store some more information about the users
    user = models.OneToOneField('auth.User',editable=False)
    first_name = models.CharField(max_length=30,blank=False)
    last_name = models.CharField(max_length=30,blank=False)
    birth_date = models.DateField(null=True,blank=True)
    creation_date = models.DateField(null=True, blank=True)
    line_1 = models.CharField(max_length=60,blank=True,null=True,verbose_name="Street Address")
    line_2 = models.CharField(max_length=60,blank=True,null=True,verbose_name="APT./Condo/Suite #")
    city = models.CharField(max_length=30,blank=True,null=True)
    state = USStateField(null=True,blank=True)
    zip = models.CharField(max_length=5,null=True)
    phone = PhoneNumberField(blank=True,null=True)

    def __unicode__(self):
        return "%s - %s" % (self.user.username,self.last_name)
    
    def get_absolute_url(self):
        return reverse("profile_stats",kwargs={'id':self.id})
    
    def save(self,*args,**kwargs):
        super(MemberProfile,self).save(*args,**kwargs)
"""
