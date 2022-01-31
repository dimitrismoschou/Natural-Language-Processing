from nltk.tokenize import word_tokenize, sent_tokenize
def sent_split(documents):
    words = [word_tokenize(sent) for sent in sent_tokenize(text)]
    return words

text = 'My name is Dimitris and I am an Olympic Laser Sailing athlete from Greece !'
t=sent_split(text)
print(t)