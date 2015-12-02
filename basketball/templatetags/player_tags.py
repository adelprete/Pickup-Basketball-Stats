from django import template
from collections import OrderedDict

from basketball import models as bmodels
from basketball import headers
register = template.Library()

@register.inclusion_tag('players/highlights.html')
def player_highlights(player_pk):
    top_plays = bmodels.PlayByPlay.objects.filter(top_play_rank__startswith='t', top_play_players__pk=player_pk)
    not_top_plays = bmodels.PlayByPlay.objects.filter(top_play_rank__startswith='nt', top_play_players__pk=player_pk)

    context = {
        'top_plays': top_plays,
        'not_top_plays': not_top_plays
    }
    return context


def calculate_player_possessions_dictionaries(context, headers, player_id=None, sort_column=""):
    
    seasons = bmodels.Season.objects.all()
    player = bmodels.Player.objects.get(id=player_id)

    possessions_tables = OrderedDict() 

    # For each game type we create a list of each player's per 100 stats
    for game_type in bmodels.GAME_TYPES:
        
        possessions_tables[game_type[1]] = []
        
        for season in seasons:
            
            if player.get_possessions_count(game_type=game_type[0], season_id=season.id) >= 100:
                season_data = {'title': season.title}
                stats_list = [header['stat'] for header in headers if header['stat'] != 'gp']
                season_data.update(player.get_per_100_possessions_data(stats_list, game_type[0], season_id=season.id))
                
                # Lastly, count how many games the player played
                statlines = player.statline_set.filter(game__game_type=game_type[0], game__date__range=(season.start_date, season.end_date))
                season_data['gp'] = statlines.count()

                possessions_tables[game_type[1]].append(season_data)

    return possessions_tables

@register.inclusion_tag('players/stats_tab.html', takes_context=True)
def player_possessions(context, player_id):
    """Return a player's per 100 stats for each season"""
    possessions_tables = calculate_player_possessions_dictionaries(context,headers.per_100_statistics, player_id=player_id)
    
    context = {
        'tables': possessions_tables,
        'active_pill': '5on5',
        'headers': headers.per_100_statistics,
    }
    return context

@register.inclusion_tag('players/stats_tab.html', takes_context=True)
def player_adv_possessions(context, player_id):
    """Return a player's per 100 stats for each season"""
    possessions_tables = calculate_player_possessions_dictionaries(context,headers.adv_per_100_statistics, player_id=player_id)
    
    context = {
        'tables': possessions_tables,
        'active_pill': '5on5',
        'headers': headers.adv_per_100_statistics,
    }
    return context

def calculate_player_totals_dictionaries(context, statistics, player_id=None):
	
        player = bmodels.Player.objects.get(id=player_id)
        seasons = bmodels.Season.objects.all()

        totals_tables = OrderedDict()
        totals_footer = {}
        # For each game type we create a list of each player's total stats
        for game_type in bmodels.GAME_TYPES:
            totals_tables[game_type[1]] = []
            totals = {}
            for season in seasons:
               
                if player.get_possessions_count(game_type=game_type[0], season_id=season.id) > 0:
                    season_data = {'title': season.title}
                    
                    stats_list = [header['stat'] for header in statistics if header['stat'] != 'gp']
                    season_data.update(player.get_totals(stats_list, game_type=game_type[0], season=season))
                    
                    # Lastly, count how many games the player played
                    statlines = player.statline_set.filter(game__game_type=game_type[0], game__date__range=(season.start_date, season.end_date))
                    season_data['gp'] = statlines.count()

                    totals_tables[game_type[1]].append(season_data)
                    for key, value in season_data.items():
                        if key is not 'title':
                            if key in totals:
                                totals[key] += value
                            else:
                                totals[key] = value

            totals_footer[game_type[1]] = totals

        return totals_tables, totals_footer

@register.inclusion_tag('players/stats_tab.html', takes_context=True)
def player_totals(context, player_id):
        """Returns a dictionary of totals for a player by Season"""

        totals_tables, totals_footer = calculate_player_totals_dictionaries(context,headers.totals_statistics[1:],player_id=player_id)
        context = {
            'tables': totals_tables,
            'totals_footer': totals_footer,
            'active_pill': '5on5',
            'headers': headers.totals_statistics
            }
        
        return context


