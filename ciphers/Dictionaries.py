import os
import json
import time

dir_path = os.path.dirname(os.path.realpath(__file__))

class LanguageTrie:
    '''
    LanguageTrie(lang_code) --> searchable language trie

    A trie data structure that holds common vocabulary from different languages.

    Parameters:

    lang (str): The language this trie searches.
    preimport (bool): Import trie from JSON on initialization.
    '''

    trie = {}
    preimport = True
    
    def __init__(self, lang = 'en', preimport = True):
        '''The trie constructor.'''
        self.lang = lang
        self.preimport = preimport
        if preimport:
            self.import_trie(lang)

    def add_word(self, node, word, idx = 0):
        '''Recursively add a word to the trie data structure.'''
        children = node['chdn']
        # If no more letters to add
        if idx == len(word):
            return
        # If the current node's children contains the current letter, select the child node
        next_node = children.get(word[idx])
        if next_node:
            self.add_word(next_node, word, idx + 1)
        else:
            # The current node does not have a child node for the current letter
            is_leaf = idx == len(word) - 1
            # Create the new child node for the current letter
            children[word[idx]] = {'chdn': {}, '#': is_leaf}
            if not is_leaf:
                # If there are more letters to go, add the next letter
                self.add_word(children.get(word[idx]), word, idx + 1)

    def build_trie(self, lang):
        '''Builds a trie from a language frequency dictionary.'''
        # Create root node
        self.trie['root'] = {'chdn': {}}
        read_file = lang_files.get(lang)
        # Read words from file and add each word to the trie
        with open(dir_path + '/' + read_file['file']) as f:
                for line in f:
                    word = line.split()[0]
                    self.add_word(self.trie['root'], word)
        # Export the trie data structure to JSON
        with open(dir_path + '/Dictionary/Tries/' + lang + '.json', mode='w') as f:
            f.write(json.dumps(self.trie))
    
    def import_trie(self, lang):
        '''Initializes a trie from JSON.'''
        with open('%s/Dictionary/Tries/%s.json' % (dir_path, lang), 'r') as f:
            data = f.read()
        self.trie = json.loads(data)

    def search(self, word, idx = 0, node = None):
        '''Recursively searches for a word in the trie.'''
        if not self.trie.get('root'):
            # If the trie wasn't preimported, import it now
            self.import_trie(self.lang)
            self.search(word, idx, node)
        if idx == len(word):
            return False
        if not node:
            node = self.trie['root']
        children = node['chdn']
        # Check if the current node's children contains a node that holds the letter at word[idx]
        next_node = children.get(word[idx])
        if next_node:
            # Check if we're at the last letter and the next node is a leaf node
            if idx == len(word) - 1 and next_node['#']:
                return True
            # Search for next letter in the child node
            return self.search(word, idx + 1, next_node)
        else:
            return False

    def compile_all(self):
        '''Builds a trie for each language in lang_files.'''
        for lang in lang_files.keys():
            print(lang)
            self.build_trie(lang)


lang_files = {
    'ar': {'file': 'Dictionary/ar_50k.txt', 'trie': LanguageTrie('ar')},
    'en': {'file': 'Dictionary/en_50k.txt', 'trie': LanguageTrie('en')},
    'fr': {'file': 'Dictionary/fr_50k.txt', 'trie': LanguageTrie('fr', preimport=False)},
    'de': {'file': 'Dictionary/de_50k.txt', 'trie': LanguageTrie('de', preimport=False)},
    'it': {'file': 'Dictionary/it_50k.txt', 'trie': LanguageTrie('it', preimport=False)},
    'ru': {'file': 'Dictionary/ru_50k.txt', 'trie': LanguageTrie('ru')},
    'es': {'file': 'Dictionary/es_50k.txt', 'trie': LanguageTrie('es')}
}

def create_language_tries():
    LanguageTrie().compile_all()

def trie_search(sentence, lang):
    '''Returns a list of words in the sentence that were found in the trie.'''
    trie = lang_files.get(lang)['trie']
    word_array = sentence.lower().strip().split()
    return list(filter(lambda w: trie.search(w), word_array))

def languageSelection(language):
    return lang_files.get(language)

def dictionarylookup(language, word):
    readfile = languageSelection(language)
    if readfile != "":
        with open(dir_path + '/' + readfile['file']) as file:
            for line in file:
                if word.strip() == line.split()[0].strip():
                    return True
                    break
    return False
