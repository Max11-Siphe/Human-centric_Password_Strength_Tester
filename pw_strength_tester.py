import math
import string
import itertools
import english_words

# character lists
NUM_LIST = string.printable[:10]
LOWERCASE_LIST = string.printable[10:36]
UPPERCASE_LIST = string.printable[36:62]
SPECIAL_CHAR_LIST = string.printable[62:-6]

# maximum number of bits (standardized)
BITS_TARGET_CEILING = 128

# maximum number of points (according to scoring system)
MAXIMUM_POSSIBLE_POINTS = 105

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
        entropy = 0

        bool_dict = character_checker(password)

        pool_size = sum([
            len(NUM_LIST) if bool_dict["num bool"] else 0,
            len(UPPERCASE_LIST) if bool_dict["uppercase bool"] else 0,
            len(LOWERCASE_LIST) if bool_dict["lowercase bool"] else 0,
            len(SPECIAL_CHAR_LIST) if bool_dict["special char bool"] else 0
        ])

        entropy = len(password) * math.log2(pool_size)

        # return entropy
        return str(min(100 ,round(entropy_percentage_calculator(entropy)))) + "%"

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
    
    return total_points
    # return str(round(points_percentage_calculator(total_points), 0)) + "%"
    

def leet_word_translator(password):
    password_copy = password
    for key, value in MULTI_CHAR_LEET.items():
        if key in password:
            password_copy.replace(key, value)
            
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
        
    all_combinations = itertools.product(*password_matrix)
    all_possible_words_set = {"".join(combo) for combo in all_combinations}
    
    return all_possible_words_set

def actual_words(word_set):
    final_words = []
    for word in word_set:
        if word in DICTIONARY:
            final_words.append(word)

    return final_words

def ambiguous_char(password):
    """
        This score is for if there are ambiguous letters in 1 password.
        if l and 1 in same password: 15 pts
    """
    pass

def leetspeak_reverse(password):
    """
        This is to check and score if the word with symbols is a real word
        or if it's random letters.
        0 pts: Dictionary words/passphrases
        20 pts: random characters with length < 10
        35 pts: random characters with 10 <= length <= 14
        50 pts: random characters with length > 14
    """
    pass

def main():
    pw = "p0e$K@ker"
    print(entropy(pw))
    print()
    pw_copy = leet_word_translator(pw)
    print(possible_words_creator(pw_copy))


if __name__ == "__main__":
    main()