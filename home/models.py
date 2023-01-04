from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50,default=' ')
    subcategory = models.CharField(max_length=50, default=' ')
    price = models.FloatField(default=0)
    description = RichTextField(blank=False, null=False, default='')
    published_date = models.DateField(auto_now_add=True)

    images = models.ImageField(upload_to='Product/images', blank=False, default='')

    def __str__(self) -> str:
        return self.product_name

