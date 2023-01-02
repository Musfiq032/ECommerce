from django.conf.urls.static import static
from django.conf import settings
from home.views import *
from django.urls import path

app_name = 'home'
urlpatterns = [
                  path('', home_view, name='Home'),
                  path('contact/', contact_view, name='Contact_Us'),
                  path('login/', login_view, name='Login'),
                  path('product/', shop_view, name='Product'),
                  

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
