#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
from chat.problem_solving import replace_word_with_numbers, defining_parameters_train, w_sug_parameters, t_sug_classification, t_classification_train, t_read_classification_names, t_ans_train, t_sug_answer

tests_file = "test_tasks"
open_tasks_amount = 6

class Task_mark:
   text = ''
   mark = 0
   def __init__(self, txt, mrk):
       self.text = txt
       self.mark = mrk
       
def generate_global_files_name(file_name):
    global user_id
    module_dir = os.path.dirname(__file__)
    file_g = os.path.join(module_dir + '/res/' + file_name + '.txt')
    return file_g
    
def read_tests():
    filename = generate_global_files_name(tests_file)
    if os.path.exists(filename)==False:
        print("Something wrong with files")
    test_file = open(filename, 'r')
    content = test_file.read()
    all_tasks = content.split('@')
    tasks = []
    answers = []
    all_tasks.pop()
    for i in range(len(all_tasks)):
        print(i)
        tmp = all_tasks[i].split('#')
        tasks.append(tmp[0])
        answers.append(int(tmp[1]))
    
    test_file.close()
    return tasks, answers
    
def answer(text, dp_clf, cl_clf, ans_clfs):
    global user_id
    tmp, task_features, predictions = w_sug_parameters(dp_clf, text)  
    processed_task = replace_word_with_numbers(text)
    features, task_type = t_sug_classification(cl_clf, processed_task, task_features, predictions)
    answer = t_sug_answer(user_id, ans_clfs, task_type, processed_task, predictions)
    return int(answer)
    
def mark(bot_answer, right_answer):
    if (int(bot_answer) == int(right_answer)):
        return 0 # верно
    else:
        return 1 

def generate_tasks_marks(user):
    global user_id
    user_id = user
    tasks, answers = read_tests()
    
    results = []
    dp_clf = defining_parameters_train(user_id)
    cl_clf = t_classification_train(user_id)
    ans_clfs = []
    types = t_read_classification_names(user_id)
    for i in range(len(types)):
        ans_clfs.append(t_ans_train(user_id, i + 1))
            
    summ = 0
    for i in range(len(tasks)):
        grade = mark(answer(tasks[i], dp_clf, cl_clf, ans_clfs), answers[i])
        summ += 1 - grade
        if (i < open_tasks_amount):
            result = Task_mark(tasks[i], grade)
        else:
            result = Task_mark("Закрытая задача", grade)
        results.append(result)
    return summ, results
    
