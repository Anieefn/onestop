from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render,redirect
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
                         print("to stock")
                         return redirect('stock_view', userid=user.id)
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
            print("saving")
            reg.save()
            print("saved")
            return render(request,'delivery/login.html')
    except IntegrityError as e:
             print(e)
             error_message = "An unexpected erroe occured. please try again"
             return render(request, 'delivery/singup.html', {"error_message" : error_message})
    return render(request, 'delivery/singup.html')

def stock_view(request, userid):
     print("in stock")
     p = get_object_or_404(Register, id=userid)
     print(p)
     if request.method == 'POST':
          name = request.POST.get('name')
          bio = request.POST.get('bio')
          picture = request.POST.get('picture')
          price = request.POST.get('price')
          discount = request.POST.get('discount')
          catagery = request.POST.get('catagery')
          print('saving data')
          discount_price = price - (price * discount / 100)
          print(discount_price)
          post = Posts(name = name, bio = bio, picture = picture, price = price, discount = discount, catagery = catagery, discount_price = discount_price,userId = p)
          post.save()
          print('saved')
     post = Posts.objects.filter(userId = p)
     print(post)
     return render(request, 'delivery/store.html',{'post':post, 'p':p})