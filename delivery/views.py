from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, render,redirect
import razorpay
from .models import Register,Posts,Cart,Otp
from django.contrib.auth.hashers import make_password,check_password
from django.conf import settings
from django.core.mail import send_mail
import random
from django.utils.timezone import now


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
                         return redirect('home', userid=user.id)
                         
                    else:
                         return redirect('stock_view', userid=user.id)
                else:
                     error_message = "Invalid username or password"
                     return render(request, 'delivery/login.html', {"error_message":error_message})
            except Register.DoesNotExist as e:
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
            reg = Register(username = username, password = hashed_password, email = email, address = address, phonenumber = phonenumber, role = role)
            reg.save()
            return render(request,'delivery/login.html')
    except IntegrityError as e:
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
     post = Posts.objects.filter(userId = p)
     if len(post) == 0:
          error_message = "No post available"
     return render(request, 'delivery/store.html',{'post':post, 'p':p, "error_message":error_message})

# updating stock indivially
 
def update_stock(request,userid, pid):
     p = get_object_or_404(Register,id =userid)
     u = get_object_or_404(Posts, id=pid, userId = p)
     if request.method == 'POST':
            u.name = request.POST.get('name')
            u.bio = request.POST.get('bio')
            u.picture = request.POST.get('picture')
            u.price = request.POST.get('price')
            u.discount = request.POST.get('discount')
            u.catagery = request.POST.get('catagery')
            u.discount_price = float(u.price) - (float(u.price) * float(u.discount) / 100)
            u.save()
            return redirect('stock_view', userid=p.id)
     post = Posts.objects.filter(name = u )
     return render(request, 'delivery/update_stock.html', {'post': post,'u': u, 'p': p})

# delete post
 
def delete_user(request, pid, userid):
    p = get_object_or_404(Register, id=userid)
    u = get_object_or_404(Posts, id=pid, userId =p)
    if request.method == 'POST':
         u.delete()
         return redirect('stock_view', userid=p.id)
    return render(request, 'delivery/delete_confirm.html', {'p': p, 'u': u})

#####################################  admin  #######################################################################
 
def home(request, userid, category_name = None):
     if category_name:
          post = Posts.objects.filter(catagery = category_name)
     else:
          post = Posts.objects.all()
     u = Register.objects.filter(id = userid).first()
     c = Posts.objects.values_list('catagery', flat=True).distinct()
     return render(request, 'delivery/home.html', {'post':post , 'u':u,'c':c, 'category_name':category_name})
 
def update_cus(request, userid) :
      u = get_object_or_404(Register, id = userid)
      p = Register.objects.filter(id = userid).first()
      if request.method == 'POST':
           u.username = request.POST.get('username')
           u.email = request.POST.get('email')
           u.address = request.POST.get('address')
           u. phonenumber = request.POST.get('phonenumber')
           u.save()
           return redirect('home',p.id)
      details = Register.objects.filter(id = userid).filter()
      return render(request,'delivery/update_cus.html',{"details":details})

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
     p = get_object_or_404(Register, id=userid)
     cart = Cart.objects.filter(customer = p).first()
     cart_items= cart.items.all() if cart else []
     total_price = cart.total_price() if cart else 0
     if total_price == 0:
          return render(request,'delivery/checkout.html',{'error':'your cart is empty!'})
     try:
       client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
       order_data = {
          'amount':int(total_price * 100),
          'currency':'INR',
          'payment_capture':'1',
     }
       order = client.order.create(data=order_data)
     except Exception as e:
          print(e)
          return render(request, 'delivery/checkout.html', {'error': f"Error creating order: {str(e)}"})

     return render(request, 'delivery/checkout.html',{
          'p' :p,
          'cart_items':cart_items,
          'total_price':total_price,
          'razorpay_key_id':settings.RAZORPAY_KEY_ID,
          'order_id':order['id'],
          'amount':total_price,
     })

def orderss(request, userid):
    p = get_object_or_404(Register, id=userid)
    cart = Cart.objects.filter(customer=p).first()

    if cart:
        cart_items = cart.items.all()
        total_price = cart.total_price()

        # Send email confirmation
        subject = "Your Order Summary"
        message = f"Hello {p.username},\n\nHere are your order details:\n" + \
                  "\n".join([f"{item.name})" for item in cart_items]) + \
                  f"\n\nTotal Price: {total_price}\n\nThank you for your order!"
        recipient = p.email

        send_mail(
            subject, message, 'anieefn@gmail.com', [recipient], fail_silently=False,
        )

        # Clear the cart
        cart.items.all().delete()

    return render(request, 'delivery/orders.html', {
        'p': p,
        'cart_items': cart_items,
        'total_price': total_price,
    })
################################################## user ###################################################

def otp(request):

     if request.method == 'POST':
          email = request.POST.get('email')
          try:
               user = Register.objects.get(email=email)
               print(user)
               print(user.id)
               print(email)
               otp = str(random.randint(100000, 999999))
               otp_obj,created = Otp.objects.update_or_create(user = user,
                    defaults={'otp':otp, 'otp_created_at':now()})
               subject = "Your OTP for Password Reset"
               message = f"Hello {user.username},\n\nYour OTP for password reset is: {otp}.\n\nThis OTP is valid for 3 minutes."
               from_email = "anieefn@gmail.com"
               recipient = user.email
               send_mail(subject,message,from_email,[recipient], fail_silently=False)
               return render(request, 'delivery/enter_otp.html',{"user_id":user.id, "email":email})
          except Exception as e:
                print(e)
                return render(request, "delivery/send_otp.html", {"error": "Email not registered."})
     return render(request, "delivery/send_otp.html")

def verify_otp_and_reset_password(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        otp = request.POST.get("otp")
        new_password = request.POST.get("new_password")

        user = Register.objects.get(id=user_id)
        otp_obj = Otp.objects.filter(user=user).first()

        if otp_obj and otp_obj.otp == otp:
            if otp_obj.is_otp_vaild():
                # Update the user's password
                user.password = make_password(new_password)
                user.save()
                # Delete the OTP object for security
                otp_obj.delete()

                return render(request, "delivery/login.html", {"success": "Password updated successfully. Please log in."})
            else:
                return render(request, "delivery/enter_otp.html", {"user_id": user.id, "email": user.email, "error": "OTP expired."})
        else:
            return render(request, "delivery/enter_otp.html", {"user_id": user.id, "email": user.email, "error": "Invalid OTP."})
    return redirect("send_otp")

####################################### order conformation and rest password ########################################################################################


