from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignupForm
from django.contrib.auth.models import User

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Register success")
            return redirect('home')
    else:
        form = SignupForm()
        return render(request, 'register.html', {'form': form})
    
    return render(request, 'register.html', {'form': form})


def home_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        checkUser = User.objects.filter(username=username)
        if not checkUser:
            messages.success(request, "User not found")
            return redirect('home')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login success")
            return redirect('home')
        else:
            messages.success(request, "Some error occurred")
            return redirect('home')
    else:
        return render(request, 'home.html', {})



def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('home')