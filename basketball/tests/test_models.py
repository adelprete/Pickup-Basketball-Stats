from django.db.models import Sum
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse 
from basketball.tests.test_base import BaseTestCase
from basketball import models as bmodels

class PlayerUnitTests(BaseTestCase):

    player = bmodels.Player.objects.get(id=9)
    season = bmodels.Season.objects.get(id=2)
    
    def test_full_name(self):
        self.assertTrue(isinstance(self.player, bmodels.Player))
        player = bmodels.Player.objects.get(id=9)
        self.assertEqual(player.get_full_name(), "Anthony Delprete")

    def test_total_wins(self):
        self.assertTrue(isinstance(self.player.total_wins(season=self.season), int))
    
    def test_total_losses(self):
        self.assertTrue(isinstance(self.player.total_losses(season=self.season), int))
    
    def test_total_games(self):
        self.assertTrue(isinstance(self.player.total_games(season=self.season), int))

    def test_per_100_data(self):
        #test fgm_percent
        per_100_statistics = ['dreb', 'oreb', 'asts', 'pot_ast', 'stls', 'to', 'blk',
                'points', 'total_rebounds', 'fgm_percent', 'threepm_percent',
                'dreb_percent', 'oreb_percent', 'treb_percent', 'ts_percent',
                'off_rating', 'def_rating', 'tp_percent']

        self.assertTrue(isinstance(self.player.get_per_100_possessions_data(per_100_statistics, game_type='5v5', season_id=self.season.id), dict))

    def test_get_averages(self):
        self.assertTrue(isinstance(self.player.get_averages(['points']), dict))
    
    def test_get_totals(self):
        self.assertTrue(isinstance(self.player.get_totals(['points']), dict))



class GameUnitTests(BaseTestCase):

    game = bmodels.Game.objects.get(id=2)

    def test_str(self):
        self.assertEqual(self.game.__str__(), "2015-06-13: Game 1")

    def test_absolute_url(self):
        self.assertEqual(self.game.get_absolute_url(), "/games/2/box-score/")

    def test_calculate_game_score(self):
        self.game.calculate_game_score()
        self.assertEqual(self.game.team1_score, 11)
        self.assertEqual(self.game.team2_score, 9)

    def test_get_bench(self):
        self.assertTrue(isinstance(self.game.get_bench(), list))

    def test_calculate_statlines(self):
        self.game.reset_statlines()
        self.game.calculate_statlines()

    def test_off_def_possessions_count(self):
        team1_pos_count = self.game.statline_set.filter(player__pk__in=self.game.team1.values_list('pk',flat=True)).aggregate(Sum('def_pos'),Sum('off_pos'))
        team2_pos_count = self.game.statline_set.filter(player__pk__in=self.game.team2.values_list('pk',flat=True)).aggregate(Sum('def_pos'),Sum('off_pos'))

        self.assertEqual(team1_pos_count['def_pos__sum'], 150)
        self.assertEqual(team1_pos_count['off_pos__sum'], 156)
        self.assertEqual(team2_pos_count['def_pos__sum'], 156)
        self.assertEqual(team2_pos_count['off_pos__sum'], 150)


