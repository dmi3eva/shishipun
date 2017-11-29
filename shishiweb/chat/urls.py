from django.conf.urls import url
from . import views

urlpatterns = [
    url('theory_chat/$', views.theory_message_sent, name='theory_message_sent'),
    url(r'sent_theory', views.theory_message_list, name='theory_message_list'),
    url('^chat/$', views.message_sent, name='message_sent'),
    url(r'sent', views.message_list, name='message_list'),
    url('type/$', views.choose_type, name='choosing_type'),
    url('rating/$', views.rating, name='rating'),
    url('test/$', views.test, name='test'),
    url('auth/', views.auth, name='auth'),
    url('auth_check', views.auth_check, name='auth_check'),
    url('logout/', views.logout, name='logout'),
    url('^$', views.auth),
]

