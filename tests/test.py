import context
import diablo
from unittest import TestCase
from mock_client import MockHttpClient


class TestCareer(TestCase):

    def test_career_load(self):
        career = diablo.career_profile(diablo.US_SERVER, 'battletag_name', 'battletag_number', http_client=MockHttpClient())
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
        hero = diablo.load_hero(diablo.US_SERVER, 'battletag_id', 'heroname', http_client=MockHttpClient())
        self.assertTrue(hero['class'])
        self.assertEquals(hero['class'], 'barbarian')

    def test_lazyness(self):
        mock_client = MockHttpClient()
        career = diablo.career_profile(diablo.US_SERVER, 'battletag_name', 'battletag_number', http_client=mock_client)
        self.assertTrue(career.heroes)
        my_hero = career.heroes[0]
        my_hero.http_client = mock_client
        self.assertTrue(my_hero.skills)
        self.assertTrue(my_hero.skills.active)
        self.assertTrue(my_hero.skills.passive)
        self.assertTrue(my_hero.items)
        self.assertTrue(my_hero.items['mainHand'])
        mainHand = my_hero.items['mainHand']
        mainHand.http_client = mock_client
        self.assertTrue(mainHand.itemLevel)
        for skill_emelement in my_hero.skills.active:
                self.assertTrue(skill_emelement)
                self.assertTrue(skill_emelement.skill)
                self.assertTrue(skill_emelement.rune)
        self.assertEquals(my_hero.gender, 'Male')
