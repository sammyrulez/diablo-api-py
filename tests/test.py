import os
import sys
parent_path = os.path.abspath("..")
sys.path.insert(0, parent_path)

from unittest import TestCase
import diablo
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
        self.assertTrue(hero.passive_skills)
        self.assertTrue(len(hero.active_skills) >0 )
        self.assertTrue(len(hero.passive_skills) > 0)
        self.assertTrue(hero.active_skills[0].skill.name)
        self.assertTrue(hero.passive_skills[0].name)
