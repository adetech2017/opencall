from readline import get_current_history_length
from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .token import account_activation_token
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import User 



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
                user = User.objects.create(email = email, username = username, password = password)
                user.is_active = False
                user.save();
                
                # to get the domain of the current site  
                # current_site = get_current_site(request)  
                # mail_subject = 'Activate your LASG-Admin Account'  
                # message = render_to_string('acc_active_email.html', {  
                #     'user': user,
                #     'domain': current_site.domain,
                #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                #     'token': account_activation_token.make_token(user),  
                # })
                # user.email_user(mail_subject, message, html_message=message)
                # to_email = request.POST['email']  
                # email = EmailMessage(  
                #     mail_subject, message, to=[to_email]
                # )  
                # email.send()
                #return HttpResponse('Please confirm your email address to complete the registration')
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
            messages.info(request, 'Invalid credentials')
            return render(request, "log-in.html")
            
    return render(request, "log-in.html")


def logout(request):
    auth.logout(request)
    return redirect("/")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')