
import requests
import json


def is_sequence(arg):
    return (not hasattr(arg, "strip") and not hasattr(arg, "iterkeys") and
            hasattr(arg, "__getitem__") and
            hasattr(arg, "__iter__"))


def is_dictionary(arg):
    return (not hasattr(arg, "strip")  and hasattr(arg, "iterkeys") and
            hasattr(arg, "__getitem__") and
            hasattr(arg, "__iter__"))


def sanitize_key(arg):
    return arg.replace(" ", "_").replace("-", "_")


class Client(object):

    def __init__(self, host):
        self.host = host
        self.http_client = requests

    def career_profile(self, battletag_name, battletag_number):
        battle_id = "%s-%s" % (battletag_name, str(battletag_number))
        url = "http://%s/api/d3/account/%s" % (self.host, battle_id)
        r = self.http_client.get(url)
        data = json.loads(r.text)
        return Career(data, self)

    def load_hero(self, battle_id, hero_name):
        url = "http://%s/api/d3/account/%s/hero/%s" % (self.host, battle_id, hero_name)
        r = self.http_client.get(url)
        data = json.loads(r.text)
        active_sk = []
        passive_sk = []
        for skill in data['skills']['active']:
            active_sk.append(Skill(skill))
        return active_sk, passive_sk


class ApiObject(object):
    """docstring for ApiObject"""
    def __init__(self, arg, http_client):
        self.http_client = http_client

        self.__dict__.update(self.fetch_map(arg))

    def fetch_list(self, arg):
        out = []
        for item in arg:
            out.append(ApiObject(item, self.http_client))
        return out

    def fetch_map(self, arg):
        out = {}
        for key in arg.keys():
            #print key
            out_key = sanitize_key(key)
            special_case = self.manage_special(out_key, arg[key])
            if special_case:
                out[out_key] = special_case
            elif is_dictionary(arg[key]):
                #print out_key , ' is a  dictionary'
                out[out_key] = ApiObject(arg[key], self.http_client)
            elif is_sequence(arg[key]):
                #print out_key , ' is a  list'
                out[out_key] = self.fetch_list(arg[key])
            else:
                out[out_key] = arg[key]
        return out

    def manage_special(self, key, value):
        manage_method = "manage_%s" % (key)
        print 'checking for ' , manage_method
        if hasattr(self, manage_method):
            return getattr(self, manage_method)(value)
        else:
            return None


class Career(ApiObject):

    def manage_last_hero_played(self, value):
        #out_hero = None
        f#or hero in self.heroes:
        #    if hero.id == value:
        #        out_hero = hero
        #return out_hero
        pass



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
        self.skill = map_descr['skill']
        self.rune =  map_descr['rune']
