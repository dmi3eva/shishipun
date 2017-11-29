
# coding: utf-8

# In[6]:

import numpy as np
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
morph.parse('Моржов')

question_words = {'nomn': ['кто', 'что'], 'gent': ['кого', 'чего'], 'datv': ['кому', 'чему'], 'accs': ['кого', 'что'], 'ablt': ['кем', 'чем'], 'loct': ['ком', 'чём']}


def remove_punctuation(s):
    s = s.replace(",", "")
    s = s.replace(":", "")
    s = s.replace(".", "")
    s = s.replace("!", "")
    s = s.replace("?", "")
    s = s.replace("-", "")
    s = s.replace("  ", "")
    return s






# In[154]:

#Находит относящийся к слову предлог
def preposition(sentence, word):
    word = word.lower()
    sentence = sentence.lower()
    sentence = remove_punctuation(sentence)
    words = sentence.split(" ")
    
    position = words.index(word)
    ind = position - 1
    while (ind != -1):
        analysis = morph.parse(words[ind])[0].tag.POS
        if (analysis == "NOUN" or analysis == "NPRO"):
            return ""
        if (analysis == "PREP"):
            return words[ind]
        ind -= 1
    return ""

def adjective(sentence, word):
    word = word.lower()
    sentence = sentence.lower()
    sentence = sentence.lower()
    sentence = remove_punctuation(sentence)
    words = sentence.split(" ")
    position = words.index(word)
    ind = position - 1
    if (ind >= 0):
        analysis = morph.parse(words[ind])[0].tag.POS
        if (analysis == "ADJF"):
            return words[ind]
    return ""

def predicate(sentence, word):
    word = word.lower()
    sentence = sentence.lower()
    sentence = remove_punctuation(sentence)
    words = sentence.split(" ")
    position = words.index(word)
    ind = position - 1
    while (ind != -1):
        analysis = morph.parse(words[ind])[0].tag.POS        
        if (analysis == "VERB"):            
            return words[ind]
        ind -= 1
    ind = position + 1
    while (ind != len(words)):
        analysis = morph.parse(words[ind])[0].tag.POS
        if (analysis == "VERB"):
            return words[ind]
        ind += 1
    return ""


def all_subordinates(sentence):
    sentence = sentence.lower()
    sentence = remove_punctuation(sentence)
    words = sentence.split(" ")
    candidates = []
    pronouns = ["он", "она", "оно", "они"]
    for i in range(len(words)):
        analysis = morph.parse(words[i])[0].tag
        if (words[i] in pronouns):
            candidates.append(words[i])
        if (analysis.POS == "NOUN"):
            if (analysis.case == "nomn"):
                candidates.append(words[i])
    if (len(candidates) > 1):        
        for i in range(len(candidates)):
            analysis = morph.parse(candidates[i])[0]
            if (analysis.inflect({'nomn'}).word == analysis.inflect({'accs'}).word):
                if (len(candidates) > 1): 
                    candidates.remove(candidates[i])
    return candidates
        

def subordinate(sentence, word):
    sentence = sentence.lower()
    sentence = remove_punctuation(sentence)
    words = sentence.split(" ")
    position = words.index(word)
    subordinates = all_subordinates(sentence)
    ind = len(subordinates) - 1
    if (len(subordinates) == 0):
        return ""
    while (position < words.index(subordinates[ind]) and ind > 0):
        ind -= 1
    if (ind == 0):
        return subordinates[0]
    else:
        return subordinates[ind - 1]
    return ""

def descriptive(sentence, word):
    sentence = sentence.lower()
    sentence = remove_punctuation(sentence)
    words = sentence.split(" ")
    position = words.index(word)
    norm = ["NUMR", "ADJF", "PREP"]
    res = word
    ind = position - 1
    while (ind != -1):
        analysis = morph.parse(words[ind])[0].tag.POS        
        if (analysis in norm or words[ind].isdigit()):
            res =  words[ind] + " " + res
            if (analysis == "PREP"):
                return res        
        else:
            return res        
        ind -= 1
    return res
    
def all_addendums(sentence):
    subordinates = all_subordinates(sentence)
    sentence = sentence.lower()
    sentence = remove_punctuation(sentence)
    words = sentence.split(" ")
    #res_des = []
    res = []
    for i in range(len(words)):
        analysis = morph.parse(words[i])[0].tag.POS        
        if ((analysis == "NOUN") & (words[i] not in subordinates)):
            #res_des.append(descriptive(sentence, words[i]))
            res.append(words[i])            
    return res



# In[152]:

def post_process(initial_sentence, sentence):
    sentence = sentence.replace("  ", " ")
   
    if (sentence[0:5] == "В что"):
        res = return_to_capital("Во что " + initial_sentence, sentence[5:])
        return res   
    return return_to_capital(initial_sentence, sentence)

def return_to_capital(initial_sentence, question):
    question = question.strip()
    initial_sentence = remove_punctuation(initial_sentence)
    sentence = initial_sentence.lower()   
    words_s = sentence.split(" ")
    words_i = initial_sentence.split(" ")
    words_q = question.split(" ")
    
    for i in range(1,len(words_q)):
        if (words_q[i] in question_words.keys()):
            pos = words_s.index(words_q[i])
            if (words_i[pos][0].isupper() & pos != 0):
                words_q[i] = words_q[i][0].upper() + words_q[i][1:]
    return " ".join(words_q)


# In[160]:

def private_noun_question(sentence, noun):
    noun= noun.lower()
    initial_sentence = sentence
    subordinators = all_subordinates(sentence)
    question = ""
    features = morph.parse(noun)[0].tag
    time_words = ["год", "век", "утро", "день", "вечер", "ночь", "зима", "лето", "весна", "осень"]
    
    if (not noun.isdigit() and features.POS != "NUMR" and morph.parse(noun)[0].normal_form not in time_words):
        #add preposition
        question +=preposition(sentence, noun) + " "

        #add question word
        if (features.animacy == "anim"):
            question += question_words[features.case][0] + " "
        else:
            question += question_words[features.case][1] + " "
    else:
        question += "Когда "
    
    
    #add predicate and subordinate
    predicator = predicate(sentence, noun)
    subordinator = subordinate(sentence, noun)
    if (noun not in subordinators):
        question += adjective(sentence, subordinator) + " " + subordinator + " " + predicator + " "
    else:
        question +=predicator + " "
    #add addendum
    addendums = all_addendums(sentence)  
    print(addendums)
    for i in range(len(addendums)):        
        if (noun != addendums[i]):            
            question += " " + descriptive(sentence, addendums[i])
           
    
    question += "?"
    question = question.strip(' ').capitalize()
    return post_process(initial_sentence, question)
  
    
#testing    
sentence = "Лейбниц в 1666 году опубликовал свой труд в известном журнале."
word = "лейбниц"


print(private_noun_question(sentence, word))


# In[118]:




# In[ ]:



