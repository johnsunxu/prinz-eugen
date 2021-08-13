import sys
sys.path.append('../src')

#Import the module
from perseus import Perseus
api = Perseus()

s = api.Ship("Nagato")
print(s.skins)