from django.shortcuts import render, redirect # redirects to wherever we define
from django.contrib.auth.forms import UserCreationForm # step 1: used for creating users and authetication
from django.http import HttpRequest

def register_view(request):
    if request.method == "POST": # all of this validates  the inpit and then saves the form answers if valid
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    else:
        form = UserCreationForm() # step 2: creating the form
    return render(request, 'users/register.html', { "form":form }) # step 3: form parameter creates the form and passes it to the register.html template
