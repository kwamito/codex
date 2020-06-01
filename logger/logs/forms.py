from django import  forms
from django.contrib.auth.models import  User
from django.contrib.auth.forms import UserCreationForm
from .models import Log, Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        

class ProfileCreateForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        user = args('user')
        super(CreateForm,self).__init__(*args,**kwargs)
        self.fields['user'] = user

    class Meta:
        model = Profile
        fields = ['avatar','bio']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar','bio']