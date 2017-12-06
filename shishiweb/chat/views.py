from django.shortcuts import render
from chat.models import User
import os, shutil
from chat.problem_solving import generate_answer, change_mode
from chat.theory_asking import generate_replic
from chat.testing import generate_tasks_marks

user_id = ''
user_dialog = {}
theory_user_dialog = {}
test_theory_user_dialog = {}
file =''
last_answer = ""
last_answers ={}
theory_last_answers ={}
test_theory_last_answers ={}
tests = {}
    
class Mes:
   source =''
   text = ''
   def __init__(self, src, txt):
       self.source = src
       self.text = txt

class Task_mark:
   text = ''
   mark = 0
   def __init__(self, txt, mrk):
       self.text = txt
       self.mark = mrk

def reset_education(request):
    module_dir = os.path.dirname(__file__)
    print(request.session['member_id'])
    target_dir = os.path.join(module_dir + '/res' + str(request.session['member_id']))       
    shutil.rmtree(target_dir)
    source_path = module_dir + '/initial_res'
    shutil.copytree(source_path, target_dir)
    return render(request, 'chat/auth.html')
    
def check_session(request):
    if 'member_id' not in request.session:
        return render(request, "chat/auth.html")
    else:
        return 0
        
def help(request):
    return render(request, "chat/help.html")
    
def logout(request):
    if 'member_id' not in request.session:
        request.session['member_id'] = ''
    else:
        change_mode(request.session['member_id'])
        user_dialog.update({request.session['member_id']:[]})
        theory_user_dialog.update({request.session['member_id']:[]})
        test_theory_user_dialog.update({request.session['member_id']:[]})
        request.session['member_id'] = ''
    return render(request, "chat/auth.html")      

def auth(request):
    return render(request, 'chat/auth.html')
    
def auth_check(request):
    if 'member_id' not in request.session:
        request.session['member_id'] = ''
    global user_id, dialog, theory_dialog
    log = request.POST.get('login', '')
    pas = request.POST.get('password', '')
    users = User.objects.all()
    for user in users:
        if (user.login == log and user.password == pas):
            request.session['member_id'] = user.id
            user_dialog.update({request.session['member_id']:[]})
            theory_user_dialog.update({request.session['member_id']:[]})
            test_theory_user_dialog.update({request.session['member_id']:[]})
            return render(request, 'chat/choose_type.html')
    return render(request, 'chat/auth.html')

def message_sent(request):
    if 'member_id' not in request.session:
        request.session['member_id'] = ''
    global user_id
    if request.session['member_id'] == '':
        return render(request, 'chat/auth.html')
    else:
        user = User.objects.get(id = request.session['member_id'])
        text_a = "Привет, " + str(user.name) + "!"
        mes_a = Mes('bot', text_a)
        dialog = user_dialog.get(request.session['member_id'])
        if dialog is None:
            dialog = []
        dialog.append(mes_a)
        user_dialog.update({request.session['member_id']:dialog})
        c = {"mes": dialog}
        return render(request, 'chat/message_list.html', c)

def message_list(request):
    if 'member_id' not in request.session:
        request.session['member_id'] = ''
    if request.session['member_id'] == '':
        return render(request, 'chat/auth.html')
    dialog = user_dialog.get(request.session['member_id'])
    if dialog is None:
            dialog = []
    global last_answer, user_id,last_answers
    
    text_q = request.GET['chat_label']
    last_answers.update({request.session['member_id']:text_q})
    
    mes_q = Mes('user', text_q)
    dialog.append(mes_q)
    
    user_id = request.session['member_id']
    last_answer = last_answers[request.session['member_id']]

    text_a = generate_answer(last_answer, user_id)
    mes_a = Mes('bot', text_a)
    dialog.append(mes_a)
    
    user_dialog.update({request.session['member_id']:dialog})
    c = {"mes": dialog}
    return render(request, 'chat/message_list.html', c)

def choose_type(request):
    if 'member_id' not in request.session:
        request.session['member_id'] = ''
    if request.session['member_id'] == '':
        return render(request, 'chat/auth.html')
    change_mode(request.session['member_id'])
    user_dialog.update({request.session['member_id']:[]})
    theory_user_dialog.update({request.session['member_id']:[]})
    test_theory_user_dialog.update({request.session['member_id']:[]})
    return render(request, 'chat/choose_type.html')
"""
def theory_file_upload(request):
    if request.session['member_id'] == '':
        return render(request, 'chat/auth.html')
    return render(request, 'chat/theory_file_upload.html') 
    
def theory_file(request):
    #parameters_names_file = static('/res/features.txt')
    #par_file = open(os.path.join(settings.STATIC_ROOT, '/res/features.txt'))
    if request.session['member_id'] == '':
        return render(request, 'chat/auth.html')
        
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir + '/res/features.txt')
    par_file = open(file_path, 'r')
    par_file.close()
    if request.method == "POST":
        file = request.FILES['theory_file'].read()
        text_a = "Я прочитал файл!"
        mes_a = Mes('bot', text_a)
        theory_dialog.append(mes_a)
        c = {"file": file, "mes": theory_dialog}
        return render(request,'chat/theory_message_list.html', c)           
    else:
        file = "Пожалуйста, загрузите файл"
        c = {"file": file}
        return render(request, 'chat/theory_file_upload.html', c)
"""     

def theory_message_sent(request):
    global user_id
    theory_dialog = []
    if 'member_id' not in request.session:
        request.session['member_id'] = ''
    if request.session['member_id'] == '':
        return render(request, 'chat/auth.html')
    else:
        user = User.objects.get(id = request.session['member_id'])
        text_a = "Привет, " + str(user.name) + "! Расскажи мне что-нибудь о том, что мы будем изучать."
        mes_a = Mes('bot', text_a)
        theory_dialog = theory_user_dialog.get(request.session['member_id'])
        if theory_dialog is None:
            theory_dialog = []
        theory_dialog.append(mes_a)
        theory_user_dialog.update({request.session['member_id']:theory_dialog})
        c = {"mes": theory_dialog}
        return render(request, 'chat/theory_message_list.html', c)
        
def theory_message_list(request):
    theory_dialog = []
    if 'member_id' not in request.session:
        request.session['member_id'] = ''
    if request.session['member_id'] == '':
        return render(request, 'chat/auth.html')
    
    theory_dialog = theory_user_dialog.get(request.session['member_id'])
    if theory_dialog is None:
            theory_dialog = []

    global theory_last_answers, user_id
    
    text_q = request.GET['theory_chat_label']
    theory_last_answers.update({request.session['member_id']:text_q})
    
    mes_q = Mes('user', text_q)
    theory_dialog.append(mes_q)
    
       
    user_id = request.session['member_id']
    theory_last_answer = theory_last_answers[request.session['member_id']]

    text_a = generate_replic(theory_last_answer, user_id, 0)
    mes_a = Mes('bot', text_a)
    theory_dialog.append(mes_a)
    
    theory_user_dialog.update({request.session['member_id']:theory_dialog})
    c = {"mes": theory_dialog}
    return render(request, 'chat/theory_message_list.html', c)
    
def rating(request):
    if 'member_id' not in request.session:
        request.session['member_id'] = ''
    if request.session['member_id'] == '':
        return render(request, 'chat/auth.html')
    test_theory_user_dialog.update({request.session['member_id']:[]})
    users = User.objects.order_by('-bot_mark')
    c = {"users": users}
    return render(request, 'chat/rating.html', c)
    
def test(request):
    global tasks
    if 'member_id' not in request.session:
        request.session['member_id'] = ''
    if request.session['member_id'] == '':
        return render(request, 'chat/auth.html')
    #tasks_marks = []
    #task_mark = Task_mark('Сколько существует способов выбрать 1 час из 24, чтобы поспать?', 1)
    #tasks_marks.append(task_mark)
    
    #task_mark = Task_mark('Сколько существует способов выбрать несколько часов из 24, чтобы поспать?', 0)
    #tasks_marks.append(task_mark)
    res, tasks_marks = generate_tasks_marks(user_id)
    user = User.objects.get(id = request.session['member_id'])
    setattr(user,'bot_mark', res)
    user.save()
    print(user.bot_mark)
    
    tests.update({request.session['member_id']:tasks_marks})
    
    tasks = tests[request.session['member_id']]
    
    c = {"tasks": tasks}
    return render(request, 'chat/test.html', c)

def test_chat(request):
    global user_id
    theory_test_dialog = []
    if 'member_id' not in request.session:
        request.session['member_id'] = ''
    if request.session['member_id'] == '':
        return render(request, 'chat/auth.html')

    user = User.objects.get(id = request.session['member_id'])
    text_a = "Привет, " + str(user.name) + "!" + "Я готов пройти тестирование!"
    mes_a = Mes('bot', text_a)
    
    theory_test_dialog = test_theory_user_dialog.get(request.session['member_id'])
    if theory_test_dialog is None:
        theory_test_dialog = []
    theory_test_dialog.append(mes_a)
    print(theory_test_dialog)
    test_theory_user_dialog.update({request.session['member_id']:theory_test_dialog})
    c = {"mes": theory_test_dialog}
    return render(request, 'chat/test_theory_message_list.html', c)
        
def test_chat_sent(request):
    theory_test_dialog = []
    if 'member_id' not in request.session:
        request.session['member_id'] = ''
    if request.session['member_id'] == '':
        return render(request, 'chat/auth.html')
    
    theory_test_dialog = test_theory_user_dialog.get(request.session['member_id'])
    if theory_test_dialog is None:
            theory_test_dialog = []

    global test_theory_last_answers, user_id
    
    text_q = request.GET['test_theory_chat_label']
    print(text_q)
    test_theory_last_answers.update({request.session['member_id']:text_q})
    
    mes_q = Mes('user', text_q)
    theory_test_dialog.append(mes_q)
    
       
    user_id = request.session['member_id']
    test_theory_last_answer = test_theory_last_answers[request.session['member_id']]

    text_a = generate_replic(test_theory_last_answer, user_id, 1)
    mes_a = Mes('bot', text_a)
    theory_test_dialog.append(mes_a)
    
    test_theory_user_dialog.update({request.session['member_id']:theory_test_dialog})
    c = {"mes": theory_test_dialog}
    return render(request, 'chat/test_theory_message_list.html', c)
