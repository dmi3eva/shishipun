from django.shortcuts import render
from chat.models import User
import os
from chat.for_web import generate_answer

user_id = ''
user_dialog = {}
theory_dialog = []
file =''
mode="sug_parameters_name"
last_answer = ""

class Mes:
   source =''
   text = ''
   def __init__(self, src, txt):
       self.source = src
       self.text = txt

def auth(request):
    return render(request, 'chat/auth.html')
    
def auth_check(request):
    global user_id, dialog
    print(user_id)
    log = request.POST.get('login', '')
    pas = request.POST.get('password', '')
    users = User.objects.all()
    for user in users:
        if (user.login == log and user.password == pas):
            request.session['member_id'] = user.id
            print(request.session['member_id'])
            user_dialog.update({request.session['member_id']:[]})
            return render(request, 'chat/choose_type.html')
    return render(request, 'chat/auth.html')
    
def message_sent(request):
    global user_id
    if request.session['member_id'] == '':
        return render(request, 'chat/auth.html')
    else:
        user = User.objects.get(id = request.session['member_id'])
        text_a = "Привет, " + str(user.login) + "!"
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
    global last_answer, mode
    text_q = request.GET['chat_label']
    last_answer = text_q;
    
    print(request.session['member_id'])
    mes_q = Mes('user', text_q)
    dialog.append(mes_q)

    text_a = generate_answer(last_answer)
    mes_a = Mes('bot', text_a)
    dialog.append(mes_a)
    user_dialog.update({request.session['member_id']:dialog})
    c = {"mes": dialog}
    return render(request, 'chat/message_list.html', c)

def choose_type(request):
    if request.session['member_id'] == '':
        return render(request, 'chat/auth.html')
    return render(request, 'chat/choose_type.html')

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
        
def theory_message_list(request):
    if request.session['member_id'] == '':
        return render(request, 'chat/auth.html')
        
    text_q = request.GET['theory_chat_label']    
    mes_q = Mes('user', text_q)
    theory_dialog.append(mes_q)

    text_a = "answer"
    mes_a = Mes('bot', text_a)
    theory_dialog.append(mes_a)
    if file != None:
        c = {"file": file, "mes": theory_dialog}
    else:
        c = {"mes": theory_dialog}
    return render(request, 'chat/theory_message_list.html', c)
