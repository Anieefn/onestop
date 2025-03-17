from django.db import IntegrityError
from django.shortcuts import render
from .models import Register
# Create your views here.

def handle_login(request):
    if request.method == 'POST' :
            username = request.POST.get('username')
            password = request.POST.get('password')
            try:
                user = Register.objects.get(username=username, password = password)
                return render(request, 'delivery/store.html')
            except Register.DoesNotExist:
                error_message = "Invalid username or password"
                return render(request, 'delivery/login.html', {"error_message":error_message})
    else:
           return render(request, 'delivery/login.html')

def handle_singup(request):
     try:
          if request.method == 'POST':
               username = request.POST.get('username')
               password = request.POST.get('password')
               email = request.POST.get('email')
               address = request.POST.get('address')
               phonenumber = request.POST.get('phonenumber')
               user = Register(username = username, password = password, email = email, address = address, phonenumber = phonenumber, role = role)
               user.save()
               return render(request, 'delivery/store.html')
     except IntegrityError:
          error_message = "Email or phone Number already exists"
          return render(request, 'delivery/singup.html', {"error_message":error_message})