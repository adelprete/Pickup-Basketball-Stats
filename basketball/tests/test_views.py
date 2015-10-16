from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from basketball.tests.test_base import BaseTestCase

class RequestTests(BaseTestCase):

    def test_homepage(self):
        response = self.client.get(reverse("root"))
        self.failUnlessEqual(response.status_code, 200)

    #game pages
    def test_games_homepage(self):
        response = self.client.get(reverse("games_home"))
        self.failUnlessEqual(response.status_code, 200)

    def test_game_page(self):
        response = self.client.get(reverse("box_score", kwargs={"id": 2}))
        self.failUnlessEqual(response.status_code, 200)

    def test_game_edit_page(self):
        response = self.client.get(reverse("edit_game", kwargs={"game_id": 2}))
        self.failUnlessEqual(response.status_code, 200)

    def test_playbyplay_edit_page(self):
        response = self.client.get(reverse("playbyplay_detail", kwargs={"game_id": 2, "play_id": 69}))
        self.failUnlessEqual(response.status_code, 200)

    def test_create_game_page(self):
        response = self.client.get(reverse("create_game"))
        self.failUnlessEqual(response.status_code, 200)

    def test_recap_page(self):
        response = self.client.get(reverse("recap", kwargs={"game_id": 2}))
        self.failUnlessEqual(response.status_code, 200)


    #player tests
    def test_players_homepage(self):
        response = self.client.get(reverse("players_home"))
        self.failUnlessEqual(response.status_code, 200)

    def test_player_page(self):
        response = self.client.get(reverse("player_page", kwargs={"id": 8}))
        self.failUnlessEqual(response.status_code, 200)

    def test_edit_player_page(self):
        response = self.client.get(reverse("edit_player", kwargs={"id": 8}))
        self.failUnlessEqual(response.status_code, 200)

    def test_create_player_page(self):
        response = self.client.get(reverse("create_player"))
        self.failUnlessEqual(response.status_code, 200)

    #leaderboard tests
    def test_leaderboard_page(self):
        response = self.client.get(reverse("leaderboard_home"))
        self.failUnlessEqual(response.status_code, 200)

    def test_leaderboard_filter(self):
        response = self.client.get("%s?season=&possessions_min=100&submit=" % reverse("leaderboard_home"))
        self.failUnlessEqual(response.status_code, 200)

    def test_leaderboard_totals_col_sort(self):
        response = self.client.get("%s?tot_sort=fgm&tot_active_pill=5on5&default_tab=totals&possessions_min=100&submit=&season=" \
                % reverse("leaderboard_home"))
        self.failUnlessEqual(response.status_code, 200)

    def test_leaderboard_totals_col_sort(self):
        response = self.client.get("%s?adv_tot_sort=ast_fgm&adv_tot_active_pill=5on5&default_tab=adv_totals&possessions_min=100&submit=&season=" \
                % reverse("leaderboard_home"))
        self.failUnlessEqual(response.status_code, 200)
