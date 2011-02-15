import sys
import operator
import string
import re
from itertools import permutations, chain
        
class memoized(object):
   def __init__(self, func):
      self.func = func
      self.cache = {}
   def __call__(self, *args):
      try:
         return self.cache[args]
      except KeyError:
         value = self.func(*args)
         self.cache[args] = value
         return value
      except TypeError:
         return self.func(*args)
   def __repr__(self):
      return self.func.__doc__
   def __get__(self, obj, objtype):
      return functools.partial(self.__call__, obj)

def flatten(listOfLists):
    return chain.from_iterable(listOfLists)

@memoized
def point_value(word):
    word = word.translate(None, ALPHABET)
    return sum(LETTER_VALUES[letter] for letter in word)

@memoized
def my_permutations(letters, r):
    return permutations(letters, r)
    
def create_word_list(f):
    word_file = open(f, "r")
    word_list = set(word.rstrip() for word in word_file)
    word_file.close()
    
    return word_list

def compute_possible_racks(rack_string):
    racks = [rack_string]
    for rack in racks:
        for index, tile in enumerate(rack):
            if tile == '*':
                for letter in ALPHABET:
                    racks += [rack[:index] + letter + rack[index+1:]]
    
    racks = set(rack for rack in racks if '*' not in rack)
    
    return racks

def exists(word):
    return word.lower() in word_list

def get_perms(racks):
    return set(flatten(my_permutations(rack, span) for rack in racks for span in xrange(2, len(rack) + 1)))

def get_candidates(perms):
    candidates = {}
    for perm in perms:
        this_perm = ''.join(perm)
        if exists(this_perm):
            candidates[this_perm] = point_value(this_perm)
    return candidates

def compute_candidates(racks):
    perms = get_perms(racks)
    candidates = get_candidates(perms)
    
    return candidates    

    
def sort_candidates(candidates):
    candidates = dict([(word, value) for (word, value) in candidates.items() if re.match(constraints, word)])
    sorted_candidates = sorted([(v, k) for (k, v) in candidates.items()], reverse=True)
    
    return sorted_candidates

if __name__ == '__main__':
    
    WORD_LIST_FILE = "enable1.txt"
    ALPHABET = string.ascii_uppercase
    LETTER_VALUES = {
        "a": 1,  "b": 4, "c": 4, "d": 2, "e": 1, "f": 4, "g": 3, "h": 3, "i": 1, 
        "j": 10, "k": 5, "l": 2, "m": 4, "n": 2, "o": 1, "p": 4, "q": 10, 
        "r": 1,  "s": 1, "t": 1, "u": 2, "v": 5, "w": 4, "x": 8, "y": 3, "z": 10, "*": 0
    }
    
    try:
        rack_string = sys.argv[1]
    except IndexError:
        print "You need to supply some letters."
        sys.exit(1)
        
    try:
        constraints = "^" + sys.argv[2] + "$"
    except IndexError: 
        constraints = "^.*$"
    
    word_list = create_word_list(WORD_LIST_FILE)
    rack_string += constraints.translate(None, string.punctuation)  
    
    if rack_string.count('*') > 2:
        raise ValueError("You can only have a maximum of two blank rack_strings.")
    
    possible_racks = compute_possible_racks(rack_string)
    candidates = compute_candidates(possible_racks)
    sorted_candidates = sort_candidates(candidates)
    
    if sorted_candidates:
        print "\nPoints\tWord\tLength"    
        for (points, word) in sorted_candidates:
            pass
            #print points, "\t", word, "\t", len(word)
        print len(sorted_candidates), "words"
    else:
        print "\nNo words found."
        