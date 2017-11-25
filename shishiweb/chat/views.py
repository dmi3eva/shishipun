from django.shortcuts import render
from django.http import HttpResponse
from chat.models import User

dialog = []
theory_dialog = []
file =''

class Mes:
   source =''
   text = ''
   def __init__(self, src, txt):
       self.source = src
       self.text = txt

def auth(request):
    return render(request, 'chat/auth.html')
    
def auth_check(request):
    log = request.POST.get('login', '')
    pas = request.POST.get('password', '')
    users = User.objects.all()
    for user in users:
        if (user.login == log and user.password == pas):
            return render(request, 'chat/choose_type.html')
    return render(request, 'chat/auth.html')
    
def message_sent(request):
    return render(request, 'chat/chat.html')

def message_list(request):
    text_q = request.GET['chat_label']
    mes_q = Mes('user', text_q)
    dialog.append(mes_q)

    text_a = "answer"
    mes_a = Mes('bot', text_a)
    dialog.append(mes_a)
    c = {"mes": dialog}
    return render(request, 'chat/message_list.html', c)

def choose_type(request):
    return render(request, 'chat/choose_type.html')

def theory_file_upload(request):
    return render(request, 'chat/theory_file_upload.html') 
    
def theory_file(request):
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
    text_q = request.GET['theory_chat_label']
    mes_q = Mes('user', text_q)
    theory_dialog.append(mes_q)

    text_a = "answeredgtrfhyugyttbiuhuihnubyftrxgcvjhnuygtfgvhjgybytdcyvjhgj"
    mes_a = Mes('bot', text_a)
    theory_dialog.append(mes_a)
    if file != None:
        c = {"file": file, "mes": theory_dialog}
    else:
        c = {"mes": theory_dialog}
    return render(request, 'chat/theory_message_list.html', c)
