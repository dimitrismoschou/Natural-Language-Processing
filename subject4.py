import ast
import os
import nltk
nltk.download('punkt')
import pandas as pd
import spacy
from spacy.matcher import Matcher
import networkx as nx
import matplotlib.pyplot as plt
nlp = spacy.load('en_core_web_sm')

#Reads a string that contains that contains sentences and finds entities, relations and reloards
#.txt file of knowledge base
def load_sentences_to_knowledge_base(sstring,knlg_database,relationsold):
  sentences = nltk.tokenize.sent_tokenize(sstring)
  entities = []
  relations = []
  for i in range(len(sentences)):
    entities.append(get_entities(sentences[i]))
    relations.append(get_relation(sentences[i]))
  knlg_database = knlg_database + entities
  relationsold = relationsold + relations
  open("knowledge_base.txt", "w").close()
  with open("knowledge_base.txt", "w") as the_file:
    the_file.write(str(knlg_database) + "\n" + str(relationsold))
  return knlg_database, relationsold

#Reads a file and finds entities, relations and reloads
# .txt file of knoledge base
def load_file_to_knowledge_base(file_name,knlg_database,relationsold):
  try:
    text = read_from_file(file_name)
    sentences = nltk.tokenize.sent_tokenize(text)

    entities = []
    relations = []
    for i in range(len(sentences)):
      entities.append(get_entities(sentences[i]))
      relations.append(get_relation(sentences[i]))
    knlg_database = knlg_database + entities
    relationsold = relationsold + relations
    open("knowledge_base.txt", "w").close()
    with open("knowledge_base.txt", "w") as the_file:
      the_file.write(str(knlg_database)+"\n"+str(relationsold))
    return knlg_database,relationsold
  except OSError as e:
    print("File does not exist.")
    return knlg_database,relationsold

def get_entities(sent):
  sent = sent.lower()
  ent1 = ""
  ent2 = ""

  prv_tok_dep = ""
  prv_tok_text = ""

  prefix = ""
  modifier = ""

  for token in nlp(sent):
    #If token is a fullstop then go to next token
    if token.dep_ != "punct":
      #Checks if token is a complex word
      if token.dep_ == "compound":
        prefix = token.text
        #If previous word was complex the add it
        if prv_tok_dep == "compound":
          prefix = prv_tok_text + " " + token.text

      #If token is a modifier
      if token.dep_.endswith("mod") == True:
        modifier = token.text
        #If previous word was complex the add it
        if prv_tok_dep == "compound":
          modifier = prv_tok_text + " " + token.text

      #If subject found
      if token.dep_.find("subj") == True:
        entity1 = modifier + " " + prefix + " " + token.text
        prefix = ""
        modifier = ""
        previous_tok_dep = ""
        previous_tok_text = ""

      #If object found
      if token.dep_.find("obj") == True:
        entity2 = modifier + " " + prefix + " " + token.text

      #Variable reload
      prv_tok_dep = tok.dep_
      prv_tok_text = tok.text

  print([ent1.strip(), ent2.strip()])
  return [ent1.strip(), ent2.strip()]

def get_relation(sent):

  doc = nlp(sent)

  # Matcher class object
  matcher = Matcher(nlp.vocab)

  #ορισμός του προτύπου
  pattern = [{'DEP':'ROOT'},
            {'DEP':'prep','OP':"?"},
            {'DEP':'agent','OP':"?"},
            {'POS':'ADJ','OP':"?"}]

  matcher.add("matching_1", None, pattern)

  matches = matcher(doc)
  k = len(matches) - 1

  span = doc[matches[k][1]:matches[k][2]]
  print(span.text)
  return(span.text)

#Διαβάζει ένα αρχείο και επιστρέφει το κείμενο που περιέχει
def read_from_file(file_name):
  file1 = open(file_name, "r+", encoding="utf8")
  print("The file text is:")
  text = file1.read()
  return text

#Plots know;edge graph
def draw_knowledge_graph(entities,relations):
  # extract subject
  source = [i[0] for i in entities]

  # extract object
  target = [i[1] for i in entities]

  kg_df = pd.DataFrame({'source': source, 'target': target, 'edge': relations})
  # create a directed-graph from a dataframe
  G = nx.from_pandas_edgelist(kg_df, "source", "target",
                              edge_attr=True, create_using=nx.MultiDiGraph())
  plt.figure(figsize=(12, 12))

  pos = nx.spring_layout(G)
  nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos=pos)
  plt.show()

#Converts list to a dictionary for every index of the list
def list_to_dictionary_with_indexes(lst):
  dict = {}
  for i in range(len(lst)):
    dict[i] = lst[i]
  return dict

#Διαγραφή ενός στοιχείου από την βάση σε κάποιο συγκεκριμένο index
def delete_from_db(index,entities,relations):
  try:
    entities.pop(index)
    relations.pop(index)
    open("knowledge_base.txt", "w").close()
    with open("knowledge_base.txt", "w") as the_file:
      the_file.write(str(entities) + "\n" + str(relations))
    return entities, relations
  except IndexError:
    print("Not a valid index (out of range)")
    return entities,relations

#Αν δεν υπάρχει αρχείο για την βάση γνώσης φτιάξε ένα
if not os.path.exists("knowledge_base.txt"):
  with open("knowledge_base.txt", "w") as the_file:
    the_file.write(str("[]\n[]"))

#Φόρτοση της βάσης γνώσης από το txt αρχείο στις ανάλογες λίστες
database = open("knowledge_base.txt", 'r')
Lines = database.readlines()
knowledge_database = ast.literal_eval(Lines[0].strip())
relations_database = ast.literal_eval(Lines[1].strip())
draw_knowledge_graph(knowledge_database, relations_database)


while True:
  # Menu with options
  print('------------------------Menu------------------------')
  print('1. Insert sentences from a file.')
  print('2. Insert sentence/sentences as input')
  print('3. Ask a question to the knowledge database')
  print('4. Show the knowledge database')
  print('5. Delete something from knowledge database')
  print('6. Exit the script')
  print("----------------------------------------------------")
  try:
    user_choice = int(input("Choose:"))
    #Αν δεν είναι ένας αριθμός από το 1-4 τότε η είσοδος είναι λάθος
    if user_choice<0 or user_choice>6:
      print("Not a valid number. Choose a number from 1-4.")
      continue
  #Αν δεν είναι αριθμός τότε είναι λάθος
  except ValueError:
    print("Not a valid number. Choose a number from 1-4.")
  #Αν ειναι η 6η επιλογή τερμάτισε το πρόγραμμα
  if user_choice == 6:
    exit(0)
  #Αν είναι η 4η επιλογή τότε εμφάνισε την βάση σε μορφή πίνακα με ένα pandas dataframe
  if user_choice == 4:
    source = [i[0] for i in knowledge_database]
    target = [i[1] for i in knowledge_database]
    sdf = pd.DataFrame({'Entity[0]': source, 'Entity[1]': target, 'Relation': relations_database})
    print(sdf)
  #Αν είναι η 1η επιλογή τότε φόρτωσε από το αρχείο που θα δοθεί από τον χρήστη
  #στην βάση γνώσης
  if user_choice == 1:
    fl = input("File name:")
    knowledge_database,relations_database = load_file_to_knowledge_base(fl,knowledge_database,relations_database)
    draw_knowledge_graph(knowledge_database, relations_database)
  #Αν είναι η 2η επιλογή τότε φόρτωσε από το string που θα δοθεί από τον χρήστη
  #στην βάση γνώσης
  if user_choice == 2:
    snt = input("Write the sentence/sentences:")
    knowledge_database, relations_database = load_sentences_to_knowledge_base(snt,knowledge_database, relations_database)
    draw_knowledge_graph(knowledge_database, relations_database)
  #Αν είναι η 3η επιλογή τότε ψάξε την ερώτηση που θα δώσει ο χρήστης στην βάση γνώσης και απάντησε
  if user_choice == 3:
    question = input("Write a question to the database:")
    t = get_entities(question)
    if t not in knowledge_database:
      print("Output: No")
    else:
      r = knowledge_database.index(t)
      print("Output: ",relations_database[r])
  #Αν είναι η 5η επιλογή τότε γίνεται διαγραφή ενός στοιχείου από την βάση
  if user_choice == 5:
    print(list_to_dictionary_with_indexes(knowledge_database))
    print(list_to_dictionary_with_indexes(relations_database))
    try:
      #Πάρε ως είσοδο το index για διαγραφή
      indx = int(input("Choose a index from the dictionary to delete from the database:"))
      knowledge_database,relations_database = delete_from_db(indx,knowledge_database,relations_database)
      draw_knowledge_graph(knowledge_database, relations_database)
      print("Deleted successfully")
    except ValueError:
      print("Not a valid index")
      continue