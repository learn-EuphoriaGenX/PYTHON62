from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def sign_in(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password :
            messages.error(request, "all fields are required!")
            return redirect('sign-up')
        else:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login Successfull!")
                return redirect('overview')
            else:
                messages.error(request, "Invalid credentials!")
                return redirect('sign-in')
            
    return render(request, 'signin.html')

def sign_up(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not username or not password  or not email :
            messages.error(request, "all fields are required!")
            return redirect('sign-up')
        else:
            is_user = User.objects.filter(username = username).exists()
            if is_user:
                messages.error(request, "User already Exists!")
                return redirect('sign-up')
            else:
                new_user = User.objects.create_user(
                    username = username,
                    email = email,
                    password = password,
                )
                new_user.save()
                messages.success(request, "User registered successfully!")
                return redirect('sign-in')
    return render(request, 'signup.html')

def logout_user(request):
    logout(request)
    messages.success(request, "User logout successfully!")
    return redirect('sign-in')
    