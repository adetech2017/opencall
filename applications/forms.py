from dataclasses import fields
#from tkinter import Widget
from django import forms
from django.forms import ModelForm, Textarea
from .models import Application



# create application form
class ApplicationsForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            'matric_number', 'first_name', 'last_name', 'phone_number', 'date_of_birth',
            'email', 'aim_objective', 'school_name', 'school_address','school_id', 'video_file',
            'photo', 'project_source', 'desc', 'project_desc', 'project_benefit'
        ]
        
        labels = {
            'matric_number': 'Matric Number',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'phone_number': 'Phone Number',
            # 'photo': 'Upload passport photograph ',
            # 'video_file': 'Upload project video ( max size 5mins)',
            # 'matric_number': 'Matric Number',
            # 'matric_number': 'Matric Number',
            # 'matric_number': 'Matric Number',
            # 'matric_number': 'Matric Number',
            # 'matric_number': 'Matric Number',
            # 'matric_number': 'Matric Number'
        }
        
        
        Widgets = {
            'matric_number': forms.TextInput(attrs={'size': 100, 'title': 'Your name'}),
        }
    
    
    
class OrderForm(ModelForm):
    class Meta:
        model = Application
        fields = ['matric_number', 'first_name', 'last_name', 'phone_number', 'date_of_birth', 'desc']
        
        Widgets = {
            'matric_number': forms.TextInput(attrs={'size': 100, 'title': 'Your name'}),
            'desc': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Text goes here', 'rows': '4', 'cols': '10'})
        }
        

CHOICES = (('no','No'),('yes','Yes'))

class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        
        fields = ['matric_number', 'first_name', 'last_name', 'phone_number', 'date_of_birth',
            'email', 'aim_objective', 'school_name', 'school_address','school_id', 'video_file',
            'photo', 'project_source', 'project_desc', 'project_benefit', 'desc']
        
        widgets = {
            'school_address': forms.Textarea(attrs={'rows':2, 'cols':10}),
            'project_desc': forms.Textarea(attrs={'rows':4, 'cols':15}),
            'project_benefit': forms.Textarea(attrs={'rows':4, 'cols':15}),
            'date_of_birth': forms.DateInput(format=('%Y-%m-%d'),attrs={'class': 'form-control', 'placeholder': 'Select a date','type': 'date'}),
            'project_source': forms.RadioSelect(choices=CHOICES),
            'desc': forms.Textarea(attrs={'rows':4, 'cols':20}),
        }
        
        labels = {
            'matric_number': 'Matric Number',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'phone_number': 'Phone Number',
            'aim_objective': 'Project Aim / Objectives',
            'school_id': 'Upload school identity card',
            'video_file': 'Upload project video ( max size 5mins)',
            'photo': 'Upload passport photograph',
            'project_source': 'Is material locally sourced? ',
            'project_desc': 'Project Description (300 characters)',
            'project_benefit': 'Project Benefit',
            'desc': 'Additional details (optional)'
        }
        
    
        def clean(self):
            super(ApplicationForm, self).clean()
            
            matric_number = self.changed_data.get('matric_number')
            phone_number = self.changed_data.get('phone_number')
            first_name = self.changed_data.get('first_name')
            
            if len(matric_number) < 9:
                self._errors['matric_number'] = self.error_class(['A minimum of 5 chracters is required'])
            
            
            return self.cleaned_data