from django.contrib import admin
from base.models import *

# Register your models here.
class GroupAdmin(admin.ModelAdmin):
    pass

class MemberPermissionAdmin(admin.ModelAdmin):
    pass

class MemberInviteAdmin(admin.ModelAdmin):
    list_display = ['code', 'email', 'group', 'active', 'permission']

admin.site.register(Group, GroupAdmin)
admin.site.register(MemberPermission, MemberPermissionAdmin)
admin.site.register(MemberInvite, MemberInviteAdmin)
