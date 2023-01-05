from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from Product import views

app_name = 'Product'
urlpatterns = [
               path('<slug:slug>/', views.product_details_view, name='Product-Details'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
