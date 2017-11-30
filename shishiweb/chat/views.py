from django.shortcuts import render
from chat.models import User
import os
from chat.problem_solving import generate_answer
from chat.theory_asking import generate_replic

user_id = ''
user_dialog = {}
theory_user_dialog = {}
file =''
last_answer = ""
last_answers ={}
theory_last_answers ={}
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

def logout(request):
    user_dialog.update({request.session['member_id']:[]})
    request.session['member_id'] = ''
    return render(request, "chat/auth.html")      

def auth(request):
    return render(request, 'chat/auth.html')
    
def auth_check(request):
    global user_id, dialog, theory_dialog
    log = request.POST.get('login', '')
    pas = request.POST.get('password', '')
    print(log, pas)
    users = User.objects.all()
    print(users)
    for user in users:
        if (user.login == log and user.password == pas):
            request.session['member_id'] = user.id
            user_dialog.update({request.session['member_id']:[]})
            theory_user_dialog.update({request.session['member_id']:[]})
            return render(request, 'chat/choose_type.html')
    return render(request, 'chat/auth.html')

def message_sent(request):
    global user_id
    if request.session['member_id'] == '':
        return render(request, 'chat/auth.html')
    else:
        user = User.objects.get(id = request.session['member_id'])
        text_a = "Привет, " + str(user.name) + "!"
        mes_a = Mes('bot', text_a)
        dialog = user_dialog.get(request.session['member_id'])
        dialog.append(mes_a)
        user_dialog.update({request.session['member_id']:dialog})
        c = {"mes": dialog}
        return render(request, 'chat/message_list.html', c)

def message_list(request):
    if request.session['member_id'] == '':
        return render(request, 'chat/auth.html')
    dialog = user_dialog.get(request.session['member_id'])
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
    if request.session['member_id'] == '':
        return render(request, 'chat/auth.html')
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
    if request.session['member_id'] == '':
        return render(request, 'chat/auth.html')
    else:
        user = User.objects.get(id = request.session['member_id'])
        text_a = "Привет, " + str(user.name) + "! Расскажи мне что-нибудь о том, что мы будем изучать. Если же ты, наоборот, хочешь проверить мои знания, просто обратись ко мне по имени. Например, \"Шишипун, что такое комбинаторика?\""
        mes_a = Mes('bot', text_a)
        theory_dialog = theory_user_dialog.get(request.session['member_id'])
        theory_dialog.append(mes_a)
        theory_user_dialog.update({request.session['member_id']:theory_dialog})
        c = {"mes": theory_dialog}
        return render(request, 'chat/theory_message_list.html', c)
        
def theory_message_list(request):
    if request.session['member_id'] == '':
        return render(request, 'chat/auth.html')
    
    theory_dialog = theory_user_dialog.get(request.session['member_id'])
    
    global theory_last_answers, user_id
    
    text_q = request.GET['theory_chat_label']
    theory_last_answers.update({request.session['member_id']:text_q})
    
    mes_q = Mes('user', text_q)
    theory_dialog.append(mes_q)
    
       
    user_id = request.session['member_id']
    theory_last_answer = theory_last_answers[request.session['member_id']]

    text_a = generate_replic(theory_last_answer, user_id)
    mes_a = Mes('bot', text_a)
    theory_dialog.append(mes_a)
    
    theory_user_dialog.update({request.session['member_id']:theory_dialog})
    c = {"mes": theory_dialog}
    return render(request, 'chat/theory_message_list.html', c)
    
def rating(request):
    users = User.objects.order_by('-bot_mark')
    c = {"users": users}
    return render(request, 'chat/rating.html', c)
    
def test(request):
    global tasks
    tasks_marks = []
    task_mark = Task_mark('Сколько существует способов выбрать 1 час из 24, чтобы поспать?', 1)
    tasks_marks.append(task_mark)
    
    task_mark = Task_mark('Сколько существует способов выбрать несколько часов из 24, чтобы поспать?', 0)
    tasks_marks.append(task_mark)
    
    
    
    tests.update({request.session['member_id']:tasks_marks})
    
    tasks = tests[request.session['member_id']]
    
    c = {"tasks": tasks}
    return render(request, 'chat/test.html', c)
