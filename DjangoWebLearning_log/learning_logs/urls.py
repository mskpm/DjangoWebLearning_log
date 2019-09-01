"""Definiuje wzorce adresów URL dla learning_logs"""

from django.urls import path, re_path
from . import views

app_name = 'learning_log'

urlpatterns = [
    # Strona główna
    path('', views.index, name='index'),
    
    # Wyświetlanie wszytkich tematów
    path('topics', views.topics, name='topics'),

    # Strona szczegółowa dotycząca pojedynczego tematu
    #re_path('topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
    path('topics/<int:topic_id>/', views.topic, name='topic'),

    # Strona przeznaczona dla dodawania nowego tematu
    path('new_topic/', views.new_topic, name='new_topic'),

    # Strona przeznaczona do dodawania nowego wpisu
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    #re_path('new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),

    # Strona przeznaczona do do edycji wpisu
    #re_path(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),
    path('edit_entry/<int:entry_id>', views.edit_entry, name='edit_entry'),

    # Strona przeznaczona do kasowania wpisu
    path('del_entry/<int:entry_id>', views.del_entry, name='del_entry'),
]
