from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.views.generic import DetailView, CreateView, DeleteView, ListView
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .models import Yatru, Relationship,Message
from .forms import YatruModelForm,MessageModelForm

#Authentication part
def signupuser(request):
    if request.method == 'GET':
        return render(request, 'app/Signup.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('app:home')
            except IntegrityError:
                return render(request, 'app/Signup.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'app/Signup.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def loginuser(request):
        if request.method == 'GET':
            return render(request, 'app/Login.html', {'form':AuthenticationForm()})
        else:
            user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
            if user is None:
                return render(request, 'app/Login.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
            else:
                login(request, user)
                return redirect('app:my-profile-view')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('app:home')

#App_apart

def home(request): 
    return render(request, 'app/home.html')

def my_profile_view(request):
    profile = Yatru.objects.get(user=request.user)
    form = YatruModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True
    else:
        profile = Yatru.objects.get(user=request.user)
        form = YatruModelForm(request.POST or None, request.FILES or None, instance=profile)
        confirm = False
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                confirm = True
        return render(request, 'app/create.html',{'form': form})

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }

    return render(request, 'app/profile.html', context)
 
 #This is for the messaging part

# def new_messages(request):
#     userName= request.POST[]
#     return render(request, 'app/profile.html')

def new_messages(request):
    form= MessageModelForm()
    if request.method == "POST":
        form= MessageModelForm(request.POST)
        if form.is_valid():
            form.save()
    context={
        'form':form
    }
    return render(request,'app/write_message.html',context)

def view_messages(request):
    messages = Message.objects.filter(receiver=request.user)
    unreadMessages = Message.objects.filter(
        receiver=request.user).filter(status=False).count()
    userIn = request.user
    
    context = {
        'msgs': messages,
        'userIn': userIn,
        'unreadmsgs': unreadMessages
    }

    return render(request, "app/message.html", context)
    
def delete_messages(request):
    pass
