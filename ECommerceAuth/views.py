from django.http import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic import View
from .models import *

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

# Reset Password Generator

from django.contrib.auth.tokens import PasswordResetTokenGenerator

# threading
import threading


# class EmailThread(threading.Thread):
#
#     def __int__(self, email):
#         self.email_message = email
#         threading.Thread.__init__(self)
#
#     def run(self):
#         self.email_message.send()


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('register-username')
        email = request.POST.get('register-email')
        password = request.POST.get('register-password')
        confirm_password = request.POST.get('register-password1')
        if password != confirm_password:
            messages.error(request, "Password do not Match,Please Try Again!")
            return redirect('/ecommerceauth/signup/')
        try:
            if User.objects.get(username=username):
                messages.warning(request, "Username Already Exists")
                return redirect('/ecommerceauth/signup/')
        except Exception as identifier:
            pass
        try:
            if User.objects.get(email=email):
                messages.warning(request, "Email Already Exists")
                return redirect('/ecommerceauth/signup/')
        except Exception as identifier:
            pass
            # checks for error inputs
        user = User.objects.create_user(username, email, password)
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
        # EmailThread('email').start()
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


class reset_password_view(View):
    def get(self, request):
        return render(request, 'ecommerceauth/reset_email.html')

    def post(self, request):
        resetemail = request.POST.get('reset-email')
        user = User.objects.filter(email=resetemail)

        if user.exists():
            current_site = get_current_site(request)
            email_subject = '[Reset Your ECommerce Password]'
            message = render_to_string('ecommerceauth/reset_password.html', {
                'user': user,
                'domain': '127.0.0.1:8000',
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0])

            })

            email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [resetemail])
            email_message.send(fail_silently=False)
            messages.info(request, 'Password Reset Link Has been sent to your Email')

            return render(request, 'ecommerceauth/reset_email.html')


class set_new_password_view(View):

    def get(self, request, uidb64, token):

        context = {
            'uidb64': uidb64,
            'token': token
        }
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.warning(request, 'Password Reset Link is Invalid')
                return render(request, 'ecommerceauth/reset_email.html')

        except DjangoUnicodeDecodeError as identifier:
            pass

        return render(request, 'ecommerceauth/set-new-password.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
        }

        password = request.POST.get('reset-password')
        confirm_password = request.POST.get('reset-password1')
        if password != confirm_password:
            messages.error(request, "Password do not Match,Please Try Again!")
            return render(request, 'ecommerceauth/set-new-password.html', context)
        try:
            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password Reset Successfull')
            return redirect('/ecommerceauth/login/')
        except DjangoUnicodeDecodeError as identifier:
            messages.error(request, 'Something went wrong')
            return render(request, 'ecommerceauth/set-new-password.html', context)


def logout_view(request):
    logout(request)
    messages.warning(request, "Logout Success")
    return render(request, 'Signup&Login/login.html')


def add_to_cart(request, slug):

    print('""""""""""""""""""""""""""')
    print(request.user)
    print('""""""""""""""""""""""""""')
    variant = request.GET.get('variant')
    product = Product.objects.get(slug=slug)
    user = request.user

    cart , _ = Cart.objects.get_or_create(user=user, is_paid=False)

    cart_item = CartItem.objects.create(cart=cart, product=product)

    if variant:
        variant = request.GET.get('variant')
        size_variant = SizeVariant.objects.get(size_name=variant)
        cart_item.size_variant = size_variant
        cart_item.save()

    print(request.user.username)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def cart(request):
    context ={
        'cart_item': CartItem.objects.filter(cart__user=request.user),
        'cart': Cart.objects.filter(user= request.user, is_paid=False)
    }
    return render(request,'ecommerceauth/cart.html', context)

def remove_from_cart(request, uid):
    try:
        cart_item= CartItem.objects.get(id=uid)
        cart_item.delete()

    except Exception as e:
        print(e)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def add_to_wishlist(request, slug):

    print('""""""""""""""""""""""""""')
    print(request.user)
    print('""""""""""""""""""""""""""')
    variant = request.GET.get('variant')
    product = Product.objects.get(slug=slug)
    user = request.user

    wishlist , _ = Wishlist.objects.get_or_create(user=user, is_paid=False)

    wishlist_item = WishlistItem.objects.create(wishlist=wishlist, product=product)

    if variant:
        variant = request.GET.get('variant')
        size_variant = SizeVariant.objects.get(size_name=variant)
        wishlist_item.size_variant = size_variant
        wishlist_item.save()

    print(request.user.username)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def wishlist(request):
    context ={
        'wishlist': Wishlist.objects.filter(is_paid=False, user= request.user)
    }
    return render(request,'ecommerceauth/wishlist.html',context)