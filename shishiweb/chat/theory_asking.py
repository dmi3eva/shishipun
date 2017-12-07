# coding: utf-8

import numpy as np
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
import os
import shutil
from chat.problem_solving import generate_inital_files

theory_file = 'theory'


question_words = {'nomn': ['кто', 'что'], 'gent': ['кого', 'чего'], 'datv': ['кому', 'чему'], 'accs': ['кого', 'что'], 'ablt': ['кем', 'чем'], 'loct': ['ком', 'чём']}


def generate_files_name(file_name):
    global user_id
    module_dir = os.path.dirname(__file__)
    file = os.path.join(module_dir + '/res' + str(user_id) + '/' +file_name + '.txt')
    return file

def generate_global_files_name(file_name):
    global user_id
    module_dir = os.path.dirname(__file__)
    file = os.path.join(module_dir + '/res/' + file_name + '.txt')
    return file

    
def remove_punctuation(s):
    s = s.replace(",", " ")
    s = s.replace(":", " ")
    s = s.replace(".", " ")
    s = s.replace("!", " ")
    s = s.replace("?", " ")
    s = s.replace("-", " ")
    while (s.find("  ") != -1):
        s = s.replace("  ", " ")   
    s = s.strip()
    return s


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
    
    sentence = remove_punctuation(sentence)
    words = sentence.split(" ")
    position = words.index(word)
    ind = position - 1
    if (ind >= 0):
        analysis = morph.parse(words[ind])[0].tag.POS
        if (analysis == "ADJF"):
            return words[ind]
    return ""

def adverb(sentence, word):
    word = word.lower()
    sentence = sentence.lower()
    
    sentence = remove_punctuation(sentence)
    words = sentence.split(" ")
    position = words.index(word)
    ind = position - 1
    if (ind >= 0):
        analysis = morph.parse(words[ind])[0].tag.POS
        if (analysis == "ADVB"):
            return words[ind]
    return ""

def participle(sentence, word):
    word = word.lower()
    sentence = sentence.lower()
    
    sentence = remove_punctuation(sentence)
    words = sentence.split(" ")
    position = words.index(word)
    ind = position + 1
    if (ind < len(words)):
        print("   " + words[ind] + " POS = " + morph.parse(words[ind])[0].tag.POS)
        analysis = morph.parse(words[ind])[0].tag.POS
        if (analysis == "PRTS"):
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
        black_list = []
        for i in range(len(candidates)):            
            analysis = morph.parse(candidates[i])[0]
            if (analysis.inflect({'nomn'}).word == analysis.inflect({'accs'}).word):
                if (len(candidates) > 1):
                    isCountable = True
                    if (i > 0):
                        if (abs(words.index(candidates[i-1]) - words.index(candidates[i])) <= 1):
                            isCountable = False
                    if (i < len(candidates) - 1):
                        if (abs(words.index(candidates[i+1]) - words.index(candidates[i])) <= 1):
                            isCountable = False              
                    if (isCountable == True):
                        black_list.append(candidates[i])
        for w in black_list:
            candidates.remove(w)
                    
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

def descriptive(sentence, word, taboo):
    sentence = sentence.lower()
    sentence = remove_punctuation(sentence)
    words = sentence.split(" ")
    position = words.index(word)
    
    
    norm = ["NUMR", "ADJF", "PREP"]
    res = word + " "
    
    if (position < len(words) - 1):
        analysis = morph.parse(words[position + 1])[0].tag.POS
       
        if ((analysis == "NOUN") & (words[position + 1] != taboo) & (morph.parse(word)[0].tag.case == morph.parse(words[position + 1])[0].tag.case)):
            res += words[position + 1]
        
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



# In[282]:

def post_process(initial_sentence, sentence):
    sentence = sentence.replace("  ", " ")
   
    if (sentence[0:5] == "В что"):
        res = return_to_capital(initial_sentence, "Во что" + sentence[5:])
        res = res.replace("  ", " ")
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
            print(question_words[features.case][1])
            question += question_words[features.case][1] + " "
    else:
        question += "Когда "
    
    
    #add predicate and subordinate
    predicator = predicate(sentence, noun)
    subordinator = subordinate(sentence, noun)
    
    if (noun not in subordinators):
        print("Here")
        print(predicator)
        print("prt " + participle(sentence, predicator))
        question += adjective(sentence, subordinator) + " " + descriptive(sentence, subordinator, noun) + " " + adverb(sentence, predicator) + " " + predicator + " " + participle(sentence, predicator)
    else:
        if (morph.parse(noun[0])[0].tag.animacy == "anim"):
            prts = morph.parse(participle(sentence, predicator))[0]
            prts_norm = ""
            if (participle(sentence, predicator) != ""):
                prts_norm = prts.inflect({'neut'}).word
            vrb = morph.parse(predicator)[0]
            question += adverb(sentence, predicator) + " " + vrb.inflect({'masc'}).word + " " + prts_norm
        else:
            prts = morph.parse(participle(sentence, predicator))[0]
            vrb = morph.parse(predicator)[0]
            prts_norm = ""
            print("hello " + participle(sentence, predicator))
            if (participle(sentence, predicator) != ""):
                prts_norm = prts.inflect({'neut'}).word
            question += adverb(sentence, predicator) + " " + vrb.inflect({'neut'}).word + " " + prts_norm
    #add addendum
    addendums = all_addendums(sentence)  
    
    for i in range(len(addendums)):        
        if (noun != addendums[i]):            
            question += " " + descriptive(sentence, addendums[i], noun)
           
    
    
    question = question.strip(' ').capitalize()
    question += "?"
    return post_process(initial_sentence, question)
    
    
def sentence_intersection(sent1, sent2):
    s1 = remove_punctuation(sent1.lower())
    s2 = remove_punctuation(sent2.lower())
    words1 = s1.split(" ")
  
    
    words1 = list(map(lambda x: morph.parse(x)[0].normal_form, words1))
    
    words2 = s2.split(" ")       

    
    words2 = list(map(lambda x: morph.parse(x)[0].normal_form, words2))
    return set(words1) & set(words2)
    
def sentence_noun_intersection(sent1, sent2):
    s1 = remove_punctuation(sent1.lower())
    s2 = remove_punctuation(sent2.lower())
    words1_all = s1.split(" ")   
    words1_all = list(map(lambda x: morph.parse(x)[0].normal_form, words1_all))
    
    words1 = []
    for word in words1_all:
        if (morph.parse(word)[0].tag.POS == "NOUN"):
            words1.append(word)

    words2_all = s2.split(" ")    
    words2_all = list(map(lambda x: morph.parse(x)[0].normal_form, words2_all))
    words2 = []
    for word in words2_all:
        if (morph.parse(word)[0].tag.POS == "NOUN"):
            words2.append(word)
    
    return set(words1) & set(words2)
  
def dontknow_replic():
    return "Я не знаю, что ответить. Я только учусь =("
    
def too_many_info_replic():
    return "Я еще слишком маленький,чтобы столько запомнить сразу. Буду рад, если вы будете рассказывать мне по одному-два предложения."                                            
    
def short_answer_reaction_replic():
    return "=))) Расскажи мне что-нибудь еще."

def  not_found_question_replic():
    "Очень интересно! Расскажите что-нибудь ещё!"
     
     
def read_knowledge():
    filename = generate_files_name("knowledge")
    if not os.path.exists(filename): 
        generate_inital_files(filename)
        file_k = open(filename, 'w')
        
        content = ""
    else:
        file_k = open(filename, 'r')
        content = file_k.read()
    return content
    
def read_theory():
    filename = generate_global_files_name("theory")
    if not os.path.exists(filename): 
        generate_inital_files(filename)
        
        
        content = ""
    else:
        file_k = open(filename, 'r')
        content = file_k.read()
    return content    
    
def save_knowledge(new_info):
    filename = generate_files_name("knowledge")
    
    if not os.path.exists(filename):        
       
        generate_inital_files(filename)
    else:
        file_k = open(filename, 'a')
        file_k.write(new_info + ".")
        
    
    
def find_answer(question):
    knowledge = read_knowledge()
    if (len(knowledge) == 0):
        return dontknow_replic()
    else:
        sentences = knowledge.split(".")
        max_inter = 0
        best_sent = ""
        for i in range(len(sentences)):
            inter = sentence_intersection(question, sentences[i])
            print(sentences[i])
            print(inter)
            if (len(inter) > max_inter):
                max_inter = len(inter)
                best_sent = sentences[i]
                print(best_sent)
        print(max_inter)
        if (max_inter == 0):
            return dontknow_replic()
        else:
            if (max_inter < 2):
                return "Я знаю лишь то, что " + best_sent[0].lower() + best_sent[1:]
            return best_sent
            
def find_priority(statement):
    prior = dict()
    theory = read_theory()
    theory_sentences = theory.split(".")
    for i in range(len(theory_sentences)):
        inter = sentence_noun_intersection(theory_sentences[i], statement)
        if (len(inter) in prior.keys()):
            prior[len(inter)].append(theory_sentences[i])
        else:
            l = []
            l.append(theory_sentences[i])
            prior[len(inter)] = l  
    values = list(prior.keys())
    values.sort(reverse=True) 
    
    order = []
    for num in range(len(values)):
       
        for sent in prior[values[num]]:
            
            order.append(sent)  
    return order

def extract_normal_nouns(text):
    nouns = []
    processed_text = remove_punctuation(text.lower())
    words = processed_text.split(" ")
    for word in words:
        analysis = morph.parse(word)[0].tag.POS
        if (analysis == "NOUN"):
            nouns.append(morph.parse(word)[0].normal_form)
    return nouns 

def extract_nouns(text):
    nouns = []
    processed_text = remove_punctuation(text.lower())
    words = processed_text.split(" ")
    for word in words:
        analysis = morph.parse(word)[0].tag.POS
        if (analysis == "NOUN"):
            nouns.append(word)
    return nouns 
            
def read_special_knowledge(q_num):
    filename = generate_files_name("special_knowledge")
    res = []
    if not os.path.exists(filename): 
        generate_inital_files(filename)
        file_k = open(filename, 'w')
        for i in range(q_num):
            file_k.write('0\n')
            res.append(0)
        return res
    else:
        file_k = open(filename, 'r')
        content = file_k.read()
        res = content.split('\n')
    file_k.close()
    res.pop()
    return res
    
def write_special_knowledge(used):
    filename = generate_files_name("special_knowledge")
   
    
    file_k = open(filename, 'w')
    for i in range(len(used)):
        file_k.write(str(used[i]) + '\n')
    file_k.close()
    

def read_general_questions():
    questions = []
    keywords = []
    tabu = []
    filename = generate_global_files_name("general_questions")
    if os.path.exists(filename)==False:
        print("Something wrong with files")
    test_file = open(filename, 'r')
    content = test_file.read()
    all_tasks = content.split('@')
    
    all_tasks.pop()
    for i in range(len(all_tasks)):
        
        tmp = all_tasks[i].split('#')
        questions.append(tmp[0])
        keywords.append(tmp[1])
        tabu.append(tmp[2])
    
    test_file.close()
    return questions, keywords, tabu
    
def general_question(statement):   
    knowledge = read_knowledge()
    questions, keywords, tabu = read_general_questions()  
    q_num = len(questions)
    used = read_special_knowledge(q_num)
    for i in range(q_num):
        inter_k = sentence_intersection(keywords[i], statement)
        inter_t = sentence_noun_intersection(tabu[i], knowledge)
        if (len(inter_k) > 0 and len(inter_t) == 0 and int(used[i]) == 0):
            used[i] = 1
            write_special_knowledge(used)
            return questions[i]
    for i in range(q_num):
        inter_k = sentence_intersection(keywords[i], statement)
        inter_t = sentence_intersection(tabu[i], statement)
        if (len(inter_t) == 0 and int(used[i]) == 0):
            used[i] = 1
            write_special_knowledge(used)
            return questions[i]
    
    
    return ""

def find_question(statement):
    g_question = general_question(statement)
    if (g_question != ""):
        return g_question
    priority = find_priority(statement)
    knowledge = read_knowledge()
    facts = set(extract_normal_nouns(knowledge))
    print(facts)
    for i in range(len(priority)):
        candidate = priority[i]
        words = extract_nouns(candidate)
        for word in words:
            if (morph.parse(word)[0].normal_form not in facts):
                return private_noun_question(candidate, word)
    return not_found_question_replic()

        
    return "Сейчас кааак спрошу!"
    #order = find_order(statement)            
    
modes = {}



def generate_replic(last_answer, user, q_a): 
    global modes, user_id
    user_id = user
    if user not in modes.keys():
        modes.update({user: "question"})
    answer = last_answer.lower()
    answer = remove_punctuation(answer)
    answer_words = answer.split(" ")
    
    if (q_a == 1):
        modes[user] = "answer"
    if (modes[user] == "answer"):
        modes[user] = "question"
        return find_answer(last_answer)
    if (modes[user] == "question"):
        sentences = last_answer.split(".")
        if (len(sentences) > 4):
            return too_many_info_replic()
        else:
            words = last_answer.split(" ")
            save_knowledge(last_answer)
            if (len(words) < 3):
                return short_answer_reaction_replic()
            
            return find_question(last_answer)
            return "Сейчас кааак спрошу!"
    #if (modes[user] = "sug_parameters_name")    
    return "Прости меня, бездушную машину - я ничего не понял!"

