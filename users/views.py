from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('users:login'))
    return render(request,'users/user.html')
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse('users:index'))
        else:
            return render(request,'users/login.html',{
                'message' : 'Invalid Credentails.'
            })
    return render(request,'users/login.html')

def logout_view(request):
    logout(request)
    return render(request,'users/login.html',{
        'message' : 'Logged Out.'
    })

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        cnf_password = request.POST.get('cnf_password')
        if User.objects.filter(username=username).exists():
            return render(request,'users/register.html',{
                'message' : 'Username already taken'
            })
        elif password != cnf_password:
            return render(request,'users/register.html',{
            'message' : 'password and confirm password should be same'
        })
        elif not username or not password or not cnf_password:
            return render(request, 'users/register.html', {
            'message': 'All fields are required'
        })
        else:
            user = User.objects.create_user(username=username,password=password)
            user.save()
            return HttpResponseRedirect(reverse('users:login'))
    return render(request,'users/register.html')
