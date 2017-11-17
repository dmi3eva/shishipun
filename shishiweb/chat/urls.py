from django.conf.urls import url
from chat.views import hello, auth
from . import views

urlpatterns = [
    url('hello/$', hello),
    url('chat/$', views.message_sent, name='message_sent'),
    url(r'sent', views.message_list, name='message_list'),
    url('^$', auth),
    
]