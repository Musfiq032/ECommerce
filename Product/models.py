from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify


class Brand(models.Model):
    brand_name= models.CharField(max_length=250, blank=True, null=True,default='None')

    def __str__(self):
        return self.brand_name

class Category(models.Model):
    category_name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True, null=True)
    category_image = models.ImageField(upload_to='Categories')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    subcategory_name = models.CharField(max_length=50, default='')
    main_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True, null=True)
    subcategory_image = models.ImageField(upload_to='Sub Categories', default='')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.subcategory_name)
        super(SubCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.subcategory_name




class ColorVariant(models.Model):
    color_name = models.CharField(max_length=50, default='')
    brand= models.ForeignKey(Brand, on_delete=models.CASCADE, default=1)
    price = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.color_name


class SizeVariant(models.Model):
    size_name = models.CharField(max_length=50, default='')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, default=1)
    price = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return self.size_name



class Product(models.Model):
    product_name = models.CharField(max_length=50)
    brand= models.ForeignKey(Brand, on_delete=models.DO_NOTHING, default=1)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.DO_NOTHING)
    size_variant = models.ManyToManyField(SizeVariant, blank=True)
    color_variant = models.ManyToManyField(ColorVariant, blank=True)
    discount = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    description = RichTextField(blank=False, null=False, default='')
    published_date = models.DateField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

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


