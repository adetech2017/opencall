from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib import messages
from applications.models import Application
from .forms import ApplicationForm

# Create your views here.


def newApplications(request):
    return render(request, "application.html")
    


def newForm(request):
    submitted = False
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            
            if Application.objects.filter(email = email).exists():
                messages.info(request, 'Email already exist')
                return ('new-form', {'form':form})

            elif Application.objects.filter(phone_number = phone_number).exists():
                messages.info(request, 'Phone number already exist')
                return redirect('new-form', {'form':form})
        
            else:
            
                form.save()
                messages.success(request, 'Application submitted successfuly')
                return ('new-form')
                #return HttpResponseRedirect('/new-form?submitted=True')
        
    else:
        form = ApplicationForm
        if 'submitted' in request.GET:
            submitted = True
            
    return render(request, 'testForm.html', {'form':form, 'submitted':submitted})





def createApplication(request):
    if request.method == 'POST':

        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        phone_number = request.POST['phone_number']
        email = request.POST['email']
        school_name = request.POST['school_name']
        school_address = request.POST['school_address']
        desc = request.POST['desc']
        school_id = request.FILES['school_id']
        video_file = request.FILES['video_file']
        
        if Application.objects.filter(email = email).exists():
            print('Email already exist')
            messages.info(request, 'Email already exist')
            return redirect('new-application')
        
        elif Application.objects.filter(phone_number = phone_number).exists():
            messages.info(request, 'Phone number already exist')
            return redirect('new-application')
        
        else:
            
            instance = Application.objects.create(f_name = f_name, l_name = l_name, phone_number = phone_number,
            email = email, school_name = school_name, school_address = school_address, desc = desc, school_id = school_id,
            video_file = video_file)
        
            instance.save();
            messages.success(request, 'Application submitted successfuly')
            return render(request, "/")
    else:
        messages.danger(request, 'Error submitting')
        return render(request, "application.html")

        