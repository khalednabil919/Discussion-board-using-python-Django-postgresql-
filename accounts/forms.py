from dataclasses import field
import email
from pyexpat import model
from re import L
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class SignUp(UserCreationForm):
    email=forms.CharField(max_length=50,required=True,widget=forms.EmailInput)
    class Meta:
        model=User
        fields=['username','password1','password2','email']