from django.contrib import admin
from base.models import *

# Register your models here.
class GroupAdmin(admin.ModelAdmin):
    pass

admin.site.register(Group, GroupAdmin)
