import math
import string

# maximum number of bits (standardized)
BITS_TARGET_CEILING = 128

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

def entropy_percentage_calculator(entropy):
    return (entropy/BITS_TARGET_CEILING) * 100 

def character_checker(password):
        """ 
            Calculates how secure a password is (E = L * log2(R))
            E = entropy in bytes
            L = length of the password
            R = pool of characters
        """
        # character lists
        num_list = string.printable[:10]
        lowercase_list = string.printable[10:36]
        uppercase_list = string.printable[36:62]
        special_char_list = string.printable[62:-6]

        # character booleans
        num_bool = False
        lowercase_bool = False
        uppercase_bool = False
        special_char_bool = False

        entropy = 0

        for char in password:
            if char in num_list:
                num_bool = True
            elif char in lowercase_list:
                lowercase_bool = True
            elif char in uppercase_list:
                uppercase_bool = True
            elif char in special_char_list:
                special_char_bool = True

        pool_size = sum([
            len(num_list) if num_bool else 0,
            len(uppercase_list) if uppercase_bool else 0,
            len(lowercase_list) if lowercase_bool else 0,
            len(special_char_list) if special_char_bool else 0
        ])

        entropy = len(password) * math.log2(pool_size)

        return entropy
    
# Human Friction Metrics Functions
def diff_char_friction(password):
    pass

def ambiguous_char(password):
    pass

def leetspeak_reverse(password):
    pass

def main():
    print(character_checker("something"))


if __name__ == "__main__":
    main()