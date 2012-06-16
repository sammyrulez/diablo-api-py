import diablo
from unittest import TestCase
from mock_client import MockHttpClient


class TestCareer(TestCase):

    def test_career_load(self):
        c = diablo.Client('host')
        c.http_client = MockHttpClient()
        career = c.career_profile('battletag_name', 'battletag_number')
        self.assertTrue(career.heroes)
        self.assertTrue(len(career.heroes) > 0)
        self.assertTrue(career.heroes[0].name)
        self.assertTrue(career.last_hero_played)
        self.assertTrue(career.last_hero_played.name)
        self.assertTrue(career.last_updated)
        self.assertTrue(career.kills)
        self.assertTrue(career.kills.monsters)
        self.assertTrue(career.kills.elites)
        self.assertTrue(career.kills.hardcoreMonsters)

class TestHero(TestCase):

    def test_hero_load(self):
        c = diablo.Client('host')
        c.http_client = MockHttpClient()
        c.load_hero("ID","name")

    def test_hero_lazyness(self):

        hero =diablo.Hero("robin",4,0,'hunter',12321,'magnus-1')
        self.assertFalse(hero.active_skills)
        c = diablo.Client('host')
        c.http_client = MockHttpClient()
        hero.__client__ = c
        self.assertTrue(hero.active_skills)
