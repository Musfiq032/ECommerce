from django.shortcuts import render, redirect, HttpResponseRedirect
from Product.models import Product
from ECommerceAuth.models import *


# Create your views here.
def product_details_view(request, slug):

    try:

        prorduct_details = Product.objects.get(slug=slug)
        context = {'product_details': prorduct_details, }

        if request.GET.get('size'):
            size = request.GET.get('size')
            print(size)

            price = prorduct_details.get_product_price_by_size(size)
            print(price)
            context['selected_size'] = size
            context['updated_price'] = price

        return render(request, 'Product/product_details.html', context=context)
    except Exception as product:
        print(product)


def product_list_view(request):
    product_list = Product.objects.all()

    context = {
        'product_list': product_list
    }
    return render(request, 'Product/product_list.html', context)


