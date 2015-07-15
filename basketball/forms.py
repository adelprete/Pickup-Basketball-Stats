from django import forms
from basketball import models as bmodels
from django.db.models import Q

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

    class Meta:
        model = bmodels.PlayByPlay
        exclude = ['game']

class PlayByPlayFileForm(forms.Form):
    pbpFile = forms.FileField(label="Play By Play File", help_text="Only upload .csv files")
