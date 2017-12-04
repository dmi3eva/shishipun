#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os

class Task_mark:
   text = ''
   mark = 0
   def __init__(self, txt, mrk):
       self.text = txt
       self.mark = mrk
       
def generate_files_name(file_name):
    global user_id
    module_dir = os.path.dirname(__file__)
    file = os.path.join(module_dir + '/res' + str(user_id) + '/' +file_name + '.txt')
    return file       

def generate_tasks_marks(user):
    global user_id
    user_id = user