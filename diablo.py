
import requests
import json


class Client(object):

    def __init__(self, host):
        self.host = host
        self.http_client = requests

    def career_profile(self, battletag_name, battletag_number):
        battle_id = "%s-%s" % (battletag_name, str(battletag_number))
        url = "http://%s/api/d3/account/%s" % (self.host,battle_id )
        r = self.http_client.get(url)
        data = json.loads(r.text)
        heroes = []
        for hero in data['heroes']:
            heroes.append(Hero(hero['name'], hero['id'], hero['gender'], hero['class'], hero['last-updated'], battle_id))
        last_hero_played = None
        for hero in heroes:
            if hero.id == data['last-hero-played']:
                last_hero_played = hero
        kills_map = data['kills']
        kills = Kills(kills_map['monsters'], kills_map['elites'], kills_map['hardcoreMonsters'])
        return Career(heroes, last_hero_played, data['last-updated'], kills)

    def load_hero(self,battle_id,hero_name):
        url = "http://%s/api/d3/account/%s/hero/%s" % (self.host, battle_id, hero_name)
        r = self.http_client.get(url)
        data = json.loads(r.text)
        active_sk = []
        passive_sk = []
        for skill in data['skills']['active']:
            active_sk.append(Skill(skill))
        for skill in data['skills']['passive']:
            passive_sk.append(SkillElement(skill['slug'], skill['name'], skill['description']))
        return active_sk, passive_sk


class Career(object):
    """docstring for Career"""
    def __init__(self, heroes, last_hero_played, last_updated, kills):
        self.heroes = heroes
        self.last_hero_played = last_hero_played
        self.last_updated = last_updated
        self.kills = kills


class Hero(object):

    genders = {0: 'Male', 1: 'Female'}

    __client__ = None
    active_skills = None
    passive_skills = None

    """docstring for Hero"""
    def __init__(self, name, id_param, gender, class_name, last_updated, career_id):
        self.career_id = career_id
        self.name = name
        self.id = id_param
        self.gender = self.genders[gender]
        self.class_name = class_name
        self.last_updated = last_updated

    def __lazy_load__(self):
        if self.__client__:
            self.active_skills , self.passive_skills = self.__client__.load_hero(self.career_id,self.name)

    def __getattribute__(self, name):
        if object.__getattribute__(self, name) == None and name in ['active_skills', 'passive_skills']:
            self.__lazy_load__()

        return object.__getattribute__(self, name)



class Kills(object):
    """docstring for kills"""
    def __init__(self, monsters, elites, hardcoreMonsters):
        self.monsters = monsters
        self.hardcoreMonsters = hardcoreMonsters
        self.elites = elites

class Skill(object):
    def __init__(self,map_descr):
        skill_element = map_descr['skill']
        self.skill = SkillElement(skill_element['slug'],skill_element['name'],skill_element['simpleDescription'])
        rune_element = map_descr['rune']
        self.rune = SkillElement(rune_element['slug'],rune_element['name'],rune_element['simpleDescription'])

class SkillElement(object):
    def __init__(self, slug ,name,simpleDescription):#TODO manage icon
        self.slug = slug
        self.name = name
        self.description = simpleDescription
