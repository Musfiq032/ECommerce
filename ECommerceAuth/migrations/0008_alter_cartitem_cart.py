# Generated by Django 4.1.5 on 2023-01-11 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ECommerceAuth', '0007_coupon_cart_coupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='ECommerceAuth.cart'),
        ),
    ]