from Dictionaries import LanguageTrie, trie_search, dictionarylookup
import time

class Color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def test(sentence, lang, iterations):
  '''Tests a dictionary lookup on a sentence using a trie search v.s. a line-by-line lookup.'''
  print(Color.BLUE + 'Testing sentence: %r' % sentence + Color.END)
  print('%sWord count:%s %d' % (Color.CYAN, Color.END, len(sentence.split())))
  print('%sTesting trie_search: %s %d iterations' % (Color.YELLOW, Color.END, iterations))
  start = time.time()
  for i in range(iterations):
      trie_search(sentence, lang)
  stop = time.time()
  print(Color.GREEN + '    Time elapsed:' + Color.END, stop - start, 'seconds')
  print('%sTesting dictionarylookup: %s %d iterations' % (Color.YELLOW, Color.END, iterations))
  start = time.time()
  for i in range(iterations):
      word_arr = sentence.split()
      for w in word_arr:
          dictionarylookup('en', w)
  stop = time.time()
  print(Color.GREEN + '    Time elapsed:' + Color.END, stop - start, 'seconds');
  print ('-' * 50)

if __name__ == '__main__':
  test('the quick brown fox jumps over the lazy red dog.', 'en', 100)
  test('the quick brown fox jumps over the lazy red dog. ' * 5, 'en', 100)