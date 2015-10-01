from django.test import TestCase
from django.test.client import Client

class BaseTestCase(TestCase):
    fixtures = [
            'user-test-data.json',
            'game-test-data.json',
            'statline-test-data.json',
            'player-test-data.json',
            'playbyplay-test-data.json',
            'season-test-data.json'
    ]

    def setUp(self):
        self.client = Client()

