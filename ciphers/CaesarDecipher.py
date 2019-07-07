from ciphers.Dictionaries import trie_search

specialCase = ' 1234567890_=~!@#$%^&*()_+,./?:;"*-'

# LETTER BY LETTER WE SHIFT THE MESSAGE BY KEY WITH INCREMENTS OF 1
def shift(message, key):
    exitmessage = ""
    for letter in message:
        if letter in specialCase:
            exitmessage += ' ' + letter + ' '  # SEPARATE SPECIAL CHARACTERS BY A SPACE FOR DICTIONARY LOOKUP
        else:
            exitmessage += chr(ord(letter) + key)
    return exitmessage


# WE ARE TAKING ARRAY OF WORDS AND CHECK THEM ONE BY ONE IN THE DICTIONARY
def lookup(array, language):
    for index in range(len(array) - 1):
        if language == 'zh' or language == 'ar':
            if dictionarylookup(language, array[index]):    # CHINESE AND ARABIC USE 1 SYMBOL SO LENGTH OF THE WORD IS 1
                return True
        elif len(array[index]) > 3:
            if dictionarylookup(language, array[index]):    # USE DICTIONARY MODULE TO LOAD THE PROPER FILE
                return True
    return False

def decrypt(cipher, language):
    '''Takes a cipher, tries 26 shifts, and returns the answer containing the most dictionary words'''
    # Create a tuple representing the values: (number_of_dictionary_words_found, shift_key)
    matches = (0, 0)
    for key in range(-13,13,1):
        shifted = shift(cipher, key)
        words_found = trie_search(shifted, language)
        num_found = len(words_found)
        # If number of dictionary words is greater than the current greatest, update matches
        if num_found > matches[0]:
            matches = (num_found, key)
    # If none of the shifts yielded any dictionary words
    if matches[0] == 0 and matches[1] == 0:
        return 'Failed to decipher.'
    return shift(cipher, matches[1])


