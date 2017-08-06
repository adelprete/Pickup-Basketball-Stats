from django.contrib import admin
from base.models import *

# Register your models here.
class GroupAdmin(admin.ModelAdmin):
    pass

class GroupSettingAdmin(admin.ModelAdmin):
    pass

admin.site.register(Group, GroupAdmin)
admin.site.register(GroupSetting, GroupSettingAdmin)
