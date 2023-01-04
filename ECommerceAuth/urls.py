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



              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
