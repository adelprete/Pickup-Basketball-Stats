from django.contrib import admin
from basketball import models as bmodels

class PlayerAdmin(admin.ModelAdmin):
	pass

class GameAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        
        for player in form.cleaned_data['team1']:
            if not bmodels.StatLine.objects.filter(game=obj,player=player):
                bmodels.StatLine.objects.create(game=obj,player=player)

        for player in form.cleaned_data['team2']:
            if not bmodels.StatLine.objects.filter(game=obj,player=player):
                bmodels.StatLine.objects.create(game=obj,player=player)

class StatLineAdmin(admin.ModelAdmin):
	pass

class PlayByPlayAdmin(admin.ModelAdmin):
    pass

admin.site.register(bmodels.Player,PlayerAdmin)
admin.site.register(bmodels.Game,GameAdmin)
admin.site.register(bmodels.StatLine,StatLineAdmin)
admin.site.register(bmodels.PlayByPlay,PlayByPlayAdmin)
