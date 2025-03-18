from django.db import IntegrityError
from django.shortcuts import render
from .models import Register,Posts
from django.contrib.auth.hashers import make_password,check_password
# Create your views here.

def handle_login(request):
    if request.method == 'POST' :
            username = request.POST.get('username')
            password = request.POST.get('password')
            try:
                user = Register.objects.get(username=username)
                if check_password(password, user.password):
                    if user.role == "customer":
                         return render(request,'delivery/home.html')
                    else:
                         return render(request, 'delivery/store.html')
                else:
                     error_message = "Invalid username or password"
                     return render(request, 'delivery/login.html', {"error_message":error_message})
            except Register.DoesNotExist as e:
                print(e)
                error_message = "user Not exists"
                return render(request, 'delivery/login.html', {"error_message":error_message})
    return render(request, 'delivery/login.html')

def singup(request):
     return render(request, 'delivery/singup.html')

def handle_singup(request):
    try :
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            email = request.POST.get('email')
            address = request.POST.get('address')
            phonenumber = request.POST.get('phonenumber')
            role = request.POST.get('role')
            if Register.objects.filter(email=email).exists() or Register.objects.filter(phonenumber=phonenumber).exists():
                error_message = "Email or phone number already exists"
                return render(request, 'delivery/singup.html', {"error_message": error_message})
            hashed_password = make_password(password)
           # print("password hassed", hashed_password)
            reg = Register(username = username, password = hashed_password, email = email, address = address, phonenumber = phonenumber, role = role)
            reg.save()
            return render(request,'delivery/login.html')
    except IntegrityError as e:
             print(e)
             error_message = "An unexpected erroe occured. please try again"
             return render(request, 'delivery/singup.html', {"error_message" : error_message})
    return render(request, 'delivery/singup.html')

def add_post(request):
     if request.method == 'POST':
          name = request.POST.get('name')
          bio = request.POST.get('bio')
          img = request.POST.get('img')
          price = request.POST.get('price')
          catagery = request.POST.get('catagery')
          discount = request.POST.get('discount')
          print("Data at backenf")
          post = Posts(name = name, bio = bio, img = img, price = price, catagery = catagery, discount = discount)
          post.save()
          print("Data saved")
          posts = Posts.objects.all()
          print("Data saved")
          for post in posts:
             post.discounted_price = post.get_discount_price()  # Attach discounted price to each post object
          print("discount price calculated")
     return render(request, 'delivery/store.html', {"posts":posts})