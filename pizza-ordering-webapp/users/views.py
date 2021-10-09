from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

# Create your views here.

def index(request):
    if request.method == "GET":
        return render(request, "register.html", context=None)
    username = request.POST["user"]
    email = request.POST["email"]
    password = request.POST["pwd"]
    rpassword = request.POST["rpwd"]
    if password != rpassword:
        return HttpResponse("Password match Failed")
    user = User.objects.create_user(username, email, password)
    return render(request, "login.html", context=None)

def login_view(request):
    if request.method == "POST":
       username = request.POST["user"]
       password = request.POST["pwd"]
       user = authenticate(request, username=username, password=password)
       login(request, user)
       return redirect("/orders/")
    else:
        return render(request, "login.html")

def logout_view(request):
    logout(request)
    return render(request, "login.html")
