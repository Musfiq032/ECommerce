from django.contrib import admin
from ECommerceAuth.models import *

# Register your models here.

admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Wishlist)
admin.site.register(WishlistItem)


