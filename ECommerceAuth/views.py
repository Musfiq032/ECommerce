from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic import View

# to activate the user accounts

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import NoReverseMatch, reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError

# getting token from utils.py

from .utils import TokenGenerator, generate_token

# emails

from django.core.mail import send_mail, EmailMultiAlternatives, EmailMessage
from django.core.mail import BadHeaderError, send_mail
from django.core import mail
from django.conf import settings

# threading
import threading


#class EmailThread(threading.Thread):

   # def __int__(self, email_message):
    #    self.email_message = email_message
   ##     threading.Thread.__init__(self)

   # def run(self):
  #      self.email_message.send()


def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('register-email')
        password = request.POST.get('register-password')
        confirm_password = request.POST.get('register-password1')
        if password != confirm_password:
            messages.error(request, "Password do not Match,Please Try Again!")
            return redirect('/ecommerceauth/signup/')
        try:
            if User.objects.get(username=email):
                messages.warning(request, "Email Already Exists")
                return redirect('/ecommerceauth/signup/')
        except Exception as identifier:
            pass
        try:
            if User.objects.get(email=email):
                messages.warning(request, "Email Already Exists")
                return redirect('/signup')
        except Exception as identifier:
            pass
            # checks for error inputs
        user = User.objects.create_user(email, email, password)
        user.is_active = False
        user.save()
        email_subject = 'Activate Your Account'
        message = render_to_string('ecommerceauth/activate.html', {
            'user': user,
            'domain': '127.0.0.1:8000',
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': generate_token.make_token(user)

        })

        # email_message = message.EmailMessage(email_verify, message.settings.EMAIL_HOST_USER, [email] )

        email = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])

        email.send(fail_silently=True)
        # send_mail
        #       email_subject,
        #     message,
        #      user,
        #      ['info@ammch.edu.bd']
        # )
        messages.info(request, 'Activate your account by clicking on this link in your Email')

        messages.info(request, 'Thanks For Signing Up')
        # messages.info(request,"Signup Successful Please Login")
        return redirect('/ecommerceauth/login/')
    return render(request, 'Signup&Login/signup.html')


class activate_account_view(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None

        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.info(request, 'Acoount is Activated Successfully')
            return redirect('/ecommerceauth/login/')
        return render(request, 'ecommerceauth/activatefail.html')


def login_view(request):
    if request.method == 'POST':
        # get parameters
        loginusername = request.POST['singin-email']
        loginpassword = request.POST['singin-password']
        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.info(request, "Successfully Logged In")
            return redirect('/')

        else:
            messages.error(request, "Invalid Credentials")
            return redirect('/ecommerceauth/login/')

    return render(request, 'Signup&Login/login.html')


def logout_view(request):
    logout(request)
    messages.warning(request, "Logout Success")
    return render(request, 'Signup&Login/login.html')
