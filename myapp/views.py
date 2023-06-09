from django.shortcuts import render
from .forms import UserRegsitrationForm,UpdateUserForm,ProfileUpdateForm
from .models import ImageUploader, Cart
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
# Create your views here.

@login_required
def addtocart(request):
    image = request.GET.get('image')
    image_id = request.GET.get('image_id')
    image_name = request.GET.get('image_name')
    #print(image_id, image_name)
    cart_item = Cart(image=image, image_id=image_id, image_name=image_name, user=request.user)
    cart_item.save()
    return render(request, 'profile.html')

@login_required
def viewcart(request):
    items = Cart.objects.filter(user=request.user)
    return render(request, 'viewcart.html', {'items':items}) 

def home(request):
        if request.method == "POST" and 'upload' in request.POST:
                img_name = 'img_name' in request.POST and request.POST['img_name']
                img = 'img' in request.FILES and request.FILES['img']
                u_profile = 'u_profile' in request.POST and request.POST['u_profile']


                img_uploader = ImageUploader(image_name = img_name,
                                                image = img,
                                                user=request.user,
                                                user_profile = u_profile,
                                                date=datetime.now())
                img_uploader.save()
                messages.success(request,'Your Image Uploaded Successfully !!')


        images = ImageUploader.objects.all()
        return render(request,'home.html',{'images':images})
    
        
def signup(request):
        if request.method == "POST":
                fm = UserRegsitrationForm(request.POST)
                if fm.is_valid():
                        fm.save()
                        messages.success(request,'Signup Done !!')

        else:
                fm  = UserRegsitrationForm()

        context = {'fm':fm}
        return render(request,'signup.html',context)

@login_required
def profile(request):

        if request.method == "POST":
                u_form = UpdateUserForm(instance = request.user,data=request.POST)
                p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
                if u_form.is_valid() and p_form.is_valid():
                    u_form.save()
                    p_form.save()
                    messages.success(request, f'Your Profile has been updated!')


        
        
        else:
                u_form = UpdateUserForm(instance = request.user)
                p_form = ProfileUpdateForm(instance = request.user.profile)

        return render(request,'profile.html',{'u_form':u_form,'p_form':p_form})


def user_profile(request,user):

        users = User.objects.get(username=user)
        image = ImageUploader.objects.filter(user=user)


        return render(request,'user-profile.html',{'users':users,'image':image})
    
def search(request):
      title = request.POST.get('title', False)
      #obj = ImageUploader.objects.all().filter(image_name=title)
      #context = {'obj':obj, 'title': title}
      #print(context)
      #images = ImageUploader.objects.all()
      images = ImageUploader.objects.all().filter(image_name=title)
      return render(request,'search.html',{'images':images})
  

def makepayment(request):
    if request.method == "POST":
        name = request.POST.get('name')
        amount =int(request.POST.get('amount'))*100
        email=request.POST.get('email')
        client = razorpay.Client(auth =("rzp_test_ifqXZb84qSL1CP" , "IwSyyaBvXh300nlqM0kqb0ow"))
        payment = client.order.create({'amount':amount, 'currency':'INR',
                              'payment_capture':'1' })
        
        #info = donate(name = name , email = email , amount =amount , order_id = payment['id'])
        #info.save()
        
        return render(request, 'index.html' ,{'payment':payment})
    return render(request, 'index.html')

@csrf_exempt
def success(request):
    if request.method == "POST":
        a = request.POST
        order_id = ""
        for key , val in a.items():
            if key == "razorpay_order_id":
                order_id = val
                break
    
        #user = donate.objects.filter(order_id = order_id).first()
        #user.paid = True
        #user.save()
        
       

    return render(request, "success.html")
