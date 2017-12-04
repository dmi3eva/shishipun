
# coding: utf-8


import os
import shutil

parameters_names_file = 'parameters_names'
parameters_label_file = "train_parameters_label"
parameters_features_file = "train_parameters_features"
processed_tasks_file = "user_tasks"


classification_names_file = 'tasks_types'
classification_label_file = 'train_classification_labels'
classification_features_file = "train_classification_features"

def generate_files_name(file_name):
    global user_id
    module_dir = os.path.dirname(__file__)
    file = os.path.join(module_dir + '/res' + str(user_id) + '/' +file_name + '.txt')
    return file
    
def copy_initial_files(source_path, target_path):
    shutil.copytree(source_path, target_path)
    print(source_path, target_path)
    
def generate_inital_files(filename):
    target_path = os.path.split(filename)[0]
    print(target_path)
    module_dir = os.path.dirname(__file__)
    source_path = module_dir + '/initial_res'
    copy_initial_files(source_path, target_path)
    
#Save parameters of the task (same for all tasks from the theme)
def save_parameters_names(list_of_parameters_names): 
    filename = generate_files_name(parameters_names_file)
    par_file = open(filename, 'w')
    for parameter in list_of_parameters_names:
        par_file.write(parameter + '\n')
    par_file.close()
    


# In[62]:

#Read parameters of the task (same for all tasks from the theme)
def read_parameters_names():  
    filename = generate_files_name(parameters_names_file)
    if os.path.exists(filename)==False:
        generate_inital_files(filename)
    par_file = open(filename, 'r')
    content = par_file.read()
    list_of_parameters_names = content.split('\n')
    list_of_parameters_names.pop()
    par_file.close()
    
    
    
    return list_of_parameters_names
#print(read_parameters_names())


# In[ ]:




# In[ ]:




# In[63]:

def intersect(l1, l2):
    return (len(list(set(l1) & set(l2))) > 0)

def remove_punctuation(s):
    s = s.replace(",", "")
    s = s.replace(":", "")
    s = s.replace(".", "")
    s = s.replace("!", "")
    s = s.replace("?", "")
    s = s.replace("-", "")
    s = s.replace("  ", "")
    return s

def process_answer(s):
    s = remove_punctuation(s)
    s = s.lower()
    s = s.strip()
    
    return s

def process_answer_with_comma(s):   
    s = s.lower()
    s = s.strip()
    s = s.replace(",", "хюх")
    s = s.replace(" ", "ыыёы")
    s = s.title()
    s = s.replace("ыыёы", " ")
    s = s.replace("хюх", ",")
    
    return s


def w_sug_parameters_names(): 
    
    output = "Я правильно понимаю, что нам нужно найти значение следующих параметров:\n"
    names = read_parameters_names()
    for i in range(len(names)):
        if (i != len(names) - 1):
            output += "   " + str(i + 1) + ". " + names[i] + "\n"
        else:
            output += "   " + str(i + 1) + ". " + names[i] + "?" + "\n"
    output += "Все правильно?\n"
    return output
    
def quest_parameters_names():    
    ans = input("Введите: \n \"1\", если всё правильно \n \"0\", иначе\n")
    while (ans != "0" & ans != "1"):
        ans = input("Введите: \n \"1\", если всё правильно \n \"0\", иначе\n")
    

def ans_parameters_names(): 
    possible_yes = ["да", 'правильно', 'верно', 'согласен', 'согласна', 'yes']
    possible_no = ["нет"]
    ans = ""
    while (1):
        ans = input()
        ans = process_answer(ans)
        
        ans_words = ans.split(" ")
        if (intersect(ans_words, possible_yes)):
            print("Ура! Я рад, что всё правильно!")
            break
        else:
            if (intersect(ans_words, possible_no)):
                repair_parameters_names()
                break
            else:
                print("К сожалению, я не понял ответа. Напишите, пожалуйста, \"да\" или \"нет\".")
                
            
    
        
def repair_parameters_names(): 
    new_names_str = input("Перечислите через точку с запятой названия параметров:\n")
    new_names = new_names_str.split(";")
    for i in range(len(new_names)):        
        new_names[i] = process_answer_with_comma(new_names[i])
        
    
    save_parameters_names(new_names)
    
def w_repair_parameters_name():
    return "Значения каких параметров в задаче нужно найти? Перечислите через точку с запятой:\n"

    
def w_repair_classification_names():
    return "Перечислите через точку с запятой, какие типы задач бывают:\n"

def w_repair_classification_names_done(ans):
    new_names = ans.split(";")
    for i in range(len(new_names)):        
        new_names[i] = process_answer_with_comma(new_names[i])   
    
    save_classification_names(new_names) 
    return "Я запомнил!"
    
def w_repair_parameters_done(answer):
    new_names = answer.split(";")
    for i in range(len(new_names)):
        new_names[i] = process_answer_with_comma(new_names[i])
    save_parameters_names(new_names)
    return "Я запомнил!"

def read_task():
    nums = []
    parameters_names = read_parameters_names() 
    while (len(nums) < len(parameters_names)):
        task = input("Введите текст задачи:\n")
        processed_task = replace_word_with_numbers(task)
        nums = extract_numbers(processed_task)
        if (len(nums) < len(parameters_names)):
            print("Не могу найти достаточное количество данных=( Попробуйте ввести все числительне цифрами!")
            
    return task

def w_sug_task():
    return "Введите текст задачи:\n"

def w_repair_task(task):
    parameters_names = read_parameters_names() 
    processed_task = replace_word_with_numbers(task)
    nums = extract_numbers(processed_task)
    if (len(nums) < len(parameters_names)):
        return "false", "Не могу найти достаточное количество данных=( Попробуйте ввести все числительне цифрами!"
    else:
        return "true", "Классная задача!"
    


# In[66]:

import numpy as np
import pymorphy2
morph = pymorphy2.MorphAnalyzer()


# In[67]:

def save_task(task, fname, delimiter):
    filename = generate_files_name(fname)
    if os.path.exists:
        file = open(filename, 'a') #if file exists, than add new task
    else:
        file = open(filename, 'w') # else create new file
    
    file.write(task)
    file.write(delimiter)
    file.close()
    return 0


# In[68]:

#Словарь числительных (нужно дополнять)
num_dict = {'несколько': 10000000007,
            'один': 1,
            'одному': 1,
            'два': 2,
            'двоих': 2,
            'двое': 2,
            'двум': 2,
            'три': 3,
            'троих': 3,
            'трое': 3,
            'трем': 3,
            'трём': 3,
            'трёх': 3,
            'трех': 3,
            'четыре': 4,
            'четырем': 4,
            'четырём': 4,
            'четырёх': 4,
            'четырех': 4,
            'четверых': 4,
            'четверо': 4,
            'пять': 5,
            'пяти': 5,
            'петярых': 5,
            'пятеро': 5,
            'пятерым': 5,
            'шесть': 6,
            'шести': 6,
            'шестерых': 6,
            'шестерым': 6,
            'шестеро': 6,
            'семь': 7,
            'семерых': 7,
            'семеро': 7,
            'семерым': 7,
            'семи': 7,
            'восемь': 8,
            'восьмерых': 8,
            'восьми': 8,
            'восьмеро': 8,
            'восьмерым': 8,
            'девять': 9,
            'девятерых': 9,
            'девятерым': 9,
            'девятеро': 9,
            'девяти': 9,
            'десять': 10,
            'десяти': 10,
            'десятерых': 10,
            'десятерым': 10,
            'десятеро': 10,
            'одиннадцать': 11,
            'двенадцать': 12,
            'тринадцать': 13,
            'четырнадцать': 14,
            'пятнадцать': 15,
            'шестнадцать': 16,
            'семнадцать': 17,
            'восемнадцать': 18,
            'девятнадцать': 19,
            'двадцать': 20,
            'тридцать': 30,
            'сорок': 40,
            'пятьдесят': 50,
            'шестьдесят': 60,
            'семьдесят': 70,
            'восемьдесят': 80,
            'девяносто': 90,
            'сто': 100,
            'двести': 200,
            'триста': 300,
            'четыреста': 400,
            'пятьсот': 500,
            'шестьсот': 600,
            'семьсот': 700,
            'восемьсот': 800,
            'девятьсот': 900,
            'тысяча': 1000,
            'миллион': 1000000,
            'миллиард': 1000000000,
           }

#Функция для того, чтобы отделить знаки препинания от слов с помощью добавления пробела

def punctuation_separ(task):
    task = task.replace('.', ' .')
    task = task.replace('?', ' ?')
    task = task.replace('!', ' !')
    task = task.replace(';', ' ;')
    task = task.replace(':', ' :')
    task = task.replace('(', ' (')
    task = task.replace(')', ' )')
    task = task.replace(',', ' ,')
    return task

#Функция объединяет слова из списка в строку, удаляет лишние пробелы

def listToString(task):
    task_ret = []
    
    for elem in task:
        if elem != '' and elem != ' ':
            task_ret.append(elem)
    s = ' '
    task_ret = s.join(task_ret)
    task_ret = task_ret.replace(' .', '.')
    task_ret = task_ret.replace(' ?', '?')
    task_ret = task_ret.replace(' !', '!')
    task_ret = task_ret.replace(' ;', ';')
    task_ret = task_ret.replace(' :', ':')
    task_ret = task_ret.replace(' (', '(')
    task_ret = task_ret.replace(' )', ')')
    task_ret = task_ret.replace(' ,', ',')
    
    return task_ret

#Функция замены числительных на цифры, возвращает задачу, в которой произведены замены

def replace_word_with_numbers(task):
    task = punctuation_separ(task)
    
    task = task.split()
    for i in range(len(task)):
        if task[i] in num_dict:
            if task[i + 1] in num_dict:
                if task[i + 2] in num_dict:
                    task[i] = str(num_dict[task[i]] + num_dict[task[i + 1]] + num_dict[task[i + 2]])
                    task[i + 1] = ''
                    task[i + 2] = ''
                else:
                    task[i] = str(num_dict[task[i]] + num_dict[task[i + 1]])
                    task[i + 1] = ''
            else:
                task[i] = str(num_dict[task[i]])
    task_ret = listToString(task)
    return task_ret
"""
Проверка части речи с помощью библиотеки pymorphy2, возращаем все тэги о слове, нет парсинга.
"""
def check_part_of_speech(word):
    morph = pymorphy2.MorphAnalyzer()
    answer = (morph.parse(word))
    return answer

"""
Если есть существительное, то выводим его, его одушевленность (0-неодушевленный, 1-одушевленный),
строку с прилагательным о существительном (выбираем прилагательное самое близкое к параметру (к цифре))
Если существительного нет, или предложение закончилось, то возвращаем пустую строку.
"""
def extract_noun(task, parameter):
    #task = task.decode('utf-8')
    task_list = punctuation_separ(task)

    task_list = task_list.split()

   
    
    adj =""
    
    index = -1
    for i in range(len(task_list)):
        if(task_list[i] == str(parameter)):
            index = i
            break
    for i in range(index, len(task_list)):
        answer = check_part_of_speech(task_list[i])[0]
        if adj =="" and 'ADJF' == answer.tag.POS:
            adj = task_list[i]
        if 'NOUN' == answer.tag.POS:
            index= i
            break
        if 'PNCT' in answer.tag:
            return '', '', ''
    
    if index != -1:
        if index < len(task_list) - 1:
            if answer.tag.animacy == 'anim':
                return task_list[index], 1, adj
            elif answer.tag.animacy == 'inan':
                return task_list[index], 0, adj
            else:
                return task_list[index]
        else:
            return '', '', ''
    return '', '', ''




# In[69]:

#Чтение задач и лэйблов из файла, сохраняем их вместе с лэйблами в файл

import os

def read_task_from_file(fname):
    filename = generate_files_name(fname)
    if os.path.exists(filename):
        file = open(filename, 'r')
    else:
        print("No such file: " + str(filename))
        return 0
    tasks =[]
    s = ""
    for line in file:
        if "@" not in line:
            s += line
        else:
            tasks.append(s)
            s = ""
    return tasks



# In[71]:

def word_number(text):
    while (text.find("  ") != -1):
        text = text.replace("  ", " ")
    return (text.count(" ") + 1)

def extract_sentence_with_parameter(parameter, text):
    pattern = str(parameter) #cast to string
    sentence = ""
    position = text.find(pattern)
    punctuation_marks = ".?!\n"
    left = position
    while ((left > 0) & (text[left] not in punctuation_marks)):
        left -= 1
    if (text[left] in punctuation_marks):
        left += 1
        if (text[left] == " "):
            left += 1
            
    right = position
    while ((right < len(text))):
        if (text[right] in punctuation_marks):
            break
        right += 1
    
    return text[left : right]


# In[72]:

#find position (as proportion) of the number in the text (if we count for letters)
def extract_text_position_as_letters(parameter, text): 
    #text =  text.decode('utf-8')
    pattern = str(parameter) #cast to string
    parameterPosition = text.find(pattern) #two bytes for russian letters 
    numberOfLetters = len(text)
    
    if (numberOfLetters == 0):
        print("Text is empty!")
        return 0
    if (text.find(pattern) == -1):
        print("1Pattern \"" + pattern + "\" doesn't exist in the text!")
        return 0
    return float(parameterPosition) / numberOfLetters


#find position (as proportion) of the number in the sentence (if we count for letters)
def extract_sentence_position_as_letters(parameter, text): 
    #text =  text.decode('utf-8')
    pattern = str(parameter) #cast to string
    sentence = extract_sentence_with_parameter(parameter, text)
    
    parameterPosition = sentence.find(pattern) #two bytes for russian letters 
    numberOfLetters = len(sentence)
    if (numberOfLetters == 0):
        print("Sentence is empty!")
        return 0
    if (sentence.find(pattern) == -1):
        print("2Pattern \"" + pattern + "\" doesn't exist in the text!")
        return 0
    return float(parameterPosition) / (numberOfLetters - 1)


# In[73]:

def extract_text_position_as_words(parameter, text): 
    #text =  text.decode('utf-8')
    pattern = str(parameter) #cast to string
    parameterPosition = text.find(pattern) #two bytes for russian letters 
    number_of_words = word_number(text)
    if (number_of_words == 0):
        print("Text is empty!")
        return 0
    
    if (text.find(pattern) == -1):
        print("3Pattern \"" + pattern + "\" doesn't exist in the text!")
        return 0
    before_parameter = text[0 : text.find(pattern)]
    number_of_words_before_parameter = word_number(before_parameter)
    return float(number_of_words_before_parameter) / number_of_words

def extract_sentence_position_as_words(parameter, text): 
    #text =  text.decode('utf-8')
    pattern = str(parameter) #cast to string
    sentence = extract_sentence_with_parameter(parameter, text)
    parameterPosition = sentence.find(pattern) #two bytes for russian letters 
    number_of_words = word_number(sentence)
    if (number_of_words == 0):
        print("Text is empty!")
        return 0
    if (sentence.find(pattern) == -1):
        print("4Pattern \"" + pattern + "\" doesn't exist in the text!")
        return 0
    before_parameter = sentence[0 : sentence.find(pattern)]
    number_of_words_before_parameter = word_number(before_parameter)
    return float(number_of_words_before_parameter) / number_of_words



# In[74]:

def extract_numbers(text):
    #text =  text.decode('utf-8')
    numbers = "0123456789"
    parameters = []
    ind = 0
    mode = 0 #not number in process
    cur_num = ""
    for i in range(len(text)):
        if (text[i] in numbers):
            mode = 1
            cur_num += text[i]
        else:
            if mode == 1:
                parameters.append(cur_num)
                cur_num = ""
                mode = 0
    if mode == 1:
        parameters.append(cur_num)
                 
                
    return parameters



# In[75]:

def k_stat(parameters, parameter):
    ordered = []
    for i in range(len(parameters)):
        ordered.append(parameters[i])
    
    ordered.sort()
    
    
    cur = ordered[0] - 1
    ind = -1
    k = -1
    while (cur != parameter):
        ind += 1
        if (ordered[ind] != cur):
            k += 1
        cur = ordered[ind]
    return k

#Количество прилагательных в предложении с параметром
def adj_number(parameter, text):
    sent = extract_sentence_with_parameter(parameter, text)
    #sent = sent.decode('utf-8')
    words = sent.split(" ")
    res = 0
    for word in words:        
        if word[-1] in ",.!?:-":
            word = word.replace(word[-1], "")
        if ((str(morph.parse(word)[0].tag)[0] == "A") & (str(morph.parse(word)[0].tag)[1] == "D")):
            res += 1
        
    return res  

#Возвращает количество второстепенных знаков перпинания

def punctuation(parameter, text):
    punctuation_marks = ",:"
    sent = extract_sentence_with_parameter(parameter, text)
    #sent = sent.decode('utf-8')
    res = 0
    for letter in sent:
        if (letter in punctuation_marks):
            res += 1
    return res

#Кодирует слово числом
def feature_hash(word):
    #word = word.decode('utf-8')
    word = str(word)
    res = 0
    base = 33
    rank = 1
    for ind in range(len(word)):
        res += (ord(word[ind]) - 1000) * rank
        
        rank *= base
    if (len(word) == 1):
        res = ord(word[ind]) - ord('A')
    return res


#Извлекает часть речи первого слова из предложения с параметром. Прилагательное от наречия не отличает.
def extract_first_word_in_sentence(parameter, text):
    #text = text.decode('utf-8')
    sent = extract_sentence_with_parameter(parameter, text)
    words = sent.split(" ")
    word = words[0]
    res = str(morph.parse(word)[0].tag)[0]        
    return res  


# In[76]:

def extract_parameter_features(parameters, number, text):
    for i in range(len(parameters)):
        parameters[i] = int(parameters[i])
    parameter_features = []
    parameter_features.append(parameters[number]) #само число
    parameter_features.append(extract_text_position_as_words(parameters[number], text)) #позиция в тексте (% в словах)
    parameter_features.append(extract_sentence_position_as_words(parameters[number], text)) #позиция в предложении (% в словах)
    parameter_features.append(extract_text_position_as_letters(parameters[number], text)) #позиция в тексте (% в символах)
    parameter_features.append(extract_sentence_position_as_letters(parameters[number], text)) #позиция в предложении (% в символах)
    parameter_features.append(k_stat(parameters, parameters[number])) #размер относительно других числительных
    parameter_features.append(number) #позиция относительно других числительных
    parameter_features.append(np.abs(parameters[number] - np.mean(parameters))) #отклонение от среднего остальных параметров
    parameter_features.append(adj_number(parameters[number], text)) #количество прилагательных в предложении с параметром 
    parameter_features.append(punctuation(parameters[number], text))#количество второстепенных знаков препинания
    noun, live, adj = extract_noun(text, parameters[number])
    parameter_features.append(feature_hash(noun)) #существительное, к которому относится
    parameter_features.append(feature_hash(live)) #одушевленное?
    parameter_features.append(feature_hash(adj)) #количество прилагательных в предложении с параметром (в процентах от общего числа)    
    parameter_features.append(feature_hash(extract_first_word_in_sentence(parameters[number], text)))#с какого слова начинается предложение с параметром
    
    return parameter_features


# In[77]:

def extract_all_parameters_features(text):
    #text = text.decode('utf-8')
    parameters_features = []
    substitution = -1007
    parameters = extract_numbers(text)    
    ind = 0
    
    for index in range(len(parameters)):            
        parameters_features.append(extract_parameter_features(parameters, index, text))            
        text = text.replace(str(parameters[index]), str(substitution), 1)     
            
    return parameters_features


# In[78]:

def read_param_from_task(task):
    words = task.split()
    parameters = []
    task = ''
    index = len(words)
    for i in range(len(words)):
        if words[i] == '#':
            index = i
        if i < index:
            task += str(words[i]) + ' '
        elif i > index:
            parameters.append(words[i])
    return task, parameters



# In[ ]:




# In[ ]:




# In[ ]:




# In[79]:

import numpy as np
import pandas as pd


# In[80]:

#preprocessing
from sklearn import preprocessing
from sklearn import tree
from sklearn.tree import DecisionTreeRegressor


#libraries for ANN
from sklearn.neural_network import MLPClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import accuracy_score


# In[81]:

#Reading data
def prepare_data_for_defining_parameter_training():
    parameters_names_file = 'parameters_names'
    parameters_names_file = generate_files_name(parameters_names_file)
    
    #test_parameters_label_file = "/res/test_parameters_label"
    #test_parameters_label_file = generate_files_name(test_parameters_label_file)
    
    #test_parameters_features_file = "/res/test_parameters_features"
    #test_parameters_features_file = generate_files_name(test_parameters_features_file)

    train_parameters_label_file = "train_parameters_label"
    train_parameters_label_file = generate_files_name(train_parameters_label_file)

    train_parameters_features_file = "train_parameters_features" 
    train_parameters_features_file = generate_files_name(train_parameters_features_file)
    
    train_features = pd.read_csv(train_parameters_features_file, header=None)
    
    train_labels = pd.read_csv(train_parameters_label_file, header=None)
    #test_features = pd.read_csv(test_parameters_features_file, header=None)
    #test_labels = pd.read_csv(test_parameters_label_file, header=None)
    train_features_scaled = preprocessing.scale(train_features)
    #test_features_scaled = preprocessing.scale(test_features)
    return train_features_scaled, train_labels


# In[82]:

################################
#    ANN with preprocessing    #
################################

def defining_parameters_train():
    data_train, label_train = prepare_data_for_defining_parameter_training()
    label_train = np.ravel(label_train)

    max_sc_ann = 0
    ls1 = 8 #calculated by several experiments
    ls2 = 10

    ann_clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(ls1, ls2), random_state=1)
    ann_clf.fit(data_train, label_train) 
    
    return ann_clf


# In[83]:

#Делает так, чтобы каждому параметру было что-то сопоставлено
def repair_prediction(prediction, parameters_number):
    values = dict()
    bad = []
    empty = []
    for i in range(len(prediction)):
        v = prediction[i]
        if (v in values.keys()):
            values[v] += 1
            bad.append(i)
        else:
            values[v] = 1
    for i in range(1, parameters_number + 1):
        if (i not in values.keys()):
            empty.append(i)
    for i in range(len(empty), len(bad)):
        empty.append(0)
    for i in range(len(bad)):
        prediction[bad[i]] = empty[i]
    return prediction


        


# In[84]:

def w_sug_parameters(clf, task):
        
        parameters_names = read_parameters_names()        
        processed_task = replace_word_with_numbers(task)
        nums = extract_numbers(processed_task)
        
        task_features = extract_all_parameters_features(processed_task)
        predictions = clf.predict(task_features)
        predictions = repair_prediction(predictions, len(parameters_names))
       
        answer = "Я думаю, что:\n"
        for i in range(len(predictions)):
                if (predictions[i] != 0): 
                    if (int(nums[i]) != 10000000007):
                        answer += "  " + parameters_names[int(predictions[i]) - 1] + " - " + str(int(nums[i])) + "\n"
                    else:
                        answer += "  " + parameters_names[int(predictions[i]) - 1] + " - 2 \n"
                    
        answer += "Правильно?"
        return answer, task_features, predictions


                
def w_ans(answer): 
    global last_answer
    possible_yes = ["да", 'правильно', 'верно', 'согласен', 'согласна']
    possible_no = ["нет"]
    ans = process_answer(answer)        
    ans_words = ans.split(" ")
    if (intersect(ans_words, possible_yes)):
        return "yes"
    if (intersect(ans_words, possible_no)):
        return "no"
    return "nothing"
            


# In[86]:

def find_index(l, v):
    for i in range(len(l)):
        if (l[i] == v):
            return i
    return -1


# In[87]:

def w_repair_parameters(answer, processed_task, nums):    
   
    global parameters_prediction
    global repair_parameters_iteration
    parameters_names = read_parameters_names() 
    i = repair_parameters_iteration
    replic = ""
    nums_s = []
    
    for j in range(len(nums)):
        nums_s.append(int(nums[j]))
    
    #if (i == 0):
        #prediction = np.zeros(len(nums))
        
    
    
    if (i != 0):
        value = int(answer)
        ind = find_index(nums_s, value)
   
        if (value == 2 and find_index(nums_s, 10000000007) != -1):
            parameters_prediction[find_index(nums_s, 10000000007)] = i
        else:
            if (ind == -1):                
                return -1, "Не могу найти это число в задаче. Давайте еще раз. Попробуйте записать все числительные цифрами."
            else:
                parameters_prediction[ind] = i
   
    
    
    
    repair_parameters_iteration += 1
    
    if (repair_parameters_iteration > len(parameters_names)):
        replic = ""
        return 1, replic
    else:  
        replic = "Сколько " + parameters_names[i].lower() + "?\n" 
        return 0, replic


# In[88]:

def save_defining_parameters(processed_task, task_features, predictions):
    
    save_task(processed_task, processed_tasks_file, "#\n")
    for i in range(len(task_features)):
        feature = str(task_features[i])        
        feature = feature[1:-1]        
        save_task(feature, parameters_features_file, "\n")
        save_task(str(predictions[i]), parameters_label_file, "\n")
    


# # Task classification

# Classification names

# In[89]:

#Read parameters of the task (same for all tasks from the theme)
def read_classification_names(): 
    filename = generate_files_name(classification_names_file)   
    cla_file = open(filename, 'r')
    content = cla_file.read()
    list_of_names = content.split('\n')
    list_of_names.pop()
    cla_file.close()
    
    
    return list_of_names



# In[90]:

#Save parameters of the task (same for all tasks from the theme)
def save_classification_names(list_of_parameters_names):     
    filename = generate_files_name(classification_names_file) 
    cla_file = open(filename, 'w')
    for parameter in list_of_parameters_names:
        cla_file.write(parameter + '\n')
    cla_file.close()
    


# In[91]:

def w_sug_classification_names():    
    output = []
    output = "Правда ли, что задачи бывают следующих типов: \n"
    names = read_classification_names()
    for i in range(len(names)):
        if (i != len(names) - 1):
            output += "   " + str(i + 1) + ". " + names[i] + "\n"
        else:
            output += "   " + str(i + 1) + ". " + names[i] + "?" + "\n"
    output += "Все правильно?\n"
    return output
    
        
# Defining task type

# In[92]:

#Extract features for classification the task
def extract_classification_features(processed_task, parameters_features, parameters_labels):
    #processed_task = replace_word_with_numbers(task)
    nums = extract_numbers(processed_task)
    par_values = dict()
    par_features = dict()
    for i in range(len(parameters_labels)):
        if (int(parameters_labels[i]) != 0):
            par_values[int(parameters_labels[i])] = float(nums[i])
            par_features[int(parameters_labels[i])] = parameters_features[i]
    

    
    features = []
    if (len(par_values) > 1): 
        if (int(par_values[2]) != 0):
            features.append(float(par_values[1])/float(par_values[2])) #Отношение элементов к местам
        else:
            features.append(10000000007)
    
    for i in range(1, len(par_values) + 1):       
        features.append(float(par_values[i])) #Элементы, места (сами параметры, в общем случае)
            
   
    
    for i in range(1, len(par_values) + 1):        
        for j in range(0, len(par_features[i])):
            features.append(float(par_features[i][j]))
    
    return features


# In[93]:

def prepare_data_for_classification_training():
    parameters_names_file = 'tasks_types'
    parameters_names_file = generate_files_name(parameters_names_file)

    #test_classification_label_file = "/res/test_classification_labels"
    #test_classification_label_file = generate_files_name(test_classification_label_file)

    #test_classification_features_file = "/res/test_classification_features"
    #test_classification_features_file = generate_files_name(test_classification_features_file)

    train_classification_label_file = "train_classification_labels"
    train_classification_label_file = generate_files_name(train_classification_label_file)

    train_classification_features_file = "train_classification_features" 
    train_classification_features_file = generate_files_name(train_classification_features_file)
    
    train_features = pd.read_csv(train_classification_features_file, header=None)
    train_labels = pd.read_csv(train_classification_label_file, header=None)
    #test_features = pd.read_csv(test_classification_features_file, header=None)
    #test_labels = pd.read_csv(test_classification_label_file, header=None)
    train_features_scaled = preprocessing.scale(train_features)
    #test_features_scaled = preprocessing.scale(test_features)
    return train_features_scaled, train_labels


# In[94]:


    
################################
#    ANN with preprocessing    #
################################

def classification_train():
    data_train, label_train = prepare_data_for_classification_training()
    label_train = np.ravel(label_train)

    max_sc_ann = 0
    ls1 = 8 #calculated by several experiments
    ls2 = 10

    ann_clf = MLPClassifier(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(ls1, ls2), random_state=1)
    ann_clf.fit(data_train, label_train) 
    
    return ann_clf


# In[108]:


def w_sug_classification(processed_task, task_features, predictions):
    global cl_clf
    cl_clf = classification_train()
    features = extract_classification_features(processed_task, task_features, predictions)
    types = read_classification_names()
    features_list = []
    features_list.append(features)    
    prediction = cl_clf.predict(features_list)    
    replic = "Мне кажется, что эта задача относится к типу \"" + str(types[int(prediction) - 1]) + "\"\n Правильно?"
    return replic, features, int(prediction[0])
    





def w_repair_classification():
    global classification_names
    classification_names = read_classification_names() 
    replic = "Введите номер правильного типа задачи:\n"
    for i in range(len(classification_names)):
        replic += str(i + 1) + " - " + classification_names[i] + "\n"
    
    return replic


# In[120]:

def save_classification(processed_task, cl_features, task_type):
    f = str(cl_features)
    f = f[1:-1]
    save_task(f, classification_features_file, "\n")
    save_task(str(task_type), classification_label_file, "\n")


# # Finding answer

# In[98]:

def extract_answer_features(task, dp_labels):
    nums = extract_numbers(task)   
    dp_values = dict()
    for i in range(len(dp_labels)):
        if (int(dp_labels[i]) != 0):
            dp_values[int(dp_labels[i])] = float(nums[i])
    features_ans = []    
    for i in range(len(dp_values)):
        features_ans.append(dp_values[i + 1]) 
    return features_ans


# In[99]:

def prepare_data_for_answer_training(task_type):    
    folder = ""    
    #test_answer_label_file = folder + str(task_type) + "/test_answer_labels"
    #test_answer_label_file = generate_files_name(test_answer_label_file)

    #test_answer_features_file = folder + str(task_type) + "/test_answer_features"
    #test_answer_features_file = generate_files_name(test_answer_features_file)

    train_answer_label_file = folder + str(task_type) + "/train_answer_labels"
    train_answer_label_file = generate_files_name(train_answer_label_file)

    train_answer_features_file = folder + str(task_type) + "/train_answer_features" 
    train_answer_features_file = generate_files_name(train_answer_features_file)

    train_features = pd.read_csv(train_answer_features_file, header=None)
    train_labels = pd.read_csv(train_answer_label_file, header=None)
    #test_features = pd.read_csv(test_answer_features_file, header=None)
    #test_labels = pd.read_csv(test_answer_label_file, header=None)
    train_features_scaled = preprocessing.scale(train_features)
    #test_features_scaled = preprocessing.scale(test_features)
    #return train_features_scaled, test_features_scaled, train_labels, test_labels
    return train_features, train_labels




def ans_train(task_type):
    data_train, label_train = prepare_data_for_answer_training(task_type)
    clf = DecisionTreeRegressor()
    clf.fit(data_train, label_train)
    return clf


# In[109]:

def w_sug_answer(processed_task, predictions):
    global ans_clf
    global classification
    ans_clf = ans_train(classification)
    features = extract_answer_features(processed_task, predictions)
    features_list = []
    features_list.append(features)
    prediction = ans_clf.predict(features_list)    
    answer = int(prediction[0])
    replic = "Я подумал и решил, что ответ: " + str(answer) +  "\n Правильно?\n"
    return replic, features, answer


# In[102]:

def w_repair_answer():    
    return "А какой правильный ответ?\n"
    


# In[103]:

def save_answer(task_type, ans_features, answer):
    folder = ""
    answer_features_file = folder + str(task_type) + "/train_answer_features" 
       
    answer_label_file = folder + str(task_type) + "/train_answer_labels"

    f = str(ans_features)
    f = f[1:-1]
    save_task(f, answer_features_file, "\n")
    save_task(str(answer), answer_label_file, "\n")


# # Interaction with user

# In[ ]:




# In[ ]:




# # 

# In[ ]:




# In[104]:

sug_parameters_replic = "Давай переучимся!"


# In[105]:

#mode = "sug_parameters_name"
#last_answer = ""
#prediction = []

def yes_answer():
    return "Я рад, что всё правильно!"
def nothing_answer():
    return "К сожалению, я не понял ответа. Напишите, пожалуйста, \"да\" или \"нет\"."


# In[ ]:
modes = {}
last_answer = ""

def change_mode(user):
    global modes
    modes.update({user: "sug_parameters_name"})

def generate_answer(last_answer, user):    
    global modes, prediction
    global parameters_names, classification_names
    global task, nums, dp_clf, cl_clf, ans_clf
    global parameters, parameters_prediction, classification, answer
    global classification_features, answer_features, parameters_features
    global repair_parameters_iteration
    global user_id
    
    if user not in modes.keys():
        modes.update({user: "sug_parameters_name"})
    
    user_id = user
    
    if (last_answer == sug_parameters_replic):
        modes[user] = "sug_parameters_name"
        
##### Parameters names ######
        
    if ( modes[user] == "sug_parameters_name"):
        parameters_names = read_parameters_names()
        if (len(parameters_names) != 0):
            modes[user] = "ans_parameters_name"        
            return w_sug_parameters_names()
        else:
            modes[user] = "repair_parameters_name"
            return w_repair_parameters_name()
    
    if (modes[user] == "ans_parameters_name"):
        ans = w_ans(last_answer)
        if (ans == "yes"):
            modes[user] = "ans_classification_names"
            return yes_answer() + "\n" + w_sug_classification_names()  
        if (ans == "no"):
            modes[user] = "repair_parameters_name"
            return w_repair_parameters_name()
        if (ans == "nothing"):
            return nothing_answer()
        
    if (modes[user] == "repair_parameters_name"):
        #mode = "sug_classification_names"
        classification_names = read_classification_names()
        if (len(classification_names) != 0):
            modes[user] = "ans_classification_names"        
            return w_repair_parameters_done(last_answer) + "\n" + w_sug_classification_names()
        else:
            modes[user] = "repair_classification_names"
            return w_repair_parameters_done(last_answer) + "\n" + w_repair_classification_names()
        
         
    
    
##### Classification names ######     
    
    if (modes[user] == "ans_classification_names"):
        ans = w_ans(last_answer)
        if (ans == "yes"):
        
            modes[user] = "sug_task"
            return yes_answer() + "\n" + w_sug_task()
        if (ans == "no"):
            modes[user] = "repair_classification_names"
            return w_repair_classification_names()
        if (ans == "nothing"):
            return nothing_answer()
        
    if (modes[user] == "repair_classification_names"):
        modes[user] = "sug_task"
        return w_repair_classification_names_done(last_answer) + "\n" + w_sug_task()
    
    
##### Task ######
    
    
    if (modes[user] == "sug_task"):
        task = replace_word_with_numbers(last_answer)
        res, replic = w_repair_task(last_answer)
        save_task(task, processed_tasks_file, "\n#\n")
        if (res == "true"):
            nums = extract_numbers(task)
            dp_clf = defining_parameters_train()
            replic_par, parameters_features, parameters_prediction = w_sug_parameters(dp_clf, task)
            modes[user] = "sug_parameters"
        return replic + "\n" + replic_par
    
##### Defining parameters ######
    
    if (modes[user] == "sug_parameters"):        
        ans = w_ans(last_answer)
        if (ans == "yes"):
            modes[user] = "ans_classification" #todo
            save_defining_parameters(task, parameters_features, parameters_prediction)
            replic, classification_features, classification = w_sug_classification(task, parameters_features, parameters_prediction)
            return yes_answer() + "\n" + replic #todo
        if (ans == "no"):
            modes[user] = "repair_parameters" #todo
            repair_parameters_iteration = 0
            return w_repair_parameters(last_answer, task, nums)[1] #todo
        if (ans == "nothing"):
            return nothing_answer()
        
    if (modes[user] == "repair_parameters"):
        res, ans = w_repair_parameters(last_answer, task, nums)
        if (res == -1):
            modes[user] = "sug_task"
            return ans
        if (res == 1):
            save_defining_parameters(task, parameters_features, parameters_prediction)
            modes[user] = "ans_classification"
            replic, classification_features, classification = w_sug_classification(task, parameters_features, parameters_prediction)
            return replic 
        if (res == 0): 
            return ans
        
##### Classification ######
    if (modes[user] == "ans_classification"):
        ans = w_ans(last_answer)
        if (ans == "yes"):
            #print("Hello")
            modes[user] = "ans_answer"
            replic, answer_features, answer = w_sug_answer(task, parameters_prediction)            
            return yes_answer() + "\n" + replic
        if (ans == "no"):
            modes[user] = "repair_classification"
            return w_repair_classification()
        if (ans == "nothing"):
            return nothing_answer()
        
    if (modes[user] == "repair_classification"):
            classification = int(last_answer)
            save_classification(task, classification_features, classification)
            replic, answer_features, answer = w_sug_answer(task, parameters_prediction)
            modes[user] = "ans_answer"
            return replic
        
##### Answer ######
    if (modes[user] == "ans_answer"):
        ans = w_ans(last_answer)
        if (ans == "yes"):
            modes[user] = "sug_task"
            return yes_answer() + "\n" + w_sug_task()            
        if (ans == "no"):
            modes[user] = "repair_answer"
            return w_repair_answer()
        if (ans == "nothing"):
            return nothing_answer()
        
    if (modes[user] == "repair_answer"):
            answer = int(last_answer)
            save_answer(classification, answer_features, answer)
            modes[user] = "sug_task"
            return w_sug_task()  







