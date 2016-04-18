from basketball import models

from django import template
register = template.Library()


@register.inclusion_tag('records/game_table.html')
def game_records_table():
    """
    Returns a matrix of all time game records
    """

    # grab record matrix if it exists
    record_matrix = models.TableMatrix.objects.get_or_create(title="game_records")

    if record_matrix[0].out_of_date:
        array_matrix = []
        array_matrix.append(["Stat", "Name", "Value", "Date", "Game"])

        stats = [
            ('points', 'Points'),
            ('asts', 'Assists'),
            ('total_rebounds', 'Rebounds'),
            ('dreb', 'Defensive Rebounds'),
            ('oreb', 'Offensive Rebounds'),
            ('stls', 'Steals'),
            ('blk', 'Blocks'),
            ('fgm', 'Field Goals Made'),
            ('fga', 'Field Goals Attempted'),
            ('threepm', '3 Pointers Made'),
            ('threepa', '3 Pointers Attempted'),
            ('pot_ast', 'Potential Assists'),
            ('ba', 'Blocks Against'),
            ('to', 'Turnovers'),
            ('ast_points', 'Assisted Points'),
            ('ast_fgm', 'Assisted Field Goals Made'),
            ('ast_fga', 'Assisted Field Goal Attempts'),
            ('unast_fgm', 'Unassisted Field Goals Made'),
            ('unast_fga', 'Unassisted Field Goal Attempts'),
            ('pgm', 'Putbacks Made'),
            ('pga', 'Putbacks Attempted'),
            ('fastbreaks', 'Fastbreaks'),
            ('fastbreak_points', 'Fastbreak Points'),
            ('second_chance_points', 'Second Chance Points'),
        ]

        # Most points scored in a game
        for stat in stats:
            statlines = models.StatLine.objects.filter(game__points_to_win='11').order_by("-" + stat[0],"-game__date")[:20]
            record = getattr(statlines[0], stat[0], 0)
            for statline in statlines:
                row = []
                if record == 0:
                    array_matrix.append([stat[1], "none", "none", "none", "none"])

                if getattr(statline, stat[0], 0) == record:
                    if statline is statlines[0]:
                        row.append(stat[1])
                    else:
                        row.append("")
                    row.append(statline.player)
                    row.append(getattr(statline, stat[0], 0))
                    row.append(statline.game.date)
                    row.append(statline.game.title)
                    array_matrix.append(row)
                else:
                    break

    return {"table_matrix":array_matrix}
