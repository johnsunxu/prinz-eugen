from requests.models import requote_uri
from .weapon import _Weapon 

class _Plane(_Weapon):

    @property
    def _plane(self):
        return self._weapon["spawn"][0]

    @property
    def _armaments(self):
        return self._plane["weapons"]

    @property
    def hp(self):
        return self._plane["hp"]

    @property
    def speed(self):
        return self._plane["speed"]

    @property
    def crash_damage(self):
        return self._plane["crash_damage"]

    @property
    def dodge_limit(self):
        return self._plane["dodge_limit"]

    @property
    def armament(self):
        out = []

        for armament in self._armaments:
            out += [get_armament(armament)]

        return out

class _Armament:

    def __init__(self, data: dict) -> None:
        self.data = data

    @property
    def _spawn(self):
        return self.data["spawn"][0]

    @property
    def bullet_damage(self):
        return self.data["damage"]

    @property
    def name(self):
        return self.data["name"]["en"]

    @property
    def volley(self):
        #AP rockets are single int
        #Bombs are an array

        v = self._spawn["size"]

        if type(v) == int:
            return [1,v]
        else:
            return v

    @property
    def damage(self):
        return [self.bullet_damage, self.volley[0] * self.volley[1]]

class _AntiAircraftGun(_Armament):

    @property
    def reload(self):
        return self.reload

    @property
    def volley_time(self):
        return self._spawn["volley_time"]

class _Bomb(_Armament):
    pass

def get_armament(data):
    if data["spawn_bound"] == "antiaircraft":
        return _AntiAircraftGun(data)
    else:
        return _Bomb(data)