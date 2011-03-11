import sys
import operator
import string
import re
import itertools

WORD_LIST_FILE = "enable1.txt"
ALPHABET = string.ascii_uppercase
LETTER_VALUES = {
    "a": 1,  "b": 4, "c": 4, "d": 2, "e": 1, "f": 4, "g": 3, "h": 3, "i": 1, 
    "j": 10, "k": 5, "l": 2, "m": 4, "n": 2, "o": 1, "p": 4, "q": 10, 
    "r": 1,  "s": 1, "t": 1, "u": 2, "v": 5, "w": 4, "x": 8, "y": 3, "z": 10, "*": 0
}

def flatten(listOfLists):
    return itertools.chain.from_iterable(listOfLists)
    
def permutations(letters, r=None):
    if len(letters) == 1:
        raise ValueError("Can't find permutations of a single letter.")
    
    return itertools.permutations(letters, r)

def point_value(word):
    return sum(LETTER_VALUES[letter] for letter in word if letter not in ALPHABET)
    
def create_word_list(f):
    with open(f, "r") as word_file:
        word_list = set(tuple(word.rstrip()) for word in word_file)
            
    return word_list

def compute_racks(rack_string):
    racks = [rack_string]
    for rack in racks:
        for index, tile in enumerate(rack):
            if tile == '*':
                for letter in ALPHABET:
                    racks += [rack[:index] + letter + rack[index+1:]]
    
    return set(rack for rack in racks if '*' not in rack)

def lowercase(iterable):
    return tuple(s.lower() for s in iterable)
    
def get_all_perms(rack):
    return flatten(permutations(rack, span) for span in xrange(2, len(rack) + 1))

def get_perms(racks):
    return flatten(get_all_perms(rack) for rack in racks)

def get_candidates(perms):
    return dict((''.join(perm), point_value(perm)) for perm in perms if lowercase(perm) in word_list)

def compute_candidates(racks):
    perms = get_perms(racks)
    return get_candidates(perms)
    
def sort_candidates(candidates):
    candidates = dict([(word, value) for (word, value) in candidates.items() if re.match(constraints, word)])
    return sorted([(v, k) for (k, v) in candidates.items()], reverse=True)

def grep(regex, list):
    compiled_regex = re.compile(regex)
    return itertools.filter(compiled_regex.search, list)

if __name__ == '__main__':

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
        raise ValueError("You can have a maximum of two blank tiles.")
    
    racks = compute_racks(rack_string)
    candidates = compute_candidates(racks)
    sorted_candidates = sort_candidates(candidates)
    
    if sorted_candidates:
        print "\nPoints\tWord\tLength"    
        for (points, word) in sorted_candidates:
            print points, "\t", word, "\t", len(word)
        print len(sorted_candidates), "words"
    else:
        print "\nNo words found."
        