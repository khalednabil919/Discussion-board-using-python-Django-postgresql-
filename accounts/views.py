from dataclasses import fields
import imp
from tempfile import template
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.urls import reverse_lazy
from .forms import SignUp
from django.views.generic import UpdateView
# Create your views here.

def signup(request):
    form =SignUp()
    if request.method=='POST':
        form=SignUp(request.POST)
        if form.is_valid():
            user=form.save()
            auth_login(request,user)
            return redirect('index')

    return render(request,'signup.html',{'form':form})

class UserUpdateView(UpdateView):
    model=User
    fields=['first_name','last_name','email']
    template_name='my_account.html'
    success_url=reverse_lazy('my_account')

    #btrg3ly el user ely h3ml 3leh el edit.
    def get_object(self):
        return self.request.user