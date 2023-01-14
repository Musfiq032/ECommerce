from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from Product.models import Product
from .models import *


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


def product_list_view(request,slug):

    if(Category.objects.filter(slug=slug, status=0)):
        products_filter= Product.objects.filter(category__slug=slug)
        category_filter= Category.objects.filter(slug=slug).first()
        brand_filter = Brand.objects.filter(product__category__slug__icontains=slug)
        context = {
            'main_category': category_filter,
            'product': products_filter,
            'brand': brand_filter,
        }
        return render(request, 'Product/product_list.html', context)
    else:
        messages.warning(request,"No category Found")
        return redirect('Product:Product-List')




