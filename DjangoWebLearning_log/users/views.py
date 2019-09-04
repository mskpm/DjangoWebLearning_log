from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm

def logout_view(request):
    """Wylogowywanie użytkownika"""
    logout(request)
    return HttpResponseRedirect(reverse('learning_logs:index'))

def register(request):
    """Rejestracja nowego użytkownika"""
    if request.method != 'POST':
        # Wyświetlanie pustego formularza rejestracji użytkownika
        form = UserCreationForm()
    else:
        # Przetwarzanie wypełnionego formularza
        form = UserCreationForm(data=request.POST)

    if form.is_valid():
        new_user = form.save()
        # Zalogowanie użytkownika, a następnie przekierowanie go na stronę główną
        authenticated_user = authenticate(username = new_user.username,
            password = request.POST['password1'])
        login(request, autenticated_user)
        return HttpResponseRedirect(reverse('lerning_logs:index'))
    context = {'form': form}
    return render(request, 'users/register.html', context)


