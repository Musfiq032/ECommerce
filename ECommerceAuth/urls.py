from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from ECommerceAuth import views


app_name = 'ECommerceAuth'
urlpatterns = [
               path('signup/', views.signup_view, name='Signup'),
               path('login/', views.login_view, name='login'),
               path('logout/', views.logout_view, name='logout'),
               path('activate/<uidb64>/<token>', views.activate_account_view.as_view(), name='activate'),
               path('reset-password/', views.reset_password_view.as_view(), name='ResetYourPassword'),
               path('set-new-password/<uidb64>/<token>', views.set_new_password_view.as_view(), name='Set-new-password'),
               path('cart/', views.cart, name='cart'),
               path('wishlist/', views.wishlist, name='Wishlist'),
               path('add_to_cart/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
               path('remove_cart/<uid>', views.remove_from_cart, name='remove_from_cart'),
               path('add_to_wishlist/<slug:slug>/', views.add_to_wishlist, name='add_to_wishlist'),
               path('remove_coupon/<remove_coupon_uid>/', views.remove_coupon, name='remove_coupon'),
               path('checkout/', views.checkout, name='checkout')




              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
