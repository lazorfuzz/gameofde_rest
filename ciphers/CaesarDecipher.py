from ciphers.Dictionaries import dictionarylookup

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
        if language == 'chinese' or language == 'arabic':
            if dictionarylookup(language, array[index]):    # CHINESE AND ARABIC USE 1 SYMBOL SO LENGTH OF THE WORD IS 1
                return true
        elif len(array[index]) > 3:
            if dictionarylookup(language, array[index]):    # USE DICTIONARY MODULE TO LOAD THE PROPER FILE
                return true
    return false


# MAIN FUNCTION THAT PUTS IT ALL TOGETHER
def decrypt(cipheredText, language):
    answer = ''
    answerKey = 0
    for key in range(-10,10,1):
        decipheredMessage = shift(cipheredText, key)  # SHIFT THE MESSAGE
        messageSplit = decipheredMessage.split()      # BREAK DOWN WORD BY WORD FOR DICTIONARY LOOKUP
        if lookup(messageSplit, language):                      # LOOK UP IN DICTIONARY
            answer = decipheredMessage
            answerKey = key
            break

    if len(answer) > 0:
        return 'After dictionary lookup, Caesar key is {} and message is: \n'.format(answerKey) + answer
    elif len(cipheredText) > 0:
        return 'That was not Caesar ciphering'
    else:
        return 'Make sure you gave me the message'


