import nltk
grammar = nltk.CFG.fromstring("""
  S  -> NP VP
  NP -> PN | Det N | N
  VP -> IV | IV Adv | AV Adj | TV PN NP | V NP
  IV -> 'runs' | 'run' | 'running' | 'loves' | 'loved' | 'loving' | 'walks' | 'walk' | 'walking' | 'jumps' | 'jump' | 'jumping' | 'shoots' | 'shoot' | 'shooting'
  AV -> 'is' | 'are' | 'does' | 'do' 
  TV -> 'plays' | 'play' | 'played' | 'playing'
  PN -> 'kate' | 'james' | 'tomas' 
  Adv -> 'quickly' | 'slowly' | 'independently'
  Det -> 'the' | 'a' | 'an'
  N -> 'food' | 'cat' | 'dog' | 'dogs' | 'cat' | 'cats' | 'book' | 'books' | 'sport' | 'sports' | 'daddy' | 'daddies' | 'boy' | 'boys' | 'girls' | 'girl' | 'basketball' | 'basketballs'
  Adj  -> 'scary' | 'tall' |  'short' | 'blonde' | 'slim' | 'fat'
  V ->  'chased'  | 'chase' | 'needs' | 'hates' | 'hate' | 'has' | 'has' | 'have' | 'loves' | 'love' | 'kicks' | 'kick' | 'jumps' | 'jump'
  """)
sentence = "kate played john a sport"
sent = sentence.split()
read_parser = nltk.RecursiveDescentParser(grammar)
print("Parsing  the sentence:"+ " " + sentence)
for tree in read_parser.parse(sent):
    print("The tree for the above sentence is:")
    print(tree)
    break