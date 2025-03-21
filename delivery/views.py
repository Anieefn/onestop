from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render,redirect
import razorpay
from .models import Register,Posts,Cart
from django.contrib.auth.hashers import make_password,check_password
from django.conf import settings

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
                         print(user.id)
                         return redirect('home', userid=user.id)
                         
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

def home(request, userid, category_name = None):
     print("In Home")
     if category_name:
          post = Posts.objects.filter(catagery = category_name)
     else:
          post = Posts.objects.all()
     u = Register.objects.filter(id = userid).first()
     c = Posts.objects.values_list('catagery', flat=True).distinct()
     print(u)
     return render(request, 'delivery/home.html', {'post':post , 'u':u,'c':c, 'category_name':category_name})

def update_cus(request, userid) :
      print("In update")
      u = get_object_or_404(Register, id = userid)
      p = Register.objects.filter(id = userid).first()
      print(p)
      print(u)
      if request.method == 'POST':
           u.username = request.POST.get('username')
           u.email = request.POST.get('email')
           u.address = request.POST.get('address')
           u.phonenumber = request.POST.get('phonenumber')
           print("saving")
           u.save()
           print("Saved")
           print("to home")
           return redirect('home',p)
      print("to profile")
      details = Register.objects.filter(username=u.username)
      return render(request,'delivery/update_cus.html',{"details":details, 'u':u})

def add_to_cart(request, item_id, userid):
     customer = get_object_or_404(Register, id = userid)
     item = get_object_or_404(Posts, id=item_id)
     print(customer)
     print(item)
     cart,created = Cart.objects.get_or_create(customer = customer)

     cart.items.add(item)
     customer.saved_posts.add(item)
     messages.success(request, f"{item.name} added to your cart!")
     return redirect('home', userid = customer.id)

def orders(request, userid):
     p = get_object_or_404(Register, id = userid)
     print("in order",p)
     print(type(p))
     o = Cart.objects.filter(customer= p).first()
     print(o)
     item = o.items.all() if o else []
     total_price = o.total_price() if o else 0
     return render(request,'delivery/cart.html',{'item':item, 'total_price':total_price, 'p':p})

def checkout(request, userid):
     p = get_object_or_404(Register, id = userid)
     cart = Cart.objects.filter(customer = p).first()
     cart_items= cart.items.all() if cart else []
     total_price = cart.total_price() if cart else 0

     if total_price == 0:
          return render(request,'delivery/checkout.html',{'error':'your cart is empty!'})
     
     client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

     order_data = {
          'amount':int(total_price * 100),
          'currency':'INR',
          'payment_capture':'1'
     }

     order = client.order.create(data = order_data)

     return render(request, 'delivery/checkout.html',{
          'p' :p.id,
          'cart_items':cart_items,
          'total_price':total_price,
          'razorpay_key_id':settings.RAZORPAY_KEY_ID,
          'order_id':order['id'],
          'amount':total_price
     })
          
     