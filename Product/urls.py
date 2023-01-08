from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from Product.views import *

app_name = 'Product'
urlpatterns = [
               path('<slug:slug>/', product_details_view, name='Product-Details'),
               path('product_list/', product_list_view, name='Product-List'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
