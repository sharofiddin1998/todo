from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as loginUser
from .forms import *
from .forms import *
from .models import *

# Create your views here.
def index(request):
    todos=Todo.objects.all()
    form=TodoForm()
    return render(request, 'index.html', {'form':form, 'todos':todos})

def login(request):
    if request.method=='GET':
        form=AuthenticationForm()
        context={'form':form}
        return render(request, 'login.html', context=context)

    else:
        form=AuthenticationForm(data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(request, username=username, password=password)
            if user is not None:
                loginUser(request,user)
                return redirect('index')
            
        else:
            context={'form':form}
            return render(request, 'login.html', context=context)






def register(request):
    if request.method=='GET':
        form=UserCreationForm()
        return render(request, 'register.html', {'form':form})  
    else:
        print(request.POST)
        form=UserCreationForm(request.POST)
        if form.is_valid():
           user=form.save()
           print(user)
           if user is not None:
               return redirect('login')

        else:
            return render(request, 'register.html', {'form':form})  

def add_todo(request):
    if request.user.is_authenticated:
        user=request.user
        print(user)
        form=TodoForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            todo=form.save(commit=False)
            todo.user=user
            todo.save()
            print(todo)
            return redirect('index')
        else:
            return render(request, 'index.html', {'form':form})

            

