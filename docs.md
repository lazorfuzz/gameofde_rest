# controllers.mainControllers

## generate_token
```python
generate_token(user)
```
Generates a JWT-like auth token

Arguments:
    user {User} -- A SequelAlchemy user object

Returns:
    str -- The token

## read_token
```python
read_token(token)
```
Validates the token payload with the signature, and returns
a dict containing the user data in the payload

Arguments:
    token {str} -- The token passed in the HTTP header

Returns:
    dict -- The decoded user data

## this_user
```python
this_user()
```
Gets the current user's info from token

Returns:
    dict -- The user's data

## authenticate
```python
authenticate(func)
```
A decorator method that checks that the user's auth token is valid

Arguments:
    func {func} -- The target method

Returns:
    func -- The target method

## CaesarController
```python
CaesarController(self, /, *args, **kwargs)
```

### method_decorators
Built-in mutable sequence.

If no argument is given, the constructor creates a new empty list.
The argument must be an iterable if specified.
### methods
set() -> new empty set object
set(iterable) -> new set object

Build an unordered collection of unique elements.
### post
```python
CaesarController.post(self)
```
The POST handler for the /caesar endpoint

Returns:
    dict -- A dict containing the result and the detected language

## NoAuthCaesarController
```python
NoAuthCaesarController(self, /, *args, **kwargs)
```

### methods
set() -> new empty set object
set(iterable) -> new set object

Build an unordered collection of unique elements.
### post
```python
NoAuthCaesarController.post(self)
```
The POST handler for the /test_caesar endpoint

Arguments:
    Resource {Resource} -- The Flask Resource

Returns:
    dict -- A dict containing the result and detected language

## OrganizationController
```python
OrganizationController(self, /, *args, **kwargs)
```

### method_decorators
Built-in mutable sequence.

If no argument is given, the constructor creates a new empty list.
The argument must be an iterable if specified.
### methods
set() -> new empty set object
set(iterable) -> new set object

Build an unordered collection of unique elements.
### get
```python
OrganizationController.get(self, org_name)
```
The GET handler for /orgs/<org_id> endpoint

Arguments:
    org_name {str} -- The organization's name

Returns:
    dict -- Information about the organization and its list of users

### post
```python
OrganizationController.post(self, org_name)
```
The POST handler for the /orgs/<org_name> endpoint

Arguments:
    org_name {str} -- The organization's name

Returns:
    dict -- A status message

### put
```python
OrganizationController.put(self, org_name)
```
The PUT handler for /orgs/<org_name> endpoint

Arguments:
    org_name {str} -- The organization's name

Returns:
    dict -- Information about the edited organization

## OrganizationList
```python
OrganizationList(self, /, *args, **kwargs)
```

### methods
set() -> new empty set object
set(iterable) -> new set object

Build an unordered collection of unique elements.
### get
```python
OrganizationList.get(self)
```
The GET handler for the /orgs endpoint

Returns:
    list -- List of organizations

## NewsController
```python
NewsController(self, /, *args, **kwargs)
```

### methods
set() -> new empty set object
set(iterable) -> new set object

Build an unordered collection of unique elements.
### get
```python
NewsController.get(self, org_name)
```
The GET handler for the /news endpoint

Arguments:
    org_name {str} -- The organization's name

Returns:
    list -- List of news items for the organization

## CheckSolutionController
```python
CheckSolutionController(self, /, *args, **kwargs)
```

### method_decorators
Built-in mutable sequence.

If no argument is given, the constructor creates a new empty list.
The argument must be an iterable if specified.
### methods
set() -> new empty set object
set(iterable) -> new set object

Build an unordered collection of unique elements.
### post
```python
CheckSolutionController.post(self)
```
The POST handler for the /solutions endpoint

Returns:
    dict -- Data about an existing solution

## SavedSolutionsController
```python
SavedSolutionsController(self, /, *args, **kwargs)
```

### method_decorators
Built-in mutable sequence.

If no argument is given, the constructor creates a new empty list.
The argument must be an iterable if specified.
### methods
set() -> new empty set object
set(iterable) -> new set object

Build an unordered collection of unique elements.
### get
```python
SavedSolutionsController.get(self)
```
The GET handler for the /saved_solutions endpoint

Returns:
    list -- List of saved solutions for the requesting user

### post
```python
SavedSolutionsController.post(self)
```
The POST handler for the /saved_solutions endpoint

Returns:
    dict -- Status message

## SavedSolutionController
```python
SavedSolutionController(self, /, *args, **kwargs)
```

### method_decorators
Built-in mutable sequence.

If no argument is given, the constructor creates a new empty list.
The argument must be an iterable if specified.
### methods
set() -> new empty set object
set(iterable) -> new set object

Build an unordered collection of unique elements.
### get
```python
SavedSolutionController.get(self, solution_id)
```
The GET handler for the /saved_solutions/<solution_id> endpoint

Arguments:
    solution_id {int} -- The solution's id

Returns:
    dict -- Object containing the solution data

### delete
```python
SavedSolutionController.delete(self, solution_id)
```
The DELETE handler for the /saved_solutions/<solution_id> endpoint

Arguments:
    solution_id {int} -- The solution's id

Returns:
    dict -- Status message

# controllers.userController

## LoginController
```python
LoginController(self, /, *args, **kwargs)
```

### methods
set() -> new empty set object
set(iterable) -> new set object

Build an unordered collection of unique elements.
### post
```python
LoginController.post(self)
```
The POST handler for the /login endpoint

Returns:
    dict -- Object containing the token and user details

## CreateAccountController
```python
CreateAccountController(self, /, *args, **kwargs)
```

### methods
set() -> new empty set object
set(iterable) -> new set object

Build an unordered collection of unique elements.
### post
```python
CreateAccountController.post(self)
```
The POST handler for the /create_account endpoint

Returns:
    dict -- Status message

## UserList
```python
UserList(self, /, *args, **kwargs)
```

### method_decorators
Built-in mutable sequence.

If no argument is given, the constructor creates a new empty list.
The argument must be an iterable if specified.
### methods
set() -> new empty set object
set(iterable) -> new set object

Build an unordered collection of unique elements.
### get
```python
UserList.get(self)
```
The GET hanlder for the /users endpoint

Returns:
    list -- List of users

## UserController
```python
UserController(self, /, *args, **kwargs)
```

### method_decorators
Built-in mutable sequence.

If no argument is given, the constructor creates a new empty list.
The argument must be an iterable if specified.
### methods
set() -> new empty set object
set(iterable) -> new set object

Build an unordered collection of unique elements.
### get
```python
UserController.get(self, user_id)
```
The GET handler for the /users/<user_id> endpoint

Arguments:
    user_id {int} -- The user's id

Returns:
    dict -- Data about the user

### put
```python
UserController.put(self, user_id)
```
The PUT handler for the /users/<user_id> endpoint

Arguments:
    user_id {int} -- The user's id

Returns:
    dict -- Data about the modified user

### delete
```python
UserController.delete(self, user_id)
```
The DELETE handler for the /users/<user_id> endpoint

Arguments:
    user_id {int} -- The user's id

Returns:
    dict -- Status message

# ciphers.Dictionaries

## LanguageTrie
```python
LanguageTrie(self, lang='en', preimport=True)
```
A trie data struture that holds common vocabulary from different languages.

Returns:
    LanguageTrie -- An instance of the LanguageTrie class

### preimport
bool(x) -> bool

Returns True when the argument x is true, False otherwise.
The builtins True and False are the only two instances of the class bool.
The class bool is a subclass of the class int, and cannot be subclassed.
### trie
dict() -> new empty dictionary
dict(mapping) -> new dictionary initialized from a mapping object's
    (key, value) pairs
dict(iterable) -> new dictionary initialized as if via:
    d = {}
    for k, v in iterable:
        d[k] = v
dict(**kwargs) -> new dictionary initialized with the name=value pairs
    in the keyword argument list.  For example:  dict(one=1, two=2)
### add_word
```python
LanguageTrie.add_word(self, node, word, idx=0)
```
Adds a word to the trie

Arguments:
    node {dict} -- The current node to examine
    word {str} -- The word being added

Keyword Arguments:
    idx {int} -- The character index of the word (default: {0})

### build_trie
```python
LanguageTrie.build_trie(self, lang)
```
Builds a trie from a language frequency dictionary

Arguments:
    lang {str} -- The two-letter language code

### import_trie
```python
LanguageTrie.import_trie(self, lang)
```
Initializes a trie from JSON

Arguments:
    lang {str} -- The two-letter language code

### search
```python
LanguageTrie.search(self, word, idx=0, node=None)
```
Searches for a word in the trie

Arguments:
    word {str} -- A word

Keyword Arguments:
    idx {int} -- The character index of the word (default: {0})
    node {dict} -- The current node to examine (default: {None})

Returns:
    bool -- Whether the word was found in the dictionary

### compile_all
```python
LanguageTrie.compile_all(self)
```
Builds a JSON file for each langauge in lang_files

## trie_search
```python
trie_search(sentence, lang)
```
Get a list of dictionary words from the sentence

Arguments:
    sentence {str} -- The sentence to look up
    lang {str} -- Two-letter language code

Returns:
    list -- List of dictionary words found in the sentence.

# ciphers.CaesarDecipher

## shift
```python
shift(text, s, lang='en')
```
Shifts a sentence by int s

Arguments:
    text {str} -- The string to be shifted
    s {int} -- The number of shifts

Keyword Arguments:
    lang {str} -- Two-letter language code (default: {'en'})

Returns:
    str -- The shifted sentence

## lookup
```python
lookup(array, language)
```
NO LONGER USED - Take each word and check them line by line in the dictionary

Arguments:
    array {list} -- List of words
    language {str} -- Two-letter language code

Returns:
    bool -- Whether the sentence appeared in the dictionary

## decrypt
```python
decrypt(cipher, language='idk')
```
Takes a cipher, tries 26 shifts, and returns
the answer containing the most dictionary words and the associated lang code
for that dictionary.

Arguments:
    cipher {str} -- The cipher to decrypt

Keyword Arguments:
    language {str} -- Two-letter language code (default: {'idk'})

Returns:
    (str, str) -- A tuple containing the shifted sentence and the two-letter language code

