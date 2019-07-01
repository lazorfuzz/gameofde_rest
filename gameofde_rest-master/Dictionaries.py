# TOP 10 SPOKEN LANGUAGES IN US
readfile =""

def languageSelection(language):
    if language == "arabic":
        readfile = "Dictionary/Arabic.txt"
    elif language == "chinese":
        readfile = "Dictionary/Chinese.txt"
    elif language == "english":
        readfile = "Dictionary/English.txt"
    elif language == "french":
        readfile = "Dictionary/French.txt"
    elif language == "german":
        readfile = "Dictionary/German.txt"
    elif language == "italian":
        readfile = "Dictionary/Italian.txt"
    elif language == "korean":
        readfile = "Dictionary/Korean.txt"
    elif language == "russian":
        readfile = "Dictionary/Russian.txt"
    elif language == "spanish":
        readfile = "Dictionary/Spanish.txt"
    elif language == "tagalog":
        readfile = "Dictionary/Tagalog.txt"
    elif language == "vietnamese":
        readfile = "Dictionary/Vietnamese.txt"
    return readfile


def dictionarylookup(language, word):
    readfile = languageSelection(language)
    if readfile != "":
        file = open(readfile, encoding="utf-16")
        for line in file:
            if word.strip() == line.strip():
                return True
                break
    return False