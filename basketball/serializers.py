from rest_framework import serializers
from django.conf import settings
from drf_extra_fields.fields import Base64ImageField
from basketball.models import (
    PlayByPlay, Game, Player, Season, StatLine, DailyStatline, SeasonStatline,
    PRIMARY_PLAY, Award
)


class ChoicesField(serializers.Field):
    def __init__(self, choices, **kwargs):
        self._choices = choices
        super(ChoicesField, self).__init__(**kwargs)

    def to_representation(self, obj):
        return self._choices[obj]

    def to_internal_value(self, data):
        return getattr(self._choices, data)

class PlayerCreateUpdateSerializer(serializers.ModelSerializer):
    image_src = Base64ImageField(required=False)

    def to_representation(self, instance):
        """Convert image_src to path only when in production."""
        ret = super().to_representation(instance)
        if not settings.DEBUG and ret['image_src']:
            ret['image_src'] = ret['image_src'].split('.com')[1]
        return ret

    class Meta:
        model = Player
        fields = '__all__'

class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Player
        fields = ('id', 'first_name', 'last_name', 'image_src')


class PlayCreateUpdateSerializer(serializers.ModelSerializer):

    primary_play_display = serializers.SerializerMethodField()
    secondary_play_display = serializers.SerializerMethodField()
    assist_display = serializers.SerializerMethodField()

    class Meta:
        model = PlayByPlay
        fields = '__all__'
        """
        fields = [
            'time',
            'primary_play',
            'primary_player',
            'secondary_player',
            'secondary_play',
            'assist',
            'assist_player',
            'game',
            'top_play_rank',
            'top_play_players',
            'description']
        """

    def get_primary_play_display(self,obj):
        return obj.get_primary_play_display()

    def get_secondary_play_display(self,obj):
        return obj.get_secondary_play_display()

    def get_assist_display(self,obj):
        return obj.get_assist_display()


class PlayRetrieveListSerializer(PlayCreateUpdateSerializer):
    primary_player = PlayerSerializer()
    secondary_player = PlayerSerializer()
    assist_player = PlayerSerializer()


class StatlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatLine
        depth = 1
        fields = '__all__'


class GameSerializer(serializers.ModelSerializer):
    #team1 = PlayerSerializer(many=True, read_only=True)
    #team2 = PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        depth = 1
        fields = ['id', 'group', 'date', 'title', 'exhibition', 'points_to_win', 'team1',
        'team2', 'team1_score', 'team2_score', 'winning_players', 'youtube_id',
        'game_type', 'score_type', 'top_player', 'published', 'putback_window',
        'fastbreak_window', 'statline_set']


class TopStatlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatLine
        depth = 1
        fields = ['id', 'points', 'asts', 'total_rebounds', 'player']

class GameSnippetSerializer(serializers.ModelSerializer):
    top_player = PlayerSerializer(read_only=True)
    top_statline = serializers.SerializerMethodField()
    #team2 = PlayerSerializer(many=True, read_only=True)

    def get_top_statline(self, obj):

        if obj.top_player:
            statline = StatLine.objects.get(player__id=obj.top_player.id, game__id=obj.id)
            return TopStatlineSerializer(statline).data
        else:
            return None

    class Meta:
        model = Game
        fields = ['id', 'date', 'title', 'top_player', 'top_statline', 'team1_score',
                    'team2_score', 'exhibition']

class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = '__all__'

class DailyStatlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyStatline
        depth = 1
        fields = '__all__'

class SeasonStatlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeasonStatline
        depth = 1
        fields = '__all__'

class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        depth = 1
        fields = '__all__'
