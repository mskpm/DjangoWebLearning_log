from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404

# Create your views here.

from django.http import HttpResponse
from .models import Topic, Entry

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import TopicForm, EntryForm


def index(request):
    #return HttpResponse("Hello, world. You're at the learning log.")
 
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Wyświetlenie wszystkich tematów."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

@login_required
def topic(request, topic_id):
    """Wyświetla pojedynczy temat i wszystkie związane z nim wpisy."""
    topic = Topic.objects.get(id=topic_id)
    # Upewniamy się, że temat należy do bieżącego użytkownika
    check_topic_owner(topic, request)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic, 'entries':entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Dodaj nowy teamt"""
    if request.method != 'POST':
        # Nie przekazano żadnch danych, należy utworzyć pusty formularz
        form = TopicForm()
    else:
        # Przekazano dane za pomocą żądania POST, należy je prztworzyć
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
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

@login_required
def edit_entry(request, entry_id):
    """Edycja istniejącego wpisu"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # Upewniamy się, że temat należy do bieżącego użytkownika
    check_topic_owner(topic, request)
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

@login_required
def del_entry(request, entry_id):
    """Skasowanie instniejącego wpisu"""

    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    form = EntryForm(instance=entry)
     # Upewniamy się, że temat należy do bieżącego użytkownika
    check_topic_owner(topic, request)
    if request.method == 'POST':
        entry.delete()
        return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
    context = {'entry':entry, 'topic':topic, 'form':form}
    return render(request, 'learning_logs/del_entry.html', context)

def check_topic_owner(topic, request):
    # Upewniamy się, że temat należy do bieżącego użytkownika
    if topic.owner != request.user:
        raise Http404
