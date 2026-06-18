import math
import string

# character lists
NUM_LIST = string.printable[:10]
LOWERCASE_LIST = string.printable[10:36]
UPPERCASE_LIST = string.printable[36:62]
SPECIAL_CHAR_LIST = string.printable[62:-6]

# maximum number of bits (standardized)
BITS_TARGET_CEILING = 128

# maximum number of points (according to scoring system)
MAXIMUM_POSSIBLE_POINTS = 105

LEET_REVERSE_MAP = {
    # Punctuation requested
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
    '8': ['b', 'b'],
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
        return str(round(entropy_percentage_calculator(entropy), 0)) + "%"

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
    print(character_checker("something"))


if __name__ == "__main__":
    main()