from django import template
from basketball.models import ALL_PLAY_TYPES
from django.db.models import Sum

register = template.Library()

@register.inclusion_tag('box_score.html')
def box_score(statlines,bgcolor="white"):
	team_totals = {}
	for play in ALL_PLAY_TYPES:
		x = statlines.aggregate(Sum(play[0]))
		team_totals.update(x)
	team_totals.update(statlines.aggregate(Sum('points'),Sum('total_rebounds')))
	return {'statlines': statlines,'team_totals':team_totals,'bgcolor':bgcolor}
