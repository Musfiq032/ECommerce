from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify

class Brand(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='Categories', null=True,blank=True)
    description = RichTextField(default="Nothing is available", blank=True, null=True)
    status= models.BooleanField(default=False, help_text="0=default, 1=hidden")
    trending= models.BooleanField(default=False, help_text="0=default, 1=hidden")
    meta_title= models.CharField(max_length=150, blank=True, null=True)
    meta_keywords= models.CharField(max_length=150, blank=True, null=True)
    meta_description= models.CharField(max_length=150, blank=True, null=True)
    created_at= models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Brand, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='Categories', null=True,blank=True)
    description = RichTextField(default="Nothing is available", blank=True, null=True)
    status= models.BooleanField(default=False, help_text="0=default, 1=hidden")
    trending= models.BooleanField(default=False, help_text="0=default, 1=hidden")
    meta_title= models.CharField(max_length=150, blank=True, null=True)
    meta_keywords= models.CharField(max_length=150, blank=True, null=True)
    meta_description= models.CharField(max_length=150, blank=True, null=True)
    created_at= models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class ColorVariant(models.Model):
    color_name = models.CharField(max_length=50, default='')
    price = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.color_name


class SizeVariant(models.Model):
    size_name = models.CharField(max_length=50, default='')
    price = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.size_name



class Product(models.Model):
    product_name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    brand = models.ForeignKey(Brand, on_delete=models.DO_NOTHING, default="nothing")
    size_variant = models.ManyToManyField(SizeVariant, blank=True)
    color_variant = models.ManyToManyField(ColorVariant, blank=True)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=1, null=False,blank=False)
    description = RichTextField(blank=False, null=False, default='')
    slug = models.SlugField(unique=True, blank=True, null=True)
    status= models.BooleanField(default=False, help_text="0=default, 1=hidden")
    trending= models.BooleanField(default=False, help_text="0=default, 1=hidden")
    tag= models.CharField(max_length=150, blank=True, null=True)
    meta_title= models.CharField(max_length=150, blank=True, null=True)
    meta_keywords= models.CharField(max_length=150, blank=True, null=True)
    meta_description= models.CharField(max_length=150, blank=True, null=True)
    published_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.product_name

    def get_product_price_by_size(self, size):

        return self.price + SizeVariant.objects.get(size_name= size).price

    def get_prod_count_by_category(self,subcat_slug):
        return Product.objects.filter(subcategory=subcat_slug).count()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(upload_to='Product')

class Coupon(models.Model):
    coupon_code= models.CharField(max_length=50)
    is_expired= models.BooleanField(default=False)
    discount_price= models.IntegerField(default=100)
    minimum_amount= models.IntegerField(default=500)

    def __str__(self) -> str:
        return self.coupon_code


