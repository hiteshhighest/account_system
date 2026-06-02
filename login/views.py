from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import logout

# Create your views here.
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return render(request, 'login/signup.html', {'error': 'Username already exists'})
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1
                )
                user.first_name = fname
                user.last_name = lname
                user.save()

            return redirect('login')
        else:
            return render(request, 'login/signup.html', {'error': 'Password do not match'})
    
    return render(request, 'login/signup.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(home)
        else:
            return render(request, 'login/login.html', {'error': 'Invalid username or password'})
            
    return render(request, 'login/login.html')

def home(request):
    if request.user.is_authenticated:
        return render(request, 'login/index.html', {'user': request.user.first_name})
    else:
        return redirect('login')
    
def logout_view(request):
    logout(request)
    return redirect('login')