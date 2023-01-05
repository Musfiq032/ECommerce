from django.shortcuts import render

from Product.models import *


# Create your views here.

def home_view(request):
    product = Product.objects.all()
    sub_category = SubCategory.objects.all()
    context = {
        'main_category': sub_category,
        'product': product
    }
    return render(request, 'index.html', context)


def contact_view(request):
    return render(request, 'contact.html')


def login_view(request):
    return render(request, 'Signup&Login/login.html')


def shop_view(request):
    return render(request, 'Product/product_list.html')
