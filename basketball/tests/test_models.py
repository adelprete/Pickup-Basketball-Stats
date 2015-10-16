from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse 
from basketball.tests.test_base import BaseTestCase
from basketball import models as bmodels

class PlayerUnitTests(BaseTestCase):

    def test_full_name(self):
        player = bmodels.Player.objects.get(id=9)
        self.assertTrue(isinstance(player, bmodels.Player))
        self.assertEqual(player.get_full_name(), "Anthony Delprete")

    def test_total_wins(self):
        player = bmodels.Player.objects.get(id=9)
        season = bmodels.Season.objects.get(id=2)
        self.assertTrue(isinstance(player.total_wins(season=season), int))
    
    def test_total_losses(self):
        player = bmodels.Player.objects.get(id=9)
        season = bmodels.Season.objects.get(id=2)
        self.assertTrue(isinstance(player.total_losses(season=season), int))
    
    def test_total_games(self):
        player = bmodels.Player.objects.get(id=9)
        season = bmodels.Season.objects.get(id=2)
        self.assertTrue(isinstance(player.total_games(season=season), int))

    def test_per_100_data(self):
        player = bmodels.Player.objects.get(id=9)
        season = bmodels.Season.objects.get(id=2)

        #test fgm_percent
        per_100_statistics = ['dreb', 'oreb', 'asts', 'pot_ast', 'stls', 'to', 'blk',
                'points', 'total_rebounds', 'fgm_percent', 'threepm_percent',
                'dreb_percent', 'oreb_percent', 'treb_percent', 'ts_percent',
                'off_rating', 'def_rating', 'tp_percent']

        for stat in per_100_statistics:
            self.assertTrue(isinstance(player.get_per_100_possessions_data(stat, game_type='5v5', season_id=season.id), float))

    def test_get_averages(self):
        player = bmodels.Player.objects.get(id=9)
        self.assertTrue(isinstance(player.get_averages('points'), float))
    
    def test_get_totals(self):
        player = bmodels.Player.objects.get(id=9)
        self.assertTrue(isinstance(player.get_totals('points'), int))



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



