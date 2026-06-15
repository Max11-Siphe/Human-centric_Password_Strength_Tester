import math
import string

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

        # print 
        print(lowercase_list, len(lowercase_list))
        print(uppercase_list, len(uppercase_list))

        # character booleans
        num_bool = False
        lowercase_bool = False
        uppercase_bool = False
        special_char_bool = False

        entropy = 0

        for char in password:
            if char in num_list:
                num_bool = True
            elif char in lowercase_bool:
                lowercase_bool = True
            elif char in uppercase_bool:
                uppercase_bool = True
            elif char in special_char_bool:
                special_char_bool = True

        

        if num_bool and alpha_bool and special_char_bool:
            entropy = len(password) * math.log2(len(num_list) + len(uppercase_list) + len(special_char_list))
        elif num_bool and alpha_bool:
            entropy = len(password) * math.log2(len(num_list) + len(uppercase_list))
        elif num_bool:
            entropy = len(password) * math.log2(len(num_list))
        elif alpha_bool and special_char_bool:
            entropy = len(password) * math.log2(len(special_char_list) + len(uppercase_list))
        elif alpha_bool:
            entropy = len(password) * math.log2(len(uppercase_list))
        
        if num_bool and alpha_bool and special_char_bool:
            entropy = len(password) * math.log2(len(num_list) + len(lowercase_list) + len(special_char_list))
        elif num_bool and alpha_bool:
            entropy = len(password) * math.log2(len(num_list) + len(lowercase_list))
        elif num_bool:
            entropy = len(password) * math.log2(len(num_list))
        elif alpha_bool and special_char_bool:
            entropy = len(password) * math.log2(len(special_char_list) + len(lowercase_list))
        elif alpha_bool:
            entropy = len(password) * math.log2(len(lowercase_list))

        elif special_char_bool and num_bool:
            entropy = len(password) * math.log2(len(special_char_list) + len(num_list))
        elif special_char_bool:
            entropy = len(password) * math.log2(len(special_char_list))

        return entropy

def main():
    print(character_checker("something"))


if __name__ == "__main__":
    main()