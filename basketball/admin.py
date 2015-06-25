from django.contrib import admin
from basketball import models as bmodels

class PlayerAdmin(admin.ModelAdmin):
	pass

class GameAdmin(admin.ModelAdmin):
	pass

class StatLineAdmin(admin.ModelAdmin):
	pass

class PlayByPlayAdmin(admin.ModelAdmin):
	pass

admin.site.register(bmodels.Player,PlayerAdmin)
admin.site.register(bmodels.Game,GameAdmin)
admin.site.register(bmodels.StatLine,StatLineAdmin)
admin.site.register(bmodels.PlayByPlay,PlayByPlayAdmin)
