from basketball import models as bmodels
from django_filters import rest_framework as drf_filters
import django_filters

class StatlineFilter(drf_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter()
    game_type = django_filters.CharFilter()

    class Meta:
        model = bmodels.StatLine
        fields = ['date']

class DailyStatlineFilter(StatlineFilter):
    class Meta:
        model = bmodels.DailyStatline
        fields = ['date']

class SeasonStatlineFilter(drf_filters.FilterSet):
    game_type = django_filters.CharFilter()
    
    class Meta:
        model = bmodels.SeasonStatline
        fields = ['season']
