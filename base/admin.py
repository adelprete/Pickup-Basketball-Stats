from django.contrib import admin
from base.models import *

class ContactAdmin(admin.ModelAdmin):
    list_display = ['creation_date', 'email', 'subject']

class GroupAdmin(admin.ModelAdmin):
    pass

class MemberPermissionAdmin(admin.ModelAdmin):
    pass

class MemberInviteAdmin(admin.ModelAdmin):
    list_display = ['code', 'email', 'group', 'active', 'permission']

admin.site.register(Contact, ContactAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(MemberPermission, MemberPermissionAdmin)
admin.site.register(MemberInvite, MemberInviteAdmin)
