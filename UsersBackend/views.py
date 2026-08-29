from django.shortcuts import render
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
        else:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password
                )
                user.save()
                messages.success(request, 'Account created successfully. Please log in.')
                return redirect('login')
    return render(request, 'register.html')

def logout_view(request):
    auth.logout(request)
    return redirect('index')

def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})