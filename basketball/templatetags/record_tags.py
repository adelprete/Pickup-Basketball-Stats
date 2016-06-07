from basketball import models as bmodels
from basketball import headers
from collections import OrderedDict

from django import template
register = template.Library()

IGNORED_STATS = [
    ('def_pos', 'Defensive Possessions'),
    ('off_pos', 'Offensive Possessions'),
    ('total_pos', 'Total Possessions'),
    ('dreb_opp', 'Dreb Opportunities'),
    ('oreb_opp', 'Oreb Opportunities'),
]

@register.inclusion_tag('records/game_table.html')
def game_records_table(points_to_win, season=None):
    """
    Returns a matrix of all time game records
    """
    tables = OrderedDict()

    for game_type in bmodels.GAME_TYPES:
        # grab record matrix if it exists
        record_matrix = bmodels.TableMatrix.objects.get_or_create(type="game_records",
                                                                 points_to_win=points_to_win,
                                                                 game_type=game_type[0],
                                                                 season=season)[0]
        if record_matrix.out_of_date:
            record_matrix.delete()
            array_matrix = []
            array_matrix.append(["Stat", "Name", "Value", "Date", "Game"])

            statlines = bmodels.StatLine.objects.filter(
                game__points_to_win=points_to_win,
                game__game_type=game_type[0]
            )
            if season:
                statlines = statlines.filter(
                    game__date__range=(season.start_date, season.end_date),
                )

            # Run through each stat and find the best statline for each one
            for stat in bmodels.STATS:
                if stat not in IGNORED_STATS:
                    statlines = statlines.order_by("-" + stat[0],"-game__date")

                    record = False
                    for statline in statlines:

                        if statline.player.get_possessions_count() < 200:
                            continue
                        elif not record:
                            record = getattr(statline, stat[0], 0)

                        row = []
                        if record == 0:
                            array_matrix.append([stat[1], "none", "none", "none", "none"])

                        if getattr(statline, stat[0], 0) == record:
                            array_matrix.append([
                                stat[1],
                                statline.player.get_full_name(),
                                str(getattr(statline, stat[0], 0)),
                                statline.game.date.strftime('%b %d %Y'),
                                statline.game.title,
                            ])
                        else:
                            break
            if len(array_matrix) > 1:
                matrix = bmodels.TableMatrix.objects.create(type="game_records",
                                                           points_to_win=points_to_win,
                                                           season=season,
                                                           game_type=game_type[0],
                                                           out_of_date=False)

                for y, row in enumerate(array_matrix):
                    for x, value in enumerate(row):
                        cell = bmodels.Cell.objects.create(row=y, column=x, value=value, matrix=matrix)
                        cell.save()

                tables[game_type[1]] = array_matrix

        else:
            array_matrix = []
            cells = record_matrix.cell_set.all()

            for i in range(0, int(cells.count()/5)):
                row = [
                    cells.get(row=i,column=0).value,
                    cells.get(row=i, column=1).value,
                    cells.get(row=i, column=2).value,
                    cells.get(row=i, column=3).value,
                ]
                array_matrix.append(row)

            if len(array_matrix) > 1:
                tables[game_type[1]] = array_matrix

    return {"tables":tables}

from django.db.models import Count, Min, Sum, Avg
@register.inclusion_tag('records/day_table.html')
def day_records_table(points_to_win,season=None):
    """
    Calculate records on achieved on a single day
    """
    tables = OrderedDict()

    for game_type in bmodels.GAME_TYPES:
        # grab record matrix if it exists
        record_matrix = bmodels.TableMatrix.objects.get_or_create(type="day_records",
                                                                 points_to_win=points_to_win,
                                                                 game_type=game_type[0],
                                                                 season=season)[0]

        if record_matrix.out_of_date:
            record_matrix.delete()
            array_matrix = []
            array_matrix.append(["Stat", "Name", "Value", "Date"])

            statlines = bmodels.DailyStatline.objects.filter(
                    points_to_win=points_to_win,
                    game_type=game_type[0]
                )
            if season:
                statlines = statlines.objects.filter(
                    date__range=(season.start_date, season.end_date),
                )

            # Run through each stat and find the best statline for each one
            for stat in bmodels.STATS:
                if stat not in IGNORED_STATS:

                    statlines = statlines.order_by("-" + stat[0], "-date")

                    record = False

                    for statline in statlines:

                        if statline.player.get_possessions_count() < 200:
                            continue
                        elif not record:
                            record = getattr(statline, stat[0], 0)

                        row = []
                        if record == 0:
                            array_matrix.append([stat[1], "none", "none", "none", "none"])

                        if getattr(statline, stat[0], 0) == record:
                            array_matrix.append([
                                stat[1],
                                statline.player.get_full_name(),
                                str(getattr(statline, stat[0], 0)),
                                statline.date.strftime('%b %d %Y'),
                            ])
                        else:
                            break

            if len(array_matrix) > 1:
                matrix = bmodels.TableMatrix.objects.create(type="day_records",
                                                           points_to_win=points_to_win,
                                                           season=season,
                                                           game_type=game_type[0],
                                                           out_of_date=False)

                for y, row in enumerate(array_matrix):
                    for x, value in enumerate(row):
                        cell = bmodels.Cell.objects.create(row=y, column=x, value=value, matrix=matrix)
                        cell.save()

                tables[game_type[1]] = array_matrix

        else:
            array_matrix = []
            cells = record_matrix.cell_set.all()

            for i in range(0, int(cells.count() / 5)):
                row = [
                    cells.get(row=i, column=0).value,
                    cells.get(row=i, column=1).value,
                    cells.get(row=i, column=2).value,
                    cells.get(row=i, column=3).value,
                ]
                array_matrix.append(row)

            if len(array_matrix) > 1:
                tables[game_type[1]] = array_matrix

    return {"tables": tables}

@register.inclusion_tag('records/season_table.html')
def season_records_table(points_to_win):
    """
    Calculate records achieved on during a season
    """
    tables = OrderedDict()

    for game_type in bmodels.GAME_TYPES:
        # grab record matrix if it exists
        record_matrix = bmodels.TableMatrix.objects.get_or_create(type="season_records",
                                                                 points_to_win=points_to_win,
                                                                 game_type=game_type[0])[0]

        if record_matrix.out_of_date:
            record_matrix.delete()
            array_matrix = []
            array_matrix.append(["Stat", "Name", "Value", "Season"])

            statlines = bmodels.SeasonStatline.objects.filter(
                points_to_win=points_to_win,
                game_type=game_type[0]
            )
            # Run through each stat and find the best statline for each one
            for stat in bmodels.STATS:
                if stat not in IGNORED_STATS:
                    statlines = statlines.order_by("-" + stat[0], "-season__end_date")

                    record = False

                    for statline in statlines:

                        if statline.player.get_possessions_count() < 200:
                            continue
                        elif not record:
                            record = getattr(statline, stat[0], 0)

                        row = []
                        if record == 0:
                            array_matrix.append([stat[1], "none", "none", "none", "none"])

                        if getattr(statline, stat[0], 0) == record:
                            array_matrix.append([
                                stat[1],
                                statline.player.get_full_name(),
                                str(getattr(statline, stat[0], 0)),
                                statline.season.title,
                            ])
                        else:
                            break

            if len(array_matrix) > 1:
                matrix = bmodels.TableMatrix.objects.create(
                    type="season_records",
                    points_to_win=points_to_win,
                    out_of_date=False,
                    game_type=game_type[0])

                for y, row in enumerate(array_matrix):
                    for x, value in enumerate(row):
                        cell = bmodels.Cell.objects.create(row=y, column=x, value=value, matrix=matrix)
                        cell.save()

                tables[game_type[1]] = array_matrix

        else:
            array_matrix = []
            cells = record_matrix.cell_set.all()

            for i in range(0, int(cells.count() / 4)):
                row = [
                    cells.get(row=i, column=0).value,
                    cells.get(row=i, column=1).value,
                    cells.get(row=i, column=2).value,
                    cells.get(row=i, column=3).value,
                ]
                array_matrix.append(row)

            if len(array_matrix) > 1:
                tables[game_type[1]] = array_matrix


    return {"tables": tables}

@register.inclusion_tag('records/season_per100_table.html')
def season_per100_records_table(points_to_win):
    """
    Calculate records achieved on during a season
    """
    tables = OrderedDict()

    stats = headers.per_100_statistics + headers.adv_per_100_statistics

    for game_type in bmodels.GAME_TYPES:
        # grab record matrix if it exists
        record_matrix = bmodels.TableMatrix.objects.get_or_create(type="season_per100_records",
                                                                 points_to_win=points_to_win,
                                                                 game_type=game_type[0])[0]

        if record_matrix.out_of_date:
            record_matrix.delete()
            array_matrix = []
            array_matrix.append(["Stat", "Name", "Value", "Season", ""])

            # Run through each stat and find the best statline for each one
            statlines = bmodels.SeasonPer100Statline.objects.filter(
                points_to_win=points_to_win,
                game_type=game_type[0]
            ).exclude(
                player__first_name__in=['Team1', 'Team2']
            )
            for stat in stats:
                if stat['stat'] != 'gp':
                    if stat['stat'] != 'def_rating':
                        statlines = statlines.order_by("-" + stat['stat'], "-season__end_date")
                    else:
                        statlines = statlines.order_by(stat['stat'], "-season__end_date")

                    record = False

                    percent_sign = ''
                    if stat['full_name'][-1] == '%':
                        percent_sign = '%'

                    for statline in statlines:

                        #Quickly check different stat categories to see if the player meets the minimum requiremeents
                        totals_statline = bmodels.SeasonStatline.objects.get(
                            player=statline.player,
                            game_type=game_type[0],
                            season=statline.season,
                            points_to_win=statline.points_to_win
                        )
                        if stat['stat'] in ['fgm_percent','ts_percent','unast_fgm_percent','unast_fga_percent','ast_fgm_percent','ast_fga_percent']:
                            if totals_statline.fga <= 30:
                                continue
                        if stat['stat'] == 'threepm_percent':
                            if totals_statline.threepa <= 30:
                                continue
                        if stat['stat'] == 'tp_percent':
                            if totals_statline.asts + totals_statline.pot_ast <= 40:
                                continue
                        if stat['stat'] == 'pgm_percent':
                            if totals_statline.pga <= 10:
                                continue
                        if totals_statline.off_pos < 200:
                            continue

                        #set a record if there isn't any yet
                        if not record:
                            record = getattr(statline, stat['stat'], 0)

                        row = []
                        if record == 0:
                            array_matrix.append([stat['full_name'], "none", "none", "none", "none"])

                        if getattr(statline, stat['stat'], 0) == record:
                            array_matrix.append([
                                stat['full_name'],
                                statline.player.get_full_name(),
                                str(getattr(statline, stat['stat'], 0)) + percent_sign,
                                statline.season.title,
                                stat['title']
                            ])
                        else:
                            break

            if len(array_matrix) > 1:
                matrix = bmodels.TableMatrix.objects.create(
                    type="season_per100_records",
                    points_to_win=points_to_win,
                    out_of_date=False,
                    game_type=game_type[0])

                for y, row in enumerate(array_matrix):
                    for x, value in enumerate(row):
                        cell = bmodels.Cell.objects.create(row=y, column=x, value=value, matrix=matrix)
                        cell.save()

                tables[game_type[1]] = array_matrix

        else:
            array_matrix = []
            cells = record_matrix.cell_set.all()

            for i in range(0, int(cells.count() / 5)):
                row = [
                    cells.get(row=i, column=0).value,
                    cells.get(row=i, column=1).value,
                    cells.get(row=i, column=2).value,
                    cells.get(row=i, column=3).value,
                    cells.get(row=i, column=4).value,
                ]
                array_matrix.append(row)

            if len(array_matrix) > 1:
                tables[game_type[1]] = array_matrix


    return {"tables": tables}


