from django.conf.urls import url
from . import views

urlpatterns = [
    url('theory_file_upload/$', views.theory_file_upload, name='theory_file_upload'),
    url('theory_file/$', views.theory_file, name='theory_file'),
    url(r'sent_theory', views.theory_message_list, name='theory_message_list'),
    url('^chat/$', views.message_sent, name='message_sent'),
    url(r'sent', views.message_list, name='message_list'),
    url('type/$', views.choose_type, name='choosing_type'),
    url('auth/$', views.auth),
    url('auth_check/$', views.auth_check),
    url('^$', views.auth),
]

