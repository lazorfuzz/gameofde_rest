# TOP 10 SPOKEN LANGUAGES IN US
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

lang_files = {
    'ar': {'file': 'Dictionary/Arabic.txt', 'encoding': 'utf-16'},
    'zh': {'file': 'Dictionary/Chinese.txt', 'encoding': 'utf-16'},
    'en': {'file': 'Dictionary/English.txt', 'encoding': 'utf-8'},
    'fr': {'file': 'Dictionary/French.txt', 'encoding': 'utf-8'},
    'de': {'file': 'Dictionary/German.txt', 'encoding': 'utf-8'},
    'it': {'file': 'Dictionary/Italian.txt', 'encoding': 'utf-8'},
    'ko': {'file': 'Dictionary/Korean.txt', 'encoding': 'utf-16'},
    'ru': {'file': 'Dictionary/Russian.txt', 'encoding': 'utf-16'},
    'es': {'file': 'Dictionary/Spanish.txt', 'encoding': 'utf-8'},
    'tl': {'file': 'Dictionary/Tagalog.txt', 'encoding': 'utf-8'},
    'vi': {'file': 'Dictionary/Vietnamese.txt', 'encoding': 'utf-16'}
}

def languageSelection(language):
    return lang_files.get(language)

def dictionarylookup(language, word):
    readfile = languageSelection(language)
    if readfile != "":
        with open(dir_path + '/' + readfile['file'], encoding=readfile['encoding']) as file:
            for line in file:
                if word.strip() == line.strip():
                    return True
                    break
    return False
