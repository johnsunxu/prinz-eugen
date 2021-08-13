import unittest
import sys
sys.path.append('../src')
from perseus import Perseus

class TestPerseus(unittest.TestCase):
    def test_arguments(self):
        api = Perseus()
        api.initiate()
        s = api.Ship("Helena",
        level=80,
        limit_break=3,
        affinity=125,
        oathed=True,
        retrofit=False)

        self.assertEqual(s.level,80)
        self.assertEqual(s.limit_break,3)
        self.assertEqual(s.affinity,125)
        self.assertTrue(s.oathed)
        self.assertFalse(s.retrofit)


    def test_retrofit(self):
        api = Perseus()
        api.initiate()
        s = api.Ship("Helena")              #Check ship with retrofit ID
        self.assertTrue(s.retrofit)
        s = api.Ship("Jintsuu")             #Check ship without retrofit ID
        self.assertTrue(s.retrofit)
        s = api.Ship("Jintsuu",retrofit=False)             #Check a retrofit ship with the retrofit param turned off
        self.assertFalse(s.retrofit)
        s = api.Ship(10228)                 #Check if retrofit ID is converted to non-retrofit ID
        self.assertTrue(s.id,10205)
        s = api.Ship("Nagato")              #Check that ship without a retrofit does not have a retrofit
        self.assertFalse(s.retrofit)

    def test_stats(self):
        api = Perseus()
        api.initiate()
        s = api.Ship("Nagato")              #Check regular ship without retrofit. Stats have been verified with the Azur Lane Wiki.
        self.assertTrue(s.stats,{'hp': 8117, 'fp': 419, 'trp': 0, 'aa': 182, 'avi': 0, 'rld': 146, 'acc': 70, 'eva': 37, 'spd': 25, 'luk': 71, 'asw': 0, 'oil' : 15})
        s = api.Ship("Nagato",limit_break=2)        #Check oil cost for a BB at limit break 2.
        self.assertTrue(s.stats['oil'],13)
        self.assertTrue(s._limit_break,3)       #limit_break stat should be one less than _limit_break
        self.assertTrue(s.limit_break,2)




if __name__ == '__main__':
    unittest.main()
