from ciphers.Dictionaries import trie_search, lang_files

special_case = ' 1234567890_=~!@#$%^&*()_+,./?:;"*-\n'

def shift(text, s, lang = 'en'): 
    """Shifts a sentence by int s
    
    Arguments:
        text {str} -- The string to be shifted
        s {int} -- The number of shifts
    
    Keyword Arguments:
        lang {str} -- Two-letter language code (default: {'en'})
    
    Returns:
        str -- The shifted sentence
    """
    result = ''
    # traverse text 
    for i in range(len(text)): 
        char = text[i]
        if char in special_case:
            result += char
        elif (char.isupper()): 
            if lang == 'en': result += chr((ord(char) + s-65) % 26 + 65)
            else: result += chr(abs(ord(char) + s))
        else: 
            if lang == 'en': result += chr((ord(char) + s - 97) % 26 + 97) 
            else: result += chr(abs(ord(char) + s))
    return result

# WE ARE TAKING ARRAY OF WORDS AND CHECK THEM ONE BY ONE IN THE DICTIONARY
def lookup(array, language):
    """NO LONGER USED - Take each word and check them line by line in the dictionary
    
    Arguments:
        array {list} -- List of words
        language {str} -- Two-letter language code
    
    Returns:
        bool -- Whether the sentence appeared in the dictionary
    """
    for index in range(len(array) - 1):
        if language == 'zh' or language == 'ar':
            if dictionarylookup(language, array[index]):    # CHINESE AND ARABIC USE 1 SYMBOL SO LENGTH OF THE WORD IS 1
                return True
        elif len(array[index]) > 3:
            if dictionarylookup(language, array[index]):    # USE DICTIONARY MODULE TO LOAD THE PROPER FILE
                return True
    return False



def decrypt(cipher, language = 'idk'):
    """Takes a cipher, tries 26 shifts, and returns
    the answer containing the most dictionary words and the associated lang code
    for that dictionary.
    
    Arguments:
        cipher {str} -- The cipher to decrypt
    
    Keyword Arguments:
        language {str} -- Two-letter language code (default: {'idk'})
    
    Returns:
        (str, str) -- A tuple containing the shifted sentence and the two-letter language code
    """
    # Create a tuple with intended values: (number_of_dictionary_words_found, shift_key, lang)
    best_match = (0, 0, 'en')
    # Get a list of lang codes from preimported tries
    preimported_langs = list(filter(lambda l: lang_files.get(l)['trie'].preimport == True, lang_files.keys()))
    # By default, language will be 'idk'. If not, search only in that langauge
    if not language == 'idk':
        preimported_langs = [language]
    for lang in preimported_langs:
        for key in range(-13,13,1):
            shifted = shift(cipher, key, lang)
            words_found = trie_search(shifted, lang)
            num_found = len(words_found)
            # If number of dictionary words is greater than the current greatest, update matches
            if num_found > best_match[0]:
                best_match = (num_found, key, lang)
    # If none of the shifts yielded any dictionary words, return fail
    if best_match[0] == 0 and best_match[1] == 0:
        return 'Failed to decipher.', 'idk'
    # Return deciphered_text, lang_code
    return shift(cipher, best_match[1], best_match[2]), best_match[2]
