from .forms import UserRegsiterForm,UserUpdateForm,ProfileUpdateForm
from django.db import models
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.views.generic import ListView,DetailView,UpdateView,CreateView,DeleteView

def register(request):
    if request.method == 'POST':
        form = UserRegsiterForm(request.POST)
        if form.is_valid():
            old_email = User.objects.filter(email=form.cleaned_data.get('email')).exists()
            if old_email :
                messages.error(request,'The email is already used')
                return render(request,'users/register.html',{'form':form})
            form.save()
            messages.success(request,'Registeration Completed',extra_tags='success')
            return redirect('login')
    else:
        form = UserRegsiterForm() 
    return render(request,'users/register.html',{'form':form})

@login_required
def profile(request):
    if(request.method=='POST'):
        user_email = request.user.email
        user_form = UserUpdateForm(request.POST,instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            new_email = user_form.cleaned_data['email']
            if user_email != new_email and User.objects.filter(email=new_email).exists():
                messages.error(request,"This email is already used")
                return redirect(profile)                                                                  
            else:
                user_form.save()
                profile_form.save()                
                messages.success(request,"Update completed")
                return redirect(profile)
        else:
            messages.error(request,"This username is already used")
            return redirect(profile)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request,'users/profile.html',{'user_form':user_form,
                                                                'profile_form':profile_form})
