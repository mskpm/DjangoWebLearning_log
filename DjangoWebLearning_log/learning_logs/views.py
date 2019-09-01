from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import Topic, Entry

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from .forms import TopicForm, EntryForm

def index(request):
    #return HttpResponse("Hello, world. You're at the learning log.")
 
    return render(request, 'learning_logs/index.html')

def topics(request):
    """Wyświetlenie wszystkich tematów."""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    """Wyświetla pojedynczy temat i wszystkie związane z nim wpisy."""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic, 'entries':entries}
    return render(request, 'learning_logs/topic.html', context)

def new_topic(request):
    """Dodaj nowy teamt"""
    if request.method != 'POST':
        # Nie przekazano żadnch danych, należy utworzyć pusty formularz
        form = TopicForm()
    else:
        # Przekazano dane za pomocą żądania POST, należy je prztworzyć
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

def new_entry(request, topic_id):
    """Dodanie nowego wpisu dla określonego tematu"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # Nie przekazano żadnych danych, należy utworzyć pusty formularz
        form = EntryForm()
    else:
        # Przekazano dane za pomocą żadania POST, należy je przetworzyć
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
            #return HttpResponseRedirect(reverse('learning_logs:topic'))
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

def edit_entry(request, entry_id):
    """Edycja istniejącego wpisu"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    
    if request.method != 'POST':
        # Żądanie początkowe wypełnienie formularza aktualną treścią wpisu
        form = EntryForm(instance=entry)
    else:
        # Przekazane dane za pomocą żądania POST, należy je przetworzyć
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
    context = {'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'learning_logs/edit_entry.html', context)

def del_entry(request, entry_id):
    """Skasowanie instniejącego wpisu"""

    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    form = EntryForm(instance=entry)
    
    if request.method == 'POST':
        entry.delete()
        return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
    context = {'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'learning_logs/del_entry.html', context)
