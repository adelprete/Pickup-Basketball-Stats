# these are headers that we pass into a base_table template to quickly create a table
totals_statistics = [
        {'stat':'gp', 'header':'GP', 'title':'Games Played'},
        {'stat':'fgm', 'header':'FGM', 'title':'Field Goals Made (Any made basket)'},
        {'stat':'fga', 'header':'FGA', 'title':'Field Goals Attempted (Any basket attempted)'},
        {'stat':'threepm', 'header':'3PM', 'title':'Three Pointers Made (Any shot made behind te 3point line)'},
        {'stat':'threepa', 'header':'3PA', 'title':'Three Pointers Attempted (Any shot attempted behind the 3point line)'},
        {'stat':'oreb', 'header':'OFF', 'title':'Offensive Rebounds (A rebound after a teammate/self misses)'},
        {'stat':'dreb', 'header':'DEF', 'title':'defensive Rebounds (A rebound after an opponent misses)'},
        {'stat':'total_rebounds', 'header':'REB', 'title':'Total Rebounds (A rebound after any miss)'},
        {'stat':'asts', 'header':'AST', 'title':'Assists (A pass that leads to a score)'},
        {'stat':'pot_ast', 'header':'P.AST', 'title':"Potential Assists (A pass that would've lead to a score if the receiver made the shot)"},
        {'stat':'to', 'header':'TO', 'title':'Turnover (Anytime you give the ball to the other team)'},
        {'stat':'stls', 'header':'STL', 'title':'Steals (Anytime you cause a turnover from the other team)'},
        {'stat':'blk', 'header':'BLK', 'title':'Blocks (Whenver you deflect a shot attempt)'},
        {'stat':'ba', 'header':'BA', 'title':'Blocks Allowed (How many shot attempts have been deflected)'},
        {'stat':'fd', 'header':'FD', 'title':'Fouls Drawn (Whenever you are fouled)'},
        {'stat':'pf', 'header':'PF', 'title':'Personal Fouls (Amount of fouls that you have been called on)'},
        {'stat':'points', 'header':'PTS', 'title':'Points (Amount of points scored)'},
        ]

adv_totals_statistics = [
        {'stat':'gp', 'header':'GP', 'title':'Games Played'},
        {'stat':'ast_fgm', 'header':'AST FGM', 'title':'Assisted Field Goals Made'},
        {'stat':'ast_fga', 'header':'AST FGA', 'title':'Assisted Field Goal Attempts'},
        {'stat':'unast_fgm', 'header':'UNAST FGM', 'title':'Unassisted Field Goals Made'},
        {'stat':'unast_fga', 'header':'UNAST FGA', 'title':'Unassisted Field Goal Attempts'},
        {'stat':'ast_points', 'header':'AST PTS', 'title':'Assisted Points (Points scored off your assists)'},
        {'stat':'pgm', 'header':'PGM', 'title':'Putbacks Made'},
        {'stat':'pga', 'header':'PGA', 'title':'Putbacks Attempted'},
        {'stat':'fastbreak_points', 'header':'FB PTS', 'title':'FastBreak Points'},
        {'stat':'second_chance_points', 'header':'SC PTS', 'title':'Second Chance Points'},
        {'stat':'def_pos', 'header':'DEF.POS', 'title':'Defensive Possessions'},
        {'stat':'off_pos', 'header':'OFF.POS', 'title':'Offensive Possessions'},
        {'stat':'dreb_opp', 'header':'DREB.OPP', 'title':'Defensive Rebound Opportunities'},
        {'stat':'oreb_opp', 'header':'OREB.OPP', 'title':'Offensive Rebound Opportunities'},
        ]

per_100_statistics = [
        {
            'stat':'gp',
            'header':'GP',
            'full_name':'Games Played',
            'title':'Games Played'
        },
        {
            'stat':'points',
            'header':'Points',
            'full_name':'Points',
            'title':'Points'
        },
        {
            'stat':'fgm_percent',
            'header':'FGM %',
            'full_name':'Field Goals Made %',
            'title':'Field Goal Percentage.  Percentage of Field Goals Made'
        },
        {
            'stat':'threepm_percent',
            'header':'3PM %',
            'full_name': '3 Points Made %',
            'title':'3 Point Percentage. Percentage of 3 pointers made'
        },
        {
            'stat':'asts',
            'header':'Asts',
            'full_name': 'Assists',
            'title':'Assists'
        },
        {
            'stat':'pot_ast',
            'header':'P.Asts',
            'full_name': 'Potential Assists',
            'title':'Potential Assists. A pass that would’ve lead to a score if the receiver made the shot.'
        },
        {
            'stat':'dreb',
            'header':'Dreb',
            'full_name': 'Defensive Rebounds',
            'title':'Defensive Rebounds'
        },
        {
            'stat':'oreb',
            'header':'Oreb',
            'full_name': 'Offensive Rebounds',
            'title':'Offensive Rebounds'
        },
        {
            'stat':'dreb_percent',
            'header':'Dreb %',
            'full_name': 'Defensive Rebound %',
            'title':'Percentage of defensive rebounds grabbed against total defensive rebounds available'
        },
        {
            'stat':'oreb_percent',
            'header':'Oreb %',
            'full_name': 'Offensive Rebound %',
            'title':'Percentage of offensive rebounds grabbed against total offensive rebounds available'
        },
        {
            'stat':'total_rebounds',
            'header':'Reb',
            'full_name': 'Total Rebounds',
            'title':'Total Rebounds'
        },
        {
            'stat':'treb_percent',
            'header':'Reb %',
            'full_name': 'Total Rebound %',
            'title':'Percentage of possessions that result in a rebound'
        },
        {
            'stat':'stls',
            'header':'Stls',
            'full_name': 'Steals',
            'title':'Steals (Anytime you cause a turnover from the other team)'
        },
        {
            'stat':'to',
            'header':'To',
            'full_name': 'Turnovers',
            'title':'Turnovers'
        },
        {
            'stat':'blk',
            'header':'Blk',
            'full_name': 'Blocks',
            'title':'Blocks (Whenever you deflect a shot attempt)'
        },
        {
            'stat':'off_rating',
            'header':'Off.Rating',
            'full_name': 'Offensive Rating',
            'title':"Points scord per 100 possessions while you're on the floor"
        },
        {
            'stat':'def_rating',
            'header':'Def.Rating',
            'full_name': 'Defensive Rating',
            'title':"Points scored against your per 100 possessions while you're on the floor"
        },
]

adv_per_100_statistics = [
        {
            'stat':'gp',
            'header':'GP',
            'full_name': 'Games Played',
            'title':'Games Played'
        },
        {
            'stat':'ts_percent',
            'header':'TS %',
            'full_name': 'True Shooting %',
            'title':'True Shooting Percentage. Percentage of Field Goals made with the 3 pointers weighed higher.  Formula is Points / FGA'
        },
        {
            'stat':'tp_percent',
            'header':'TP %',
            'full_name': 'True Passing %',
            'title':'True Passing Percentage. Percentage of points made following your assists and potential assists'
        },
        {
            'stat':'ast_fgm_percent',
            'header':'AST FGM %',
            'full_name': 'Assisted FGM %',
            'title':'Assisted Shooting %.  Shooting percentage of shots that were assisted by another player.'
        },
        {
            'stat':'ast_fga_percent',
            'header':'AST FGA %',
            'full_name': 'Assisted FGA %',
            'title':'Assisted Field Goal %. Percentage of shots attempted that were assisted by another player.'
        },
        {
            'stat':'unast_fgm_percent',
            'header':'UNAST FGM %',
            'full_name': 'Unassisted FGM %',
            'title':'Unassisted Shooting %. Shooting percentage of shots that were not assisted by another player.'
        },
        {
            'stat':'unast_fga_percent',
            'header':'UNAST FGA %',
            'full_name': 'Unassisted FGA %',
            'title':'Unassisted Field Goal %. Percentage of shots attempted that were not assisted by another player.'
        },
        {
            'stat':'pgm_percent',
            'header':'PGM %',
            'full_name': 'Putback Goals Made %',
            'title':'Putback Shooting %.  Percentage of putbacks that go in.'
        },
        {
            'stat':'pga_percent',
            'header':'PGA %',
            'full_name': 'Putback Field Goals  %',
            'title':'Putback Field Goal %.  Percentage of shots that are considered putbacks.'
        },
        ]
