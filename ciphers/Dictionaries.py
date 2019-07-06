# TOP 10 SPOKEN LANGUAGES IN US
readfile =""

lang_files = {
    'ar': 'Dictionary/Arabic.txt',
    'zh': 'Dictionary/Chinese.txt',
    'en': 'Dictionary/English.txt',
    'fr': 'Dictionary/French.txt',
    'de': 'Dictionary/German.txt',
    'it': 'Dictionary/Italian.txt',
    'ko': 'Dictionary/Korean.txt',
    'ru': 'Dictionary/Russian.txt',
    'es': 'Dictionary/Spanish.txt',
    'tl': 'Dictionary/Tagalog.txt',
    'vi': 'Dictionary/Vietnamese.txt'
}

def languageSelection(language):
    return lang_files.get(language)

def dictionarylookup(language, word):
    readfile = languageSelection(language)
    if readfile != "":
        with open(readfile, encoding="utf-16") as file:
            for line in file:
                if word.strip() == line.strip():
                    return True
                    break
    return False