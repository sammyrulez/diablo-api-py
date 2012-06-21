import context
import diablo
from unittest import TestCase
from mock_client import MockHttpClient


class TestCareer(TestCase):

    def test_career_load(self):
        c = diablo.Client('host', 'battletag_name', 'battletag_number')
        c.http_client = MockHttpClient()
        career = c.career_profile()
        self.assertTrue(career.heroes)
        self.assertTrue(len(career.heroes) > 0)
        self.assertTrue(career.heroes[0].name)
        self.assertTrue(career.heroes[0].gender)
        self.assertEquals(career.heroes[0].gender, 'Male')
        self.assertTrue(career.last_hero_played)
        self.assertTrue(career.last_hero_played.name)
        self.assertTrue(career.last_updated)
        self.assertTrue(career.kills)
        self.assertTrue(career.kills.monsters)
        self.assertTrue(career.kills.elites)
        self.assertTrue(career.kills.hardcoreMonsters)


class TestHero(TestCase):

    def test_hero_load(self):
        c = diablo.Client('host', 'battletag_name', 'battletag_number')
        c.http_client = MockHttpClient()
        hero = c.load_hero("name")
        self.assertTrue(hero['class'])
        self.assertEquals(hero['class'], 'barbarian')

    def test_lazyness(self):
        c = diablo.Client('host', 'battletag_name', 'battletag_number')
        c.http_client = MockHttpClient()
        career = c.career_profile()
        self.assertTrue(career.heroes[0].skills)
        self.assertTrue(career.heroes[0].skills.active)
        self.assertTrue(career.heroes[0].skills.passive)
        for skill_emelement in career.heroes[0].skills.active:
                self.assertTrue(skill_emelement)
                self.assertTrue(skill_emelement.skill)
                self.assertTrue(skill_emelement.rune)
        self.assertEquals(career.heroes[0].gender, 'Male')
