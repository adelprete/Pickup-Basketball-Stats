from django.contrib import admin
from basketball import models as bmodels
from basketball import forms as bforms
from django.forms import SelectMultiple
from django.db import models


class PlayerAdmin(admin.ModelAdmin):
    pass


class GameAdmin(admin.ModelAdmin):
    exclude = ("winning_players",)

    def save_model(self, request, obj, form, change):
        obj.save()

        for player in form.cleaned_data['team1']:
            if not bmodels.StatLine.objects.filter(game=obj, player=player):
                bmodels.StatLine.objects.create(game=obj, player=player)

        for player in form.cleaned_data['team2']:
            if not bmodels.StatLine.objects.filter(game=obj, player=player):
                bmodels.StatLine.objects.create(game=obj, player=player)


class StatLineAdmin(admin.ModelAdmin):
    pass


class PlayByPlayAdmin(admin.ModelAdmin):
    pass


class SeasonAdmin(admin.ModelAdmin):
	form = bforms.SeasonForm

admin.site.register(bmodels.Player, PlayerAdmin)
admin.site.register(bmodels.Game, GameAdmin)
admin.site.register(bmodels.StatLine, StatLineAdmin)
admin.site.register(bmodels.PlayByPlay, PlayByPlayAdmin)
admin.site.register(bmodels.Season, SeasonAdmin)
