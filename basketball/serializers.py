from rest_framework import serializers
from basketball.models import PlayByPlay, Game, Player, PRIMARY_PLAY


class ChoicesField(serializers.Field):
    def __init__(self, choices, **kwargs):
        self._choices = choices
        super(ChoicesField, self).__init__(**kwargs)

    def to_representation(self, obj):
        return self._choices[obj]

    def to_internal_value(self, data):
        return getattr(self._choices, data)

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'first_name', 'last_name')


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


class GameSerializer(serializers.ModelSerializer):
    #team1 = PlayerSerializer(many=True, read_only=True)
    #team2 = PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        depth = 1
        fields = '__all__'
