from django import forms
from base import fields
from basketball import models as bmodels
from django.db.models import Q
import django_filters
from django.db import models


class DateMaskWidget(forms.TextInput):
    def __init__(self,*args,**kwargs):
        super(DateMaskWidget,self).__init__(*args,**kwargs)
        cls = ' '.join(['datepicker'])
        self.attrs.update({'class': cls})


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(max_length=30, widget=forms.PasswordInput)


class PlayerForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = bmodels.Player
        exclude = [""]


class PlayerGameLogForm(forms.Form):
    season = forms.ModelChoiceField(queryset=bmodels.Season.objects.all(), initial=bmodels.Season.objects.all()[0])


class PlayerFilterForm(forms.Form):
    season = forms.ModelChoiceField(queryset=bmodels.Season.objects.all(), empty_label="All", required=False)


class GameForm(forms.ModelForm):
    required_css_class = 'required'
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker'}))
    exhibition = fields.BooleanChoiceField(label="Exhibition Game?", required=True, initial=False, help_text="Stats for Exhibition games are NOT counted.")
    published = fields.BooleanChoiceField(label="Publish Game?", required=True, initial=False, help_text="Publish games when they are ready to be view by others.")

    def __init__(self, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        self.fields['team1'].widget.attrs = {"size": 15}
        self.fields['team1'].queryset = bmodels.Player.player_objs.all()
        self.fields['team2'].widget.attrs = {"size": 15}
        self.fields['team2'].queryset = bmodels.Player.player_objs.all()

    def clean_team1(self):
        team1_qs = self.cleaned_data.get('team1', None)
        if team1_qs:
            team1_qs = team1_qs | bmodels.Player.objects.filter(first_name='Team1')
        return team1_qs

    def clean_team2(self):
        team2_qs = self.cleaned_data.get('team2', None)
        if team2_qs:
            team2_qs = team2_qs | bmodels.Player.objects.filter(first_name='Team2')
        return team2_qs

    class Meta:
        model = bmodels.Game
        exclude = ['winning_players','top_player', 'team1_score', 'team2_score']


class PlayByPlayForm(forms.ModelForm):
    required_css_class = 'required'

    def __init__(self, game, *args, **kwargs):
        super(PlayByPlayForm, self).__init__(*args, **kwargs)
        self.fields['primary_player'].queryset = bmodels.Player.objects.filter(Q(team1_set=game) | Q(team2_set=game)).distinct()
        self.fields['secondary_player'].queryset = bmodels.Player.objects.filter(Q(team1_set=game) | Q(team2_set=game)).distinct()
        self.fields['assist_player'].queryset = bmodels.Player.objects.filter(Q(team1_set=game) | Q(team2_set=game)).distinct()
        self.fields['top_play_players'].queryset = bmodels.Player.objects.filter(Q(team1_set=game) | Q(team2_set=game)).distinct()

    class Meta:
        model = bmodels.PlayByPlay
        exclude = ['game']


class PlayByPlayFileForm(forms.Form):
    pbpFile = forms.FileField(
        label="Play By Play File", help_text="Only upload .csv files")


class NicerFilterSet(django_filters.FilterSet):

    def __init__(self, *args, **kwargs):
        super(NicerFilterSet, self).__init__(*args, **kwargs)
        for name, field in self.filters.items():
            if isinstance(field, django_filters.ChoiceFilter):
                # Add "Any" entry to choice fields.
                field.extra['choices'] = tuple([("", "Any"), ] + list(field.extra['choices']))


class PlayByPlayFilter(NicerFilterSet):
    primary_player = django_filters.ModelMultipleChoiceFilter()
    secondary_player = django_filters.ModelMultipleChoiceFilter()
    assist_player = django_filters.ModelMultipleChoiceFilter()

    def __init__(self, *args, **kwargs):
        game = kwargs.pop('game', None)
        super(PlayByPlayFilter, self).__init__(*args, **kwargs)
        self.filters['primary_play'].field.widget.attrs = {'class': 'form-control'}
        self.filters['primary_player'].extra['queryset'] = bmodels.Player.objects.filter(Q(team1_set=game) | Q(team2_set=game)).distinct()
        self.filters['primary_player'].field.widget.attrs = {'class': 'form-control'}
        self.filters['secondary_play'].field.widget.attrs = {'class': 'form-control'}
        self.filters['secondary_player'].extra['queryset'] = bmodels.Player.objects.filter(Q(team1_set=game) | Q(team2_set=game)).distinct()
        self.filters['secondary_player'].field.widget.attrs = {'class': 'form-control'}
        self.filters['assist'].field.widget.attrs = {'class': 'form-control'}
        self.filters['assist_player'].extra['queryset'] = bmodels.Player.objects.filter(Q(team1_set=game) | Q(team2_set=game)).distinct()
        self.filters['assist_player'].field.widget.attrs = {'class': 'form-control'}

    class Meta:
        model = bmodels.PlayByPlay
        fields = ['primary_play', 'primary_player', 'secondary_play', 'secondary_player', 'assist', 'assist_player']


class LeaderboardForm(forms.Form):
    season = forms.ModelChoiceField(queryset=bmodels.Season.objects.all(), empty_label="All", required=False)
    possessions_min = forms.IntegerField(label="Minimum Possessions", min_value=1)

class RecordForm(forms.Form):
    season = forms.ModelChoiceField(queryset=bmodels.Season.objects.all(), empty_label="All", required=False)
    points_to_win = forms.ChoiceField(label="Games played to",choices=(('11','11'), ('30','30'), ('other','Other')))


class SeasonForm(forms.ModelForm):

    def clean(self):
        data = self.cleaned_data
        start_date = data['start_date']
        end_date = data['end_date']

        if start_date > end_date:
                raise forms.ValidationError("Start Date can't be before end date")

        season = bmodels.Season.objects.filter(
                        Q(Q(start_date__lt=start_date)&Q(end_date__gt=start_date))
                        |Q(Q(start_date__lt=end_date)&Q(end_date__gt=end_date)))
        if self.instance:
            season = season.exclude(id=self.instance.id)

        if season:
                raise forms.ValidationError("Dates can't cross over into other seasons. Crossed over with %s" % (season[0].title))

        return data

    class Meta:
        model = bmodels.Season
        fields = ['start_date','end_date','title']
