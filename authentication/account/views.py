from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from account.models import AuthorForm
from django.contrib import messages
from .forms import SignUpForm, EditProfileForm, ChangeUserPasswordForm

# Create your views here.

def home(request):
    return render(request, 'account/home.html', {})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Welcome!"))
            return redirect('home')
        else:
            messages.success(request, ("Error Logging In - Please Try Again"))
            return redirect('login')
    else:
        return render(request, 'account/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ('You Have Been Logget Out.'))
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password= password)
            login(request, user)
            messages.success(request, ("You Have Registered!"))
            return redirect('home')
    else:
        form = SignUpForm()

    context = {'form': form}
    return  render(request, 'account/register.html', context)

def test(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, ("You Have Added An Author!"))
            return redirect('test')
    else:
        form = AuthorForm()
    context = {'form': form}
    return  render(request, 'account/test.html', context)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, ("You Have Successfully Edited Your Profile!"))
            return redirect('home')
    else:
        form = EditProfileForm(instance=request.user)

    context = {'form': form}
    return render(request, 'account/edit_profile.html', context)

def change_password(request):
    if request.method == 'POST':
        form = ChangeUserPasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, ("You Have Successfully Edited Your Password!"))
            return redirect('home')
    else:
        form = ChangeUserPasswordForm(user=request.user)

    context = {'form': form}
    return render(request, 'account/change_password.html', context)