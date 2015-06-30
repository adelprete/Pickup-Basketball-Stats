from django import template

register = template.Library()

@register.inclusion_tag('box_score.html')
def box_score(statlines,bgcolor="white"):
    return {'statlines': statlines,'bgcolor':bgcolor}
