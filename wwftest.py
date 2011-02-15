import wwf
import unittest

class KnownValues(unittest.TestCase):
    pointKnownValues = \
        (('abc',   9),
         ('boom',  10),
         ('great', 7),
         ('qi',    11),
         ('Qi',    1),
         ('QIs',   1),
         ('IS',    0))
                        
    permutationsKnownValues = \
        (('abc', len('abc'),
            [('a', 'b', 'c'), 
             ('a', 'c', 'b'), 
             ('b', 'a', 'c'), 
             ('b', 'c', 'a'), 
             ('c', 'a', 'b'), 
             ('c', 'b', 'a')]),
         ('wq', len('wq'),
            [('w', 'q'), 
             ('q', 'w')]),
         ('zz*', len('zz*'),
            [('z', 'z', '*'), 
             ('z', '*', 'z'), 
             ('z', 'z', '*'), 
             ('z', '*', 'z'), 
             ('*', 'z', 'z'), 
             ('*', 'z', 'z')]),
         ('asdf', len('asdf'),
            [('a', 's', 'd', 'f'),
             ('a', 's', 'f', 'd'),
             ('a', 'd', 's', 'f'),
             ('a', 'd', 'f', 's'),
             ('a', 'f', 's', 'd'),
             ('a', 'f', 'd', 's'),
             ('s', 'a', 'd', 'f'),
             ('s', 'a', 'f', 'd'),
             ('s', 'd', 'a', 'f'),
             ('s', 'd', 'f', 'a'),
             ('s', 'f', 'a', 'd'),
             ('s', 'f', 'd', 'a'),
             ('d', 'a', 's', 'f'),
             ('d', 'a', 'f', 's'),
             ('d', 's', 'a', 'f'),
             ('d', 's', 'f', 'a'),
             ('d', 'f', 'a', 's'),
             ('d', 'f', 's', 'a'),
             ('f', 'a', 's', 'd'),
             ('f', 'a', 'd', 's'),
             ('f', 's', 'a', 'd'),
             ('f', 's', 'd', 'a'),
             ('f', 'd', 'a', 's'),
             ('f', 'd', 's', 'a')]),
         ('asdf', 2,
            [('a', 's'),
             ('a', 'd'),
             ('a', 'f'),
             ('s', 'a'),
             ('s', 'd'),
             ('s', 'f'),
             ('d', 'a'),
             ('d', 's'),
             ('d', 'f'),
             ('f', 'a'),
             ('f', 's'),
             ('f', 'd')])
            )
        
    def testPointValueKnownValues(self):
        """point_value should give known result with known input"""
        for word, points in self.pointKnownValues:
            result = wwf.point_value(word)
            self.assertEqual(points, result)
    
    def testPermutationsKnownValues(self):
        """permutations should give known result with known input"""
        for word, r, perms in self.permutationsKnownValues:
            result = list(wwf.permutations(word, r))
            self.assertEqual(perms, result)

class PermutationsBadInput(unittest.TestCase):
    def testTooFewLetters(self):
        """permutations should fail with 1 letter input"""
        self.assertRaises(ValueError, wwf.permutations, "a")
    
    def testRTooSmall(self):
        """permutations should fail when r < 2 """
        self.assertRaises(ValueError, wwf.permutations, ("abc", 1))
        

if __name__ == '__main__':
    unittest.main()
                    