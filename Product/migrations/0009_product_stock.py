# Generated by Django 4.1.5 on 2023-01-14 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0008_coupon_product_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.IntegerField(default=1),
        ),
    ]
