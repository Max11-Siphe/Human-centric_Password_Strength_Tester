import math
import re
import string
import itertools
import geonamescache
import english_words
import calendar
from names_dataset import NameDataset

# This is the Dataset for Most of the Names in the World
nd = NameDataset()

# Initialize the offline geography cache
gc = geonamescache.GeonamesCache()

print("Loading offline geographic database...")
GLOBAL_PLACES = set()

# Load cities (with a population over 15,000 to keep lookups fast)
for city_id, city_info in gc.get_cities().items():
    GLOBAL_PLACES.add(city_info['name'].lower())
    
# Load country names
for country_code, country_info in gc.get_countries().items():
    GLOBAL_PLACES.add(country_info['name'].lower())
    
print("Database loaded successfully.")

# Get all standard calendar values
MONTHS = [calendar.month_name[i].lower() for i in range(1, 13)]
SHORT_MONTHS = [calendar.month_abbr[i].lower() for i in range(1, 13)]

# character lists
NUM_LIST = string.printable[:10]
LOWERCASE_LIST = string.printable[10:36]
UPPERCASE_LIST = string.printable[36:62]
SPECIAL_CHAR_LIST = string.printable[62:-6]

# maximum number of bits (standardized)
BITS_TARGET_CEILING = 128

# maximum number of points (according to scoring system)
MAXIMUM_POSSIBLE_POINTS = 105

# Dictionary entropy cap
DICTIONARY_MATCH_ENTROPY_CAP = 20

# english dictionary
DICTIONARY = english_words.get_english_words_set(['web2'], lower=True)

# multiple symbols represent 1 character
MULTI_CHAR_LEET = {
    "|\\/|": "m",
    "\\/": "v",
    "\\/\\/": "w",
    "|/|": "n",
    "(_)": "u",
    "|*|": "h",
}

LEET_REVERSE_MAP = {
    # Punctuations
    '.': ['i', 'l', 'e'],
    ',': ['g', 'c', 'j'],
    '-': [' '],
    
    # Common Symbols & Numbers
    '@': ['a', 'o', 'at'],
    '!': ['i', 'l', '1'],
    '1': ['i', 'l', 't'],
    '3': ['e'],
    '4': ['a', 'h'],
    '0': ['o'],
    '5': ['s', 'z'],
    '7': ['t', 'l'],
    '$': ['s'],
    '#': ['h'],
    '8': ['b'],
    '9': ['g', 'p'],
    '2': ['z', 'r'],
    '+': ['t'],
    '^': ['a'],
    '(': ['c'],
    '[': ['c'],
    '<': ['c', 'k'],
    '%': ['x'],
    '&': ['and', 'g'],
    '*': ['a', 'x']
}

# safety cap on the leet-reversal search space
MAX_LEET_COMBINATIONS = 50_000

LETTER_TO_DIGIT_MAP = {
    'o': ['0'],
    'i': ['1'],
    'l': ['1'],
    'z': ['2'],
    'e': ['3'],
    'a': ['4'],
    's': ['5'],
    'g': ['6', '9'],
    'b': ['6', '8'],
    't': ['7'],
    'q': ['9'],
}

# safety cap for the number of possibilities for calendar values
MAX_NUMERIC_COMBINATIONS = 5_000

# possible char pool for all days, months and years (entropy cap)
DATE_MATCH_ENTROPY_CAP = 16

def character_checker(password):
    # character booleans
    num_bool = False
    lowercase_bool = False
    uppercase_bool = False
    special_char_bool = False
    
    for char in password:
        if char in NUM_LIST:
            num_bool = True
        elif char in LOWERCASE_LIST:
            lowercase_bool = True
        elif char in UPPERCASE_LIST:
            uppercase_bool = True
        elif char in SPECIAL_CHAR_LIST:
            special_char_bool = True
            
    return {"num bool": num_bool, "lowercase bool": lowercase_bool, "uppercase bool": uppercase_bool, "special char bool": special_char_bool}

def entropy_percentage_calculator(entropy):
    return (entropy/BITS_TARGET_CEILING) * 100 

def entropy(password):
        """ 
            Calculates how secure a password is (E = L * log2(R))
            E = entropy in bytes
            L = length of the password
            R = pool of characters
        """
        if len(password) == 0:
            return "0%"

        bool_dict = character_checker(password)

        pool_size = sum([
            len(NUM_LIST) if bool_dict["num bool"] else 0,
            len(UPPERCASE_LIST) if bool_dict["uppercase bool"] else 0,
            len(LOWERCASE_LIST) if bool_dict["lowercase bool"] else 0,
            len(SPECIAL_CHAR_LIST) if bool_dict["special char bool"] else 0
        ])
        
        if pool_size == 0:
            return "0%"

        raw_entropy = len(password) * math.log2(pool_size)

        if is_dictionary_match(password):
            raw_entropy = min(raw_entropy, DICTIONARY_MATCH_ENTROPY_CAP)
        
        if is_date_pattern(password):
            raw_entropy = min(raw_entropy, DATE_MATCH_ENTROPY_CAP)
        
        # return entropy
        return str(min(100 ,round(entropy_percentage_calculator(raw_entropy)))) + "%"

def points_percentage_calculator(total_points):
    return (total_points/MAXIMUM_POSSIBLE_POINTS) * 100
        
# Human Friction Metrics Functions
def diff_char_friction(password):
    """ 
        This scores the different characters found in the password.
        0 pts: lowercase 
        15 pts: lower + uppercase
        20 pts: lower + uppercase + numbers
        40 pts: lower + uppercase + numbers + symbols
    """
    total_points = 0
    
    bool_dict = character_checker(password)
    
    if bool_dict["lowercase bool"]:
        pass
    if bool_dict["uppercase bool"]:
        total_points += 15
    if bool_dict["num bool"]:
        total_points += 5
    if bool_dict["special char bool"]:
        total_points += 20
        
    total_points += ambiguous_char(password)
    total_points += leetspeak_reverse(password)
    
    # return total_points
    return str(round(points_percentage_calculator(total_points))) + "%"

def leet_word_translator(password):
    password_copy = password
    for key, value in MULTI_CHAR_LEET.items():
        if key in password:
            password_copy = password_copy.replace(key, value)
            
    return password_copy

def possible_words_creator(copy_of_password):
    copy_of_password = copy_of_password.lower()
    password_matrix = []
    
    for char in copy_of_password:
        if char in LEET_REVERSE_MAP:
            options = [char] + LEET_REVERSE_MAP[char]
        else:
            options = [char]
        password_matrix.append(options)
        
    total_combinations = 1
    for options in password_matrix:
        total_combinations *= len(options)
        if total_combinations > MAX_LEET_COMBINATIONS:
            best_guess = "".join(
                opts[1] if len(opts) > 1 else opts[0]
                for opts in password_matrix
            )
            return {copy_of_password, best_guess}
        
    all_combinations = itertools.product(*password_matrix)
    all_possible_words_set = {"".join(combo) for combo in all_combinations}
    
    return all_possible_words_set

def substring_finder(clean_password):
    new_word = ''.join([x for x in clean_password if x.isalpha() or x == " "])
    new_list = []
    
    if new_word in DICTIONARY or new_word in nd.first_names.keys() or new_word in nd.last_names.keys() or new_word in GLOBAL_PLACES or new_word in MONTHS or new_word in SHORT_MONTHS:
        new_list.append(new_word)
        
    return True if len(new_list) != 0 else False

def actual_words(word_set):
    final_words = []
    for word in word_set:
        name = substring_finder(word)
        if word in DICTIONARY or word in GLOBAL_PLACES or name or word in MONTHS or word in SHORT_MONTHS:
            final_words.append(word)

    return final_words

def get_dictionary_matches(password):
    """
        checks whether the password, once run through
        the leet-reversal candidate generator, matches a real dictionary
        word, name, place, or calendar term.
    """
    candidates = possible_words_creator(password)
    return actual_words(candidates)

def is_dictionary_match(password):
    """ 
        Returns the length of the possible options in the distionary greater than 0
    """
    return len(get_dictionary_matches(password)) > 0

def numeric_candidates(token):
    """ 
        given a token (already split on whitespace/separators), tries
        to read it as a number, treating digits literally and
        digit-lookalike letters via LETTER_TO_DIGIT_MAP (e.g. "z0z6" ->
        "2026")
    """
    token = token.lower()
    matrix = []
    for char in token:
        if char.isdigit():
            matrix.append([char])
        elif char in LETTER_TO_DIGIT_MAP:
            matrix.append(LETTER_TO_DIGIT_MAP[char])
        else:
            return set()
        
    total_combinations = 1
    for options in matrix:
        total_combinations *= len(options)
        if total_combinations > MAX_NUMERIC_COMBINATIONS:
            return {"".join(opts[0] for opts in matrix)}
        
    return {"".join(combo) for combo in itertools.product(*matrix)}

def decode_month_candidates(token):
    """ 
        reuses the existing symbol->letter leet reversal to check if a
        token decodes to a month name, e.g. "$3p7Em8e2" -> "september".
    """
    candidates = possible_words_creator(token)
    return {c for c in candidates if c in MONTHS or c in SHORT_MONTHS}

def is_vaild_day(numeric_string):
    return numeric_string.isdigit() and 1 <= int(numeric_string) <= 31

def is_valid_year(numeric_string):
    return numeric_string.isdigit() and 1900 <= int(numeric_string) <= 2099

def is_date_pattern(password):
    """ 
        detects day + month + year patterns even when disguised with
        leetspeak in either direction, e.g. "11 $3p7Em8e2 z0z6" ->
        11 September 2026.
    """
    tokens = [t for t in re.split(r'[\s\-_/\.]+', password.strip()) if t]
    
    found_day = False
    found_month = False
    found_year = False
    
    for token in tokens:
        numeric_versions = numeric_candidates(token)
        if any(is_vaild_day(n) for n in numeric_versions):
            found_day = True
        if any(is_valid_year(n) for n in numeric_versions):
            found_year = True
        if decode_month_candidates(token):
            found_month = True
            
    return found_day and found_month and found_year

def ambiguous_char(password):
    """
        This score is for if there are ambiguous letters in 1 password.
        if l and 1 in same password: 15 pts
    """
    
    for char in password:
        for key, value in LEET_REVERSE_MAP.items():
            if char == key:
                for x in value:
                    if x != char and x in password:
                        return 15
                    
    return 0

def leetspeak_reverse(password):
    """
        This is to check and score if the word with symbols is a real word
        or if it's random letters.
        0 pts: Dictionary words/passphrases
        20 pts: random characters with length < 10
        35 pts: random characters with 10 <= length <= 14
        50 pts: random characters with length > 14
    """
    eng_word_list = actual_words(possible_words_creator(password))
    if password in eng_word_list:
        return 0
    elif len(password) < 10:
        return 20
    elif 10 <= len(password) <= 14:
        return 35
    else:
        return 50

def main():
    pw = "11 $3p7Em8e2 z0z6"
    print("Entropy:", entropy(pw))
    print()
    pw_copy = leet_word_translator(pw)
    # print(possible_words_creator(pw_copy))
    # print()
    print(actual_words(possible_words_creator(pw_copy)))
    print()
    print("Human-centric:", diff_char_friction(pw))
    

if __name__ == "__main__":
    main()