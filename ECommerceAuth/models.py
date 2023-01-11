from django.db import models
# from django.contrib.auth.models import User
from Product.models import *
from django.contrib.auth import get_user_model  # current user model

# Create your models here.

User = get_user_model()


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name="user_profile")
    name = models.CharField(max_length=250, null=True, blank=True, default="")
    address = models.CharField(max_length=250, blank=True)
    phone = models.CharField(max_length=250, null=True, blank=True)
    profile_photo = models.ImageField(upload_to='User Profile Photo', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_cart_count(self):
        return CartItem.objects.filter(cart__is_paid=False, cart__user=self.user).count()

    def get_wishlist_count(self):
        return WishlistItem.objects.filter(wishlist__is_paid=False, wishlist__user=self.user).count()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_item')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    color_variant = models.ForeignKey(ColorVariant, on_delete=models.SET_NULL, null=True, blank=True)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.product.product_name} in {self.cart.user.username}'s Cart"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Wishlist"

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='wishlist_item')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    color_variant = models.ForeignKey(ColorVariant, on_delete=models.SET_NULL, null=True, blank=True)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.product.product_name} in {self.wishlist.user.username}'s wishlist"

