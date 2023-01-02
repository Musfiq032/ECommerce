from django.shortcuts import render


# Create your views here.

def home_view(request):
    return render(request, 'index.html')


def contact_view(request):
    return render(request, 'contact.html')

    
def login_view(request):
    return render(request, 'Signup&Login/login.html')

def shop_view(request):
    return render(request, 'Product/product_list.html')
