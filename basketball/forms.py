from django import forms
from basketball import models as bmodels
from django.db.models import Q
import django_filters
from django.db import models

class LoginForm(forms.Form):
	username = forms.CharField(max_length=30,required=True)
	password = forms.CharField(max_length=30, widget=forms.PasswordInput)

class PlayerForm(forms.ModelForm):
    required_css_class = 'required'
    
    class Meta:
        model = bmodels.Player
        exclude = [""]

class GameForm(forms.ModelForm):
    required_css_class = 'required'

    def __init__(self,*args,**kwargs):
       super(GameForm,self).__init__(*args,**kwargs)
       self.fields['team1'].widget.attrs = {"size":15}
       self.fields['team2'].widget.attrs = {"size":15}
   
    class Meta:
        model = bmodels.Game
        exclude = ['winning_players']

class PlayByPlayForm(forms.ModelForm):
    required_css_class = 'required'

    def __init__(self,game,*args,**kwargs):
        super(PlayByPlayForm,self).__init__(*args,**kwargs)
        self.fields['primary_player'].queryset = bmodels.Player.objects.filter(Q(team1_set=game)|Q(team2_set=game)).distinct() 
        self.fields['secondary_player'].queryset = bmodels.Player.objects.filter(Q(team1_set=game)|Q(team2_set=game)).distinct()
        self.fields['assist_player'].queryset = bmodels.Player.objects.filter(Q(team1_set=game)|Q(team2_set=game)).distinct()
        self.fields['top_play_players'].queryset = bmodels.Player.objects.filter(Q(team1_set=game)|Q(team2_set=game)).distinct()

    class Meta:
        model = bmodels.PlayByPlay
        exclude = ['game']

class PlayByPlayFileForm(forms.Form):
    pbpFile = forms.FileField(label="Play By Play File", help_text="Only upload .csv files")


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

    def __init__(self,*args,**kwargs):
        game = kwargs.pop('game',None)
        super(PlayByPlayFilter,self).__init__(*args,**kwargs)
        self.filters['primary_play'].field.widget.attrs = {'class':'form-control'}
        self.filters['primary_player'].extra['queryset']=bmodels.Player.objects.filter(Q(team1_set=game)|Q(team2_set=game)).distinct()
        self.filters['primary_player'].field.widget.attrs = {'class':'form-control'}
        self.filters['secondary_play'].field.widget.attrs = {'class':'form-control'}
        self.filters['secondary_player'].extra['queryset'] = bmodels.Player.objects.filter(Q(team1_set=game)|Q(team2_set=game)).distinct()
        self.filters['secondary_player'].field.widget.attrs = {'class':'form-control'}
        self.filters['assist'].field.widget.attrs = {'class':'form-control'}
        self.filters['assist_player'].extra['queryset'] = bmodels.Player.objects.filter(Q(team1_set=game)|Q(team2_set=game)).distinct()
        self.filters['assist_player'].field.widget.attrs = {'class':'form-control'}
    class Meta:
        model = bmodels.PlayByPlay
        fields = ['primary_play', 'primary_player','secondary_play','secondary_player','assist','assist_player']

class SeasonForm(forms.Form):
    season = forms.ModelChoiceField(queryset=bmodels.Season.objects.all(),empty_label="All",required=False)
    possessions_min = forms.IntegerField(label="Minimum Possessions",min_value=1)
