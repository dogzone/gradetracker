from django import forms
from django.contrib.auth.models import User
from GradeTracker.models import Course, Graded_Activities
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.core.validators import MaxValueValidator, MinValueValidator

class courseAdd(ModelForm):
    class Meta:
        model = Course
        exclude = ('student', )

class activityEdit( ModelForm):
    class Meta:
        model = Graded_Activities
        exclude = ('course', )

class activityAdd(forms.Form):
    activityName = forms.CharField(max_length=200)
    activityWeight = forms.FloatField(validators = [MinValueValidator(0.00), MaxValueValidator(1.00)])

class subactivityAdd(forms.Form):
    subactivityName = forms.CharField(max_length=200)
    subactivityWeight = forms.FloatField(validators = [MinValueValidator(0.00), MaxValueValidator(1.00)])

#UserCreationForm already created in auth directory
class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    institution = forms.CharField(required=True)

    #embedded class that holds extra information that isn't a form
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 
        'last_name', 'institution', 'password1', 'password2')
    
    #Overriding method from UserCreationForm
    def save(self, commit=True):
        #commit = False because haven't gotten all info yet
        user = super(MyRegistrationForm, self).save(commit=False)

        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.institution = self.cleaned_data['institution']

        
        if commit:
            user.save()

        return user
