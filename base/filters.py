from base.models import MemberPermission
from django_filters import rest_framework as drf_filters
import django_filters

class MemberPermissionFilter(drf_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter()
    game_type = django_filters.CharFilter()

    class Meta:
        model = MemberPermission
        fields = ['id', 'group']
