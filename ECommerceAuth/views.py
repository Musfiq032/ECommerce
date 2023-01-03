from email import message
from lib2to3.pgen2.tokenize import generate_tokens
from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import NoReverseMatch, reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.core.mail import send_mail, EmailMultiAlternatives, BadHeaderError, EmailMessage
from django.core import mail
from django.conf import settings
from .utils import TokenGenerator



# Create your views here.

def signup_view(request):
    if request.method == 'POST':
        email=request.POST.get('register-email')
        password=request.POST.get('register-password')
        confirm_password=request.POST.get('register-password1')
        if password != confirm_password:

            messages.error(request,"Password do not Match,Please Try Again!")
            return redirect('/ecommerceauth/signup/')
        try:
            if User.objects.get(username=email):
                messages.warning(request,"Email Already Exists")
                return redirect('/ecommerceauth/signup/')
        except Exception as identifier:            
            pass 
        try:
            if User.objects.get(email=email):
                messages.warning(request,"Email Already Exists")
                return redirect('/signup')
        except Exception as identifier:
            pass        
        # checks for error inputs
        user=User.objects.create_user(email,email,password)
        user.is_active=False
        user.save()
        current_site= get_current_site(request)
        email_verify= 'Activate Your Account'
        message=  render_to_string('ecommerceauth/activate.html', {
            'user': user,
            'domain': 'http://127.0.0.1:8000/',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)

        })

        email_message= message.EmailMessage(email_verify, message.settings.EMAIL_HOST_USER,[email],)
        EmailThread(email_message).start()
        message.info(request, 'Activate your account by clicking on this link')

        messages.info(request,'Thanks For Signing Up')
        # messages.info(request,"Signup Successful Please Login")
        return redirect('/ecommerceauth/login/')    
    return render(request, 'Signup&Login/signup.html')      

def login_view(request):
    if request.method == 'POST':
        # get parameters
        loginusername=request.POST['singin-email']
        loginpassword=request.POST['singin-password']
        user=authenticate(username=loginusername,password=loginpassword)
       
        if user is not None:
            login(request,user)
            messages.info(request,"Successfully Logged In")
            return redirect('/')

        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/ecommerceauth/login/')    

        
    return render(request, 'Signup&Login/login.html')


def logout_view(request):
    logout(request)
    messages.warning(request,"Logout Success")
    return render(request,'Signup&Login/login.html')
