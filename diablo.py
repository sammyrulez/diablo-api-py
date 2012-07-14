import requests
import json

EU_SERVER = 'http://eu.battle.net'
US_SERVER = 'http://us.battle.net'
ASIA_SERVER = 'http://as.battle.net'


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

genders = {0: 'Male', 1: 'Female'}


def career_profile(host, battletag_name, battletag_number, http_client=requests):
    battle_id = "%s-%s" % (battletag_name, str(battletag_number))
    url = "%s/api/d3/account/%s" % (host, battle_id)
    r = http_client.get(url)
    if r.status_code == 200:
        data = json.loads(r.text)
        return Career(data, host, battle_id)
    else:
        raise Exception('Error:\n' + r.text)


def load_hero(host, battle_id, hero_name, http_client=requests):
    url = "%s/api/d3/account/%s/hero/%s" % (host, battle_id, hero_name)
    r = http_client.get(url)
    if r.status_code == 200:
        return json.loads(r.text)
    else:
        raise Exception('Error:\n' + r.text)


class ApiObject(object):
    """docstring for ApiObject"""
    def __init__(self, arg, host, battle_id):
        self.host = host
        self.battle_id = battle_id
        priority = {}
        for key in self.priority_boarding():
            out_key, out_element = self.route_element(key, arg[key])
            priority[out_key] = out_element
            arg.pop(key)
        if priority:
            self.__dict__.update(priority)

        self.__dict__.update(self.fetch_map(arg))

    def fetch_list(self, arg):
        out = []
        for item in arg:
            out.append(ApiObject(item, self.host, self.battle_id))
        return out

    def route_element(self, key, value):
        out_key = sanitize_key(key)
        out_element = None
        special_case = self.manage_special_case(out_key, value)
        if special_case:
            out_element = special_case
        elif is_dictionary(value):
            out_element = ApiObject(value, self.host, self.battle_id)
        elif is_sequence(value):
            out_element = self.fetch_list(value)
        else:
            out_element = value
        return out_key, out_element

    def fetch_map(self, arg):
        out = {}
        for key in arg.keys():
            out_key, out_element = self.route_element(key, arg[key])
            out[out_key] = out_element
        return out

    def manage_special_case(self, key, value):
        manage_method = "manage_%s" % (key)
        if hasattr(self, manage_method):
            return getattr(self, manage_method)(value)
        else:
            return None

    def priority_boarding(self):
        return []


class LazyObject(ApiObject):

    hydrate = False
    http_client = requests

    def http_client_callback(self):
        pass

    def __getattribute__(self, name):
        if not object.__getattribute__(self, 'hydrate') and name in  object.__getattribute__(self, 'lazy_load_attrs')():
            data = self.http_client_callback()
            self.__dict__.update(self.fetch_map(data))
            object. __setattr__(self, 'hydrate', True)
        return object.__getattribute__(self, name)


class Career(ApiObject):

    def manage_last_hero_played(self, value):
        out_hero = None
        for hero in self.heroes:
            if hero.id == value:
                out_hero = hero
        return out_hero

    def priority_boarding(self):
        return ['heroes']

    def manage_heroes(self, value):
        heroes = []
        for hero in value:
            heroes.append(Hero(hero, self.host, self.battle_id))
        return heroes

    def manage_gender(self, value):
        return genders[value]


class Hero(LazyObject):

    def lazy_load_attrs(self):
        return ['skills', 'items', 'followers', 'progress']

    def http_client_callback(self):
        return load_hero(self.host, self.battle_id, self.name, http_client=self.http_client)

    def manage_gender(self, value):
        return genders[value]
