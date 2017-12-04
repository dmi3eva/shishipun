#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os

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
    file = os.path.join(module_dir + '/res/' + file_name + '.txt')
    return file 
    
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

def generate_tasks_marks(user):
    global user_id
    user_id = user
    tasks, answers = read_tests()
    print(tasks)
    print(answers)
    results = []
    for i in range(len(tasks)):
        if (i < open_tasks_amount):
            result = Task_mark(tasks[i], 1)
        else:
            result = Task_mark("Закрытая задача", 1)
        results.append(result)
    return results
    
