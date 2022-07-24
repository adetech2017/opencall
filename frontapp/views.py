import email
from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User, auth

# Create your views here.


def index(request):
    return render(request, "index.html")

def privacy(request):
    return render(request, "privacy.html")

def terms(request):
    return render(request, "terms.html")

def register(request):
    
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']
        
        if password == confirmPassword:
            if User.objects.filter(username = username).exists():
                messages.info(request, 'Username already exist')
                #print('Username already exist')
                return render(request, "sign-up.html")
                
            elif User.objects.filter(email = email).exists():
                messages.info(request, 'Email already exist')
                #print('Email already exist')
                return render(request, "sign-up.html")
                
            elif len(password) < 8:
                messages.info(request, 'Password is less than 8 chracter')
                #print('Password is less than 8 chracter')
                return render(request, "sign-up.html")
    
            else:
                user = User.objects.create(email=email, username=username, password=password)
        
                user.save();
                print('user created')
        
                return redirect('/')
        
        else:
            print('password not matching')
            
    return render(request, "sign-up.html")



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        
        else:
            messages.info(redirect, 'Invalid credentials')
            return render(request, "sign-up.html")
            
    return render(request, "log-in.html")