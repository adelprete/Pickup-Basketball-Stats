from django import forms
from basketball import models as bmodels
from django.db.models import Q
import django_filters
from django.db import models

class PlayByPlayForm(forms.ModelForm):

    def __init__(self,game,*args,**kwargs):
        super(PlayByPlayForm,self).__init__(*args,**kwargs)
        self.fields['time'].widget = forms.widgets.TimeInput(attrs={'class':'form-control'})
        self.fields['primary_play'].widget.attrs = {'class':'form-control'}
        self.fields['primary_player'].widget.attrs = {'class':'form-control'}
        self.fields['secondary_play'].widget.attrs = {'class':'form-control'}
        self.fields['secondary_player'].widget.attrs = {'class':'form-control'}
        self.fields['assist'].widget.attrs = {'class':'form-control'}
        self.fields['assist_player'].widget.attrs = {'class':'form-control'}
        self.fields['primary_player'].queryset = bmodels.Player.objects.filter(Q(team1_set=game)|Q(team2_set=game)).distinct() 
        self.fields['secondary_player'].queryset = bmodels.Player.objects.filter(Q(team1_set=game)|Q(team2_set=game)).distinct()
        self.fields['assist_player'].queryset = bmodels.Player.objects.filter(Q(team1_set=game)|Q(team2_set=game)).distinct()

    """
    def clean_time(self):
        import pdb;pdb.set_trace()
        if len(self.cleaned_data['time'].strftime('%H:%M:%S').split(':')) != 3:
            raise forms.ValidationError('Time Must be HH:MM:SS')
        return self.cleaned_data['time']
    """
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
