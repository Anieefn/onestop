from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render,redirect
from .models import Register,Posts
from django.contrib.auth.hashers import make_password,check_password
# Create your views here.
#login page
def handle_login(request):
    if request.method == 'POST' :
            username = request.POST.get('username')
            password = request.POST.get('password')
            try:
                user = Register.objects.get(username=username)
                if check_password(password, user.password):
                    if user.role == "customer":
                         print("To home")
                         return redirect('home')
                    else:
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

#signup 
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

# view the stock of specific user
def stock_view(request, userid):
     p = get_object_or_404(Register, id=userid)
     error_message = None
     if request.method == 'POST':
          name = request.POST.get('name')
          bio = request.POST.get('bio')
          picture = request.POST.get('picture')
          price = request.POST.get('price')
          discount = request.POST.get('discount')
          catagery = request.POST.get('catagery')
          discount_price = int(price) - (int(price) * int(discount) / 100)
          post = Posts(name = name, bio = bio, picture = picture, price = price, discount = discount, catagery = catagery, discount_price = discount_price,userId = p)
          post.save()
     print(p)
     post = Posts.objects.filter(userId = p)
     if len(post) == 0:
          error_message = "No post available"
     print(post)
     return render(request, 'delivery/store.html',{'post':post, 'p':p, "error_message":error_message})

# updating stock indivially
def update_stock(request,userid, pid):
     print("into update")
     p = get_object_or_404(Register,id =userid)
     u = get_object_or_404(Posts, id=pid, userId = p)
     print(p)

     if request.method == 'POST':
            u.name = request.POST.get('name')
            u.bio = request.POST.get('bio')
            u.picture = request.POST.get('picture')
            u.price = request.POST.get('price')
            u.discount = request.POST.get('discount')
            u.catagery = request.POST.get('catagery')
            u.discount_price = float(u.price) - (float(u.price) * float(u.discount) / 100)
            print('saving')
            u.save()
            print("saved")
            return redirect('stock_view', userid=p.id)
     post = Posts.objects.filter(name = u )
     return render(request, 'delivery/update_stock.html', {'post': post,'u': u, 'p': p})

# delete post
def delete_user(request, pid, userid):
    p = get_object_or_404(Register, id=userid)
    u = get_object_or_404(Posts, id=pid, userId =p)
    print(u)  # Debugging output
    print(f"Deleting post with id {u} ")
    if request.method == 'POST':
         u.delete()
         return redirect('stock_view', userid=p.id)
    return render(request, 'delivery/delete_confirm.html', {'p': p, 'u': u})

#####################################  admin  #######################################################################

def home(request):
     print("In Home")
     post = Posts.objects.all()
     return render(request, 'delivery/home.html', {'post':post})