from typing import List

from requests.models import requote_uri
from .gear import _Gear
from .._ships.ship import _Ship

import math

class _Weapon(_Gear):

    @property
    def _weapon(self):
        return self.gear["weapons"][self.level]

    @property
    def reload(self) -> float:
        return self.gear["weapons"][self.level]["reload"]

    def get_reload_on_ship(self, ship: _Ship) -> float:
        ship_reload = ship.stats["rld"]
        result_number = self.reload * math.sqrt(200/(100+ship_reload))
        return round(result_number,2)

    @property
    def coefficient(self) -> int:
        return self._weapon["coefficient"]

    @property
    def damage(self) -> List:
        pass


class _VanguardWeapon(_Weapon):

    @property
    def _spawn(self):
        return self._weapon["spawn"][0]

    @property
    def firing_angle(self) -> int:
        return self._weapon["firing_angle"]

    @property
    def armor_mods(self) -> List[int]:
        return self._spawn["armor_mods"]

    @property
    def shell_damage(self) -> int:
        return self._weapon["damage"]


class _Gun(_VanguardWeapon):

    @property
    def spread(self) -> int:
        return self._spawn["angle"]

    @property
    def volley(self):
        return self._spawn["size"]

    @property
    def volley_time(self):
        return self._spawn["volley_time"]

    @property
    def range(self):
        return {
            "firing" : self._spawn["firing_range"],
            "shell" : self._spawn["shell_range"],
        }

    @property
    def damage(self) -> List[int]:
        return [self.shell_damage,self._spawn['size'][0] * self._spawn['size'][1]]

class _Torpedo(_VanguardWeapon):

    @property
    def damage(self) -> List[int]:
        return [self.shell_damage,self._spawn['size']]

    @property
    def range(self):
        return self._spawn["shell_range"]